"""Deterministic, illustrative demo readings. Never presented as live data."""
from datetime import datetime, timedelta, timezone
import random

from models.metrics import METRICS
from services.ingestion import validate_readings


def demo_readings():
    rng = random.Random(42)
    rows = []
    baseline = {
        "heart_rate": (64, 5), "hrv": (53, 9), "sleep_hours": (7.5, 0.9),
        "spo2": (98, 0.6), "body_temperature": (36.7, 0.2),
        "activity_minutes": (48, 15), "exercise_heart_rate": (124, 16),
        "fluid_ml": (2450, 400), "energy_kcal": (2450, 350),
        "eva_minutes": (75, 25), "radiation_msv": (0.22, 0.06),
    }
    for day in range(14):
        for crew in range(1, 4):
            for name, (mean, spread) in baseline.items():
                value = mean + rng.uniform(-spread, spread)
                if name == "eva_minutes" and day % 3:
                    value = 0
                stamp = datetime(2026, 11, 1, 8, tzinfo=timezone.utc) + timedelta(days=day)
                if name in {"activity_minutes", "fluid_ml", "energy_kcal", "eva_minutes", "radiation_msv"}:
                    stamp = stamp.replace(hour=23, minute=59)
                elif name == "exercise_heart_rate":
                    stamp = stamp.replace(hour=15)
                rows.append({"timestamp": stamp.isoformat(), "crew_id": f"crew-{crew:02d}",
                             "metric": name, "value": round(value, max(1, METRICS[name].decimals)),
                             "unit": METRICS[name].unit,
                             "data_source": "synthetic-daily-log" if name in {"fluid_ml", "energy_kcal"} else "synthetic-sensor"})
    return validate_readings(rows)
