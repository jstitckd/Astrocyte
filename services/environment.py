"""Environmental data adapted from testing.py, without its Streamlit side effects.

The CSV aliases, LMST parsing and cabin demo formulas come from that prototype.
Weather readings are snapshots, cabin demo values are synthetic, and absent
channels stay missing. Irradiance is never treated as ionising radiation dose.
"""
from dataclasses import dataclass
import csv
from io import BytesIO, StringIO
import math
from pathlib import Path
import re

import numpy as np
import pandas as pd

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "mars_sol_1740_combined_20min_sensor_averages(2).csv"
MAX_BYTES = 5 * 1024 * 1024

# Optional channels are explicit about location and units; no gas/dust guesses.
ALIASES = {
    "air": ("Air_Temp_ATS_C", "Air_Temp_C", "air_temperature_c", "Air_Temp_TIRS_C"),
    "ground": ("Ground_Temp_C", "surface_temperature_c"),
    "pressure": ("Pressure_Pa", "atmospheric_pressure_pa"),
    "humidity": ("Relative_Humidity_pct", "humidity_pct"),
    "cabin_temp": ("Cabin_Temperature_C", "cabin_temp_c"),
    "cabin_pressure": ("Cabin_Pressure_kPa",),
    "o2": ("Cabin_O2_pct", "cabin_oxygen_pct"),
    "co2": ("Cabin_CO2_ppm", "cabin_carbon_dioxide_ppm"),
    "cabin_radiation": ("Cabin_Radiation_uSv_h", "cabin_dose_rate_usv_h"),
    "surface_radiation": ("Surface_Radiation_uSv_h", "outside_dose_rate_usv_h"),
    "dose_total": ("Recorded_Dose_mSv", "accumulated_dose_msv"),
    "cabin_pm25": ("Cabin_PM25_ug_m3",),
    "dust": ("Surface_Dust_mg_m3", "airborne_dust_mg_m3"),
    "perchlorate": ("Regolith_Perchlorate_wt_pct", "perchlorate_weight_pct"),
}
UNITS = {
    "air": "°C", "ground": "°C", "pressure": "Pa", "humidity": "%",
    "cabin_temp": "°C", "cabin_pressure": "kPa", "o2": "%", "co2": "ppm",
    "cabin_radiation": "µSv/h", "surface_radiation": "µSv/h", "dose_total": "mSv",
    "cabin_pm25": "µg/m³", "dust": "mg/m³", "perchlorate": "wt%",
}


@dataclass(frozen=True)
class Reading:
    value: float | None
    unit: str
    source: str  # csv, demo or missing
    note: str = ""


@dataclass(frozen=True)
class Snapshot:
    sol: int
    time: str
    end_time: str | None
    hour: float
    readings: dict[str, Reading]
    air_range: tuple[float, float] | None


