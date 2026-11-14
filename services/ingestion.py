"""Single validation boundary for CSV files and future providers."""
import io
import re
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from models.metrics import DAILY_TOTALS, METRICS, READING_COLUMNS

MAX_UPLOAD_BYTES = 5 * 1024 * 1024


class DataValidationError(ValueError):
    """A message that may be displayed directly beside the upload control."""


def validate_readings(data) -> pd.DataFrame:
    """Return a normalized copy, or reject the entire dataset."""
    frame = pd.DataFrame(data).copy()
    missing = set(READING_COLUMNS) - set(frame.columns)
    if missing:
        raise DataValidationError("Missing columns: " + ", ".join(sorted(missing)) + ". Download the sample CSV for the format.")
    if frame.empty:
        raise DataValidationError("This file has a header but no readings. Add at least one row.")
    if len(frame) > 50_000:
        raise DataValidationError("This prototype accepts up to 50,000 readings per import.")
    frame = frame[READING_COLUMNS]
    for col in ("crew_id", "metric", "unit", "data_source"):
        if frame[col].isna().any():
            raise DataValidationError(f"{col} contains missing values. Every row needs a value.")
        frame[col] = frame[col].astype(str).str.strip()
        if frame[col].eq("").any() or frame[col].str.len().gt(120).any():
            raise DataValidationError(f"{col} must contain 1–120 characters in every row.")
        if frame[col].str.contains(r"[\x00-\x1f]", regex=True).any():
            raise DataValidationError(f"{col} cannot contain control characters.")
    if not frame.crew_id.map(lambda x: bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", x))).all():
        raise DataValidationError("crew_id must be a stable ID: 1–64 letters, digits, dots, underscores or hyphens, starting with a letter or digit.")
    unknown = sorted(set(frame.metric) - set(METRICS))
    if unknown:
        raise DataValidationError("Unknown metrics: " + ", ".join(unknown) + ". See Data & exports for accepted names.")
    expected_units = frame.metric.map(lambda name: METRICS[name].unit)
    wrong = frame.unit.ne(expected_units)
    if wrong.any():
        row = frame.loc[wrong].iloc[0]
        raise DataValidationError(f"Metric '{row.metric}' requires unit '{METRICS[row.metric].unit}', received '{row.unit}'. No automatic unit conversion is performed.")
    # Reject non-ISO dates before pandas can interpret locale-dependent formats.
    text = frame.timestamp.map(lambda value: value.isoformat() if isinstance(value, (datetime, pd.Timestamp)) else str(value))
    iso = text.str.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})?$")
    if not iso.all():
        raise DataValidationError("timestamp must be ISO 8601, for example 2026-11-14T08:00:00Z. Include a time; timestamps without an offset are treated as UTC.")
    frame["timestamp"] = pd.to_datetime(text, format="ISO8601", utc=True, errors="coerce")
    if frame.timestamp.isna().any():
        raise DataValidationError("Some timestamps are invalid dates or outside the supported timestamp range.")
    if frame.value.map(lambda value: isinstance(value, (bool, np.bool_))).any():
        raise DataValidationError("value must be numeric, not a boolean.")
    frame["value"] = pd.to_numeric(frame.value, errors="coerce")
    if not np.isfinite(frame.value.to_numpy(dtype=float)).all():
        raise DataValidationError("value must be a finite number in every row. Empty values, text, infinity and NaN are not accepted.")
    # This is a data-integrity check, not an assessment of a person's health.
    if frame.loc[frame.metric.ne("body_temperature"), "value"].lt(0).any():
        raise DataValidationError("Negative values are not valid for these metrics (temperature may be negative). Check the source file.")
    if frame.duplicated(["crew_id", "timestamp", "metric"]).any():
        raise DataValidationError("Duplicate crew_id / timestamp / metric readings found. Resolve duplicates before importing, even if the sources differ.")
    daily = frame[frame.metric.isin(DAILY_TOTALS)].copy()
    daily["date"] = daily.timestamp.dt.date
    if daily.duplicated(["crew_id", "date", "metric"]).any():
        raise DataValidationError("Daily-total metrics allow one row per crew, UTC date and metric. Combine incremental events into a daily total before importing.")
    return frame.sort_values(["timestamp", "crew_id", "metric"]).reset_index(drop=True)


def load_csv(content: bytes) -> pd.DataFrame:
    if len(content) > MAX_UPLOAD_BYTES:
        raise DataValidationError("File exceeds 5 MB. Split it into smaller date windows.")
    try:
        text = content.decode("utf-8-sig")
        frame = pd.read_csv(io.StringIO(text), dtype={"crew_id": str, "metric": str, "unit": str, "data_source": str})
    except (UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise DataValidationError("Could not read this UTF-8 CSV. Use a comma separator and the sample file's headers.") from exc
    return validate_readings(frame)


def filter_readings(frame, crew_id, start_date, end_date) -> pd.DataFrame:
    """Inclusive UTC dates. An empty window returns an empty copy."""
    start = pd.Timestamp(start_date).tz_localize("UTC")
    end = pd.Timestamp(end_date).tz_localize("UTC") + timedelta(days=1)
    if start >= end:
        raise ValueError("Start date must be on or before end date.")
    return frame.loc[frame.crew_id.eq(crew_id) & frame.timestamp.ge(start) & frame.timestamp.lt(end)].copy()


def readings_csv(frame) -> bytes:
    """A CSV that round-trips through the same ingestion boundary."""
    out = frame.copy()
    out["timestamp"] = out.timestamp.dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return out.to_csv(index=False).encode("utf-8")
