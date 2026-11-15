"""Homepage snapshots and sample assignments. No clinical scoring or alerts."""
from pathlib import Path

import pandas as pd
import streamlit as st

from services.dashboard_weather import WEATHER_PATH, weather_snapshot
from models.astronauts import Astronauts
from services.crew_health import health_score

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_TASKS = (
    {"id": "medical-check", "crew": "Petrov", "area": "science", "title": "Medical check", "detail": "Record blood pressure measurement", "due": "Now", "urgent": True},
    {"id": "cognitive-test", "crew": "Alex", "area": "living", "title": "Cognitive test", "detail": "Complete the psychomotor vigilance test", "due": "11:30", "urgent": False},
    {"id": "vo2max-test", "crew": "Milou", "area": "exercise", "title": "VO₂ max test", "detail": "Complete the assigned aerobic fitness assessment", "due": "Today", "urgent": False},
)


@st.cache_data(show_spinner=False, ttl=30)
def environmental_snapshot():
    """Load the selected readings and their compact chart histories."""
    return weather_snapshot(WEATHER_PATH.read_bytes())


@st.cache_data(show_spinner=False, ttl=30)
def crew_snapshots():
    result = []
    for name in Astronauts:
        day = pd.read_csv(ROOT / "data" / f"{name.lower()}.csv")
        recovery = pd.read_csv(ROOT / "data" / f"{name.lower()}_30days.csv")
        latest = recovery.iloc[-1]
        result.append({
            "name": name,
            "health_score": health_score(Astronauts[name]),
            "hr": round(float(day.iloc[-1]["heart_rate_bpm"])),
            "spo2": float(day.iloc[-1]["oxygen_saturation_pct"]),
            "sleep_score": round(float(latest["sleep_score_1_100"])),
            "hrv": float(latest["hrv_overnight_avg_ms"]),
            "date": str(latest["date"]),
        })
    return result


def pending_tasks():
    completed = st.session_state.get("completed_habitat_tasks", [])
    return [dict(task) for task in SAMPLE_TASKS if task["id"] not in completed]


def complete_task(task_id):
    if task_id in {task["id"] for task in SAMPLE_TASKS}:
        st.session_state.completed_habitat_tasks = list(set(st.session_state.get("completed_habitat_tasks", [])) | {task_id})
