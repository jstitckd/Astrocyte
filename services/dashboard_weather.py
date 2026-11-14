"""Dashboard readings from the supplied diurnal CSV; UV is not dose rate."""
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
import re

import numpy as np
import pandas as pd

from services.environment import Reading, station_values

WEATHER_PATH = Path(__file__).resolve().parents[1] / "data/mars_diurnal_weather_radiation-v2.csv"


@dataclass(frozen=True)
class DashboardEnvironment:
    time: str
    readings: dict[str, Reading]
    history: dict[str, list[tuple[str, float | None]]]


def weather_snapshot(payload, time="12:00"):
    frame = pd.read_csv(BytesIO(payload))
    required = {"Time", "Temperature_C", "Pressure_Pa", "UV_Index"}
    if not required.issubset(frame.columns):
        raise ValueError("Weather CSV needs Time, Temperature_C, Pressure_Pa and UV_Index columns.")
    frame["Time"] = frame["Time"].astype(str).str.strip()
    if frame["Time"].duplicated().any() or not frame["Time"].map(lambda value: bool(re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d|24:00", value))).all():
        raise ValueError("Weather CSV needs unique HH:MM times; 24:00 is allowed as the day endpoint.")
    frame = frame.sort_values("Time")
    rows = frame.loc[frame["Time"].eq(time)]
    if rows.empty:
        raise ValueError(f"Weather CSV has no observation at {time}.")
    row = rows.iloc[0]
    readings = {}
    history = {}
    for key, column, unit, minimum in (
        ("air", "Temperature_C", "°C", -273.15),
        ("pressure", "Pressure_Pa", "Pa", 0),
        ("uv_index", "UV_Index", "UV index", 0),
    ):
        values = pd.to_numeric(frame[column], errors="coerce")
        valid = np.isfinite(values) & values.ge(minimum)
        if key == "pressure":
            valid &= values.gt(0)
        values = values.where(valid)
        value = values.loc[row.name]
        readings[key] = Reading(float(value) if pd.notna(value) else None, unit, "csv" if pd.notna(value) else "missing", "Outside observation from the diurnal CSV")
        history[key] = [(str(at), float(value) if pd.notna(value) else None) for at, value in zip(frame["Time"], values)]
    # Preserve the existing cabin scenario; the new file contains no cabin gases.
    cabin = station_values(1740)
    readings["o2"] = Reading(cabin["o2"], "%", "demo", "Existing synthetic cabin scenario")
    readings["co2"] = Reading(cabin["co2"], "ppm", "demo", "Existing synthetic cabin scenario")
    for key in ("o2", "co2"):
        history[key] = [(time, readings[key].value)]
    return DashboardEnvironment(time, readings, history)
