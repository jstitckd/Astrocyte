"""Accepted measurements; these are descriptions, not clinical thresholds."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Metric:
    label: str
    unit: str
    meaning: str
    decimals: int = 0


METRICS = {
    "heart_rate": Metric("Resting heart rate", "bpm", "Individual resting measurement"),
    "hrv": Metric("Heart rate variability", "ms", "Individual RMSSD measurement"),
    "sleep_hours": Metric("Sleep duration", "h", "Total for the sleep episode ending on this date", 1),
    "spo2": Metric("Oxygen saturation", "%", "Individual peripheral oxygen saturation measurement", 1),
    "body_temperature": Metric("Body temperature", "°C", "Individual temperature measurement", 1),
    "activity_minutes": Metric("Activity duration", "min", "Daily total; one total per crew and UTC date"),
    "exercise_heart_rate": Metric("Exercise heart rate", "bpm", "Individual measurement during exercise"),
    "fluid_ml": Metric("Fluid intake", "mL", "Daily logged total; one total per crew and UTC date"),
    "energy_kcal": Metric("Energy intake", "kcal", "Daily logged total; one total per crew and UTC date"),
    "eva_minutes": Metric("EVA duration", "min", "Daily total; one total per crew and UTC date"),
    "radiation_msv": Metric("Recorded exposure", "mSv", "Daily dosimeter total; one total per crew and UTC date", 3),
}

DAILY_TOTALS = {"activity_minutes", "fluid_ml", "energy_kcal", "eva_minutes", "radiation_msv"}
READING_COLUMNS = ["timestamp", "crew_id", "metric", "value", "unit", "data_source"]
CREW_NAMES = {"crew-01": "Alex Morgan", "crew-02": "Sam Okafor", "crew-03": "Yuki Tanaka"}