def norm(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def match(frame, *aliases):
    columns = {norm(column): column for column in frame.columns}
    return next((columns[norm(alias)] for alias in aliases if norm(alias) in columns), None)


def clock(value):
    """LMST is local Mars time, not UTC. Preserve the supplied time string."""
    result = re.fullmatch(r"(\d{1,2}):(\d{2})(?::(\d{2}(?:\.\d+)?))?", str(value).strip())
    if not result:
        return float("nan")
    hour, minute, second = int(result[1]), int(result[2]), float(result[3] or 0)
    return hour + minute / 60 + second / 3600 if hour < 24 and minute < 60 and second < 60 else float("nan")


def load_csv(payload: bytes):
    """Normalize a Sol/LMST environmental snapshot file, preserving dropouts."""
    if len(payload) > MAX_BYTES:
        raise ValueError("Environmental CSV exceeds 5 MB. Use a smaller file.")
    try:
        header = next(csv.reader(StringIO(payload.decode("utf-8-sig"))), [])
        if len({norm(column) for column in header}) != len(header):
            raise ValueError("Environmental column names must be unique.")
        frame = pd.read_csv(BytesIO(payload), encoding="utf-8-sig", na_values=["null", "NULL", "N/A", "--"])
    except (UnicodeError, csv.Error, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise ValueError("Could not read the environmental CSV. Use a UTF-8, comma-separated file.") from exc
    if frame.empty or len(frame) > 50_000:
        raise ValueError("Environmental CSV must contain 1–50,000 rows.")
    frame.columns = frame.columns.str.strip()
    normalized = [norm(column) for column in frame.columns]
    if len(set(normalized)) != len(normalized) or any(column.startswith("__") for column in frame):
        raise ValueError("Environmental column names must be unique and cannot start with '__'.")
    sol_col = match(frame, "Sol", "mission_sol")
    time_col = match(frame, "LMST_Start", "LMST", "local_time")
    if sol_col is None or time_col is None:
        raise ValueError("Environmental CSV needs Sol and LMST_Start columns.")
    schema = {key: match(frame, *aliases) for key, aliases in ALIASES.items()}
    schema["end"] = match(frame, "LMST_End")
    if not any(schema[key] for key in ALIASES):
        raise ValueError("No supported environmental readings found. See docs/environment.md for columns and units.")
    frame["__sol"] = pd.to_numeric(frame[sol_col], errors="coerce")
    frame["__time"] = frame[time_col].astype(str).str.strip()
    frame["__hour"] = frame["__time"].map(clock)
    valid_sol = np.isfinite(frame["__sol"]) & frame["__sol"].ge(0) & frame["__sol"].mod(1).eq(0)
    if not valid_sol.all() or frame["__hour"].isna().any():
        raise ValueError("Every environmental row needs a non-negative whole Sol and a valid LMST start time before 24:00.")
    if frame.duplicated(["__sol", "__hour"]).any():
        raise ValueError("Duplicate Sol/LMST snapshots found. Use one station and one row per observation time.")
    frame["__sol"] = frame["__sol"].astype(int)
    for key in ALIASES:
        column = schema[key]
        if column is None:
            continue
        values = pd.to_numeric(frame[column], errors="coerce")
        values = values.where(np.isfinite(values)).replace([-9999, -99999], float("nan"))
        # Physical data checks, not health/safety thresholds.
        if key not in {"air", "ground", "cabin_temp"}:
            values = values.where(values.ge(0))
        if key in {"humidity", "o2", "perchlorate"}:
            values = values.where(values.le(100))
        if key in {"pressure", "cabin_pressure"}:
            values = values.where(values.gt(0))
        frame[column] = values
    return frame.sort_values(["__sol", "__hour"]).reset_index(drop=True), schema


def station_values(sol):
    """Synthetic cabin scenario from testing.py. These are not sensor readings."""
    sol = float(sol)
    return {
        "o2": 20.9 + 0.2 * math.sin(sol * 1.3),
        "co2": 2800 + 350 * math.sin(sol * 0.7),
        "cabin_pressure": 101.2 + 0.4 * math.sin(sol * 1.1),
        "cabin_temp": 22.4 + 0.6 * math.sin(sol * 0.5),
        "cabin_radiation": 14 + 2 * math.sin(sol * 0.8),
    }


def take_snapshot(frame, schema, sol, time, show_demo=True):
    rows = frame.loc[frame["__sol"].eq(sol) & frame["__time"].eq(time)]
    if rows.empty:
        raise ValueError("That environmental snapshot is no longer available. Choose another observation.")
    row = rows.iloc[0]
    demo = station_values(sol) if show_demo else {}
    readings = {}
    for key, unit in UNITS.items():
        column = schema.get(key)
        if column is not None:
            value = row[column]
            readings[key] = Reading(float(value), unit, "csv") if pd.notna(value) else Reading(None, unit, "missing", "No valid value at this observation")
        elif key in demo:
            readings[key] = Reading(demo[key], unit, "demo", "Synthetic cabin scenario from testing.py")
        else:
            readings[key] = Reading(None, unit, "missing", "No measurement channel in this CSV")
    day = frame.loc[frame["__sol"].eq(sol)]
    air = day[schema["air"]].dropna() if schema.get("air") else pd.Series(dtype=float)
    air_range = (float(air.min()), float(air.max())) if not air.empty else None
    end = row[schema["end"]] if schema.get("end") else None
    return Snapshot(int(sol), str(row["__time"]), str(end) if pd.notna(end) and end is not None else None, float(row["__hour"]), readings, air_range)


def converted(reading, temperature_unit="°C", pressure_unit="Pa"):
    """Display conversion only; source readings always retain their own units."""
    if reading.unit == "°C" and temperature_unit == "°F":
        return Reading(reading.value * 9 / 5 + 32 if reading.value is not None else None, "°F", reading.source, reading.note)
    if reading.unit == "Pa" and pressure_unit == "mbar":
        return Reading(reading.value / 100 if reading.value is not None else None, "mbar", reading.source, reading.note)
    return reading
