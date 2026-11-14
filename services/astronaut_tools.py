"""Read-only data for profile summaries and demonstration test entry."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (("_test", "Health tests"), ("_extra", "Strength"), ("_30days", "Recovery"), ("", "Telemetry"), ("_menstrual_cycle", "Cycle tracking"))
EXCLUDED = {"astronaut", "date", "time_station_clock", "data_type", "activity", "hrv_status", "hrv_7day_avg_ms", "established_hrv_baseline_low_ms", "established_hrv_baseline_high_ms", "vo2_max_last_estimate_date", "cycle_number", "cycle_day", "cycle_phase", "contraception_protocol", "reported_symptoms"}
MEASUREMENTS = {
    "dominant_handgrip_best_of_3_kgf": ("Dominant handgrip · best of three", "kgf"),
    "psychomotor_vigilance_median_reaction_time_ms": ("Psychomotor vigilance · reaction time", "ms"),
    "working_memory_2back_accuracy_pct": ("Working memory · 2-back accuracy", "%"),
    "dxa_total_hip_bone_density_g_cm2": ("DXA · total hip bone density", "g/cm²"),
    "isometric_mid_thigh_pull_peak_force_best_of_3_n": ("Isometric mid-thigh pull · peak force", "N"),
    "seated_leg_press_1rm_kg": ("Seated leg press · one-repetition maximum", "kg"),
    "chest_cable_isometric_peak_force_best_of_3_n": ("Chest cable · peak force", "N"),
    "row_cable_isometric_peak_force_best_of_3_n": ("Row cable · peak force", "N"),
    "sleep_score_1_100": ("Sleep score", "/100"),
    "hrv_overnight_avg_ms": ("Overnight HRV", "ms"),
    "vo2_max_estimate_ml_kg_min": ("VO₂ max estimate", "mL/kg/min"),
    "heart_rate_bpm": ("Heart rate", "bpm"),
    "oxygen_saturation_pct": ("Oxygen saturation · SpO₂", "%"),
    "basal_body_temp_c": ("Basal body temperature", "°C"),
    "menstrual_flow": ("Menstrual flow", ""),
    "ovulation_lh_test": ("Ovulation · LH test", ""),
}


def profile_data(astronaut_id):
    # Identifiers come from the application's astronaut registry, not file input.
    from models.astronauts import Astronauts
    if astronaut_id not in Astronauts:
        raise ValueError("Unknown astronaut")
    result = {}
    for suffix, _ in SOURCES:
        path = ROOT / "data" / f"{astronaut_id.lower()}{suffix}.csv"
        if path.exists():
            frame = pd.read_csv(path)
            if not frame.empty:
                result[suffix] = frame
    return result


def test_catalogue(frames):
    tests = []
    for suffix, group in SOURCES:
        if suffix not in frames:
            continue
        for column in frames[suffix].columns:
            if column in EXCLUDED:
                continue
            label, unit = MEASUREMENTS.get(column, (column.replace("_", " ").capitalize(), ""))
            series = frames[suffix][column].dropna()
            numeric = not series.empty and pd.to_numeric(series, errors="coerce").notna().all()
            tests.append({"id": column, "label": label, "unit": unit, "group": group, "numeric": bool(numeric)})
    return tests


def profile_insights(frames):
    """Describe observed differences; recommendations concern review and logging."""
    recovery = frames["_30days"]
    latest = recovery.iloc[-1]
    first = recovery.iloc[0]
    hrv, low, high = (float(latest[key]) for key in ("hrv_overnight_avg_ms", "established_hrv_baseline_low_ms", "established_hrv_baseline_high_ms"))
    position = "below" if hrv < low else "above" if hrv > high else "within"
    insights = [f"Overnight HRV is {hrv:g} ms, {position} the recorded personal baseline of {low:g}–{high:g} ms."]
    delta = float(latest["sleep_score_1_100"]) - float(first["sleep_score_1_100"])
    insights.append(f"Sleep score is {float(latest['sleep_score_1_100']):g}/100, a change of {delta:+g} points across the available recovery records.")
    recommendations = ["Review the overnight recording and sleep notes together before interpreting a change.", "Keep measurement timing and equipment consistent when comparing repeat tests."]
    if position != "within" or delta < 0:
        recommendations.insert(0, "Share the HRV and sleep trend with the mission medical officer for review.")
    tests = frames.get("_test")
    if tests is not None:
        first_rt = float(tests.iloc[0]["psychomotor_vigilance_median_reaction_time_ms"])
        latest_rt = float(tests.iloc[-1]["psychomotor_vigilance_median_reaction_time_ms"])
        insights.append(f"Latest reaction-time test: {latest_rt:g} ms ({latest_rt - first_rt:+g} ms versus the first available test).")
    return insights, recommendations
