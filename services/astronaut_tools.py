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

TEST_INSTRUCTIONS = {
    "dominant_handgrip_best_of_3_kgf": {
        "summary": "Maximal isometric grip strength of the dominant hand.",
        "equipment": "Calibrated hand dynamometer",
        "steps": [
            "Sit upright, feet flat, upper arm against the torso, elbow at 90°, forearm in neutral position.",
            "Adjust the dynamometer handle so the second finger joint wraps comfortably around the grip.",
            "Squeeze as hard as possible for 3–5 seconds on the instructor's cue.",
            "Rest 30–60 seconds, then repeat for a total of 3 trials.",
            "Log the best of the three trials in kgf.",
        ],
        "tips": "Do not swing the arm or brace against the body. Use the same hand and posture every time.",
    },
    "psychomotor_vigilance_median_reaction_time_ms": {
        "summary": "Sustained attention measured as median reaction time to random stimuli.",
        "equipment": "PVT device or app, quiet room",
        "steps": [
            "Sit comfortably in a quiet, distraction-free spot with the device at eye level.",
            "Start the PVT. A stimulus (e.g. a counter) appears at random intervals of about 2–10 seconds.",
            "Press the response button as fast as possible each time the stimulus appears.",
            "Complete the full test duration without pausing (typically 3–10 minutes).",
            "Log the median reaction time reported at the end, in ms.",
        ],
        "tips": "Test at a consistent time of day and keep caffeine intake consistent beforehand.",
    },
    "working_memory_2back_accuracy_pct": {
        "summary": "Working memory accuracy on a 2-back task.",
        "equipment": "Cognitive test software, quiet room",
        "steps": [
            "Complete the short practice block first so the rules are clear.",
            "A sequence of items (letters or positions) is shown one at a time.",
            "Respond whenever the current item matches the one shown two steps earlier.",
            "Do not respond to non-matches. Stay focused for the full block.",
            "Log the overall accuracy percentage reported by the software.",
        ],
        "tips": "Avoid multitasking and keep the same device, screen and environment between sessions.",
    },
    "dxa_total_hip_bone_density_g_cm2": {
        "summary": "Total hip bone mineral density from a DXA scan.",
        "equipment": "DXA scanner, operated by a trained technician",
        "steps": [
            "Remove metal objects (belts, zips, jewellery) and wear light clothing.",
            "Lie supine on the scan table; the technician positions the leg with the hip slightly internally rotated, usually with a positioning brace.",
            "Stay completely still during the scan (a few minutes).",
            "Take the 'total hip' BMD value from the scan report.",
            "Log the value in g/cm².",
        ],
        "tips": "DXA involves a small radiation dose and is not repeated frequently. Use the same scanner and positioning for comparisons.",
    },
    "isometric_mid_thigh_pull_peak_force_best_of_3_n": {
        "summary": "Maximal whole-body pulling force in a fixed mid-thigh position.",
        "equipment": "Force plate or load cell, fixed bar or rack, lifting straps if needed",
        "steps": [
            "Warm up with a few submaximal pulls.",
            "Set the bar at mid-thigh height: knees about 125–145°, hips about 140–150°, torso upright, arms straight.",
            "Pull the slack out of the bar, then on the cue pull up as hard and as fast as possible for 3–5 seconds.",
            "Rest about 2 minutes between trials and perform 3 trials.",
            "Log the best peak force of the three trials in newtons (N).",
        ],
        "tips": "Keep the setup identical across sessions. Redo a trial if there is a visible countermovement before the pull.",
    },
    "seated_leg_press_1rm_kg": {
        "summary": "Heaviest load you can press once with good technique (1RM).",
        "equipment": "Seated leg press, weight plates, spotter or safety stops",
        "steps": [
            "Warm up with light sets, then take progressively heavier single reps.",
            "Use the same seat position and a fixed range of motion each time (e.g. knees to about 90°).",
            "Rest 3–5 minutes between attempts and aim to reach your 1RM within 3–5 attempts.",
            "A lift counts only if the full range is completed under control.",
            "Log the heaviest successful load in kg.",
        ],
        "tips": "Use the safety stops and have a spotter present. Stop if you feel pain.",
    },
    "chest_cable_isometric_peak_force_best_of_3_n": {
        "summary": "Maximal isometric pushing force at the chest cable station.",
        "equipment": "Cable station with force sensor, fixed handle position",
        "steps": [
            "Sit or stand in the standard position and set the handle height and cable angle to the recorded setup.",
            "Lock the cable so it cannot move, then take the slack out gently.",
            "Push as hard as possible for 3–5 seconds, ramping up over about 1 second.",
            "Rest 1–2 minutes and repeat for 3 trials.",
            "Log the best peak force in newtons (N).",
        ],
        "tips": "Keep posture and foot position identical across sessions.",
    },
    "row_cable_isometric_peak_force_best_of_3_n": {
        "summary": "Maximal isometric pulling force at the row cable station.",
        "equipment": "Cable station with force sensor, fixed handle position",
        "steps": [
            "Sit in the standard position with the chest supported or torso upright, as per the recorded setup.",
            "Lock the cable and take the slack out gently.",
            "Pull toward the torso as hard as possible for 3–5 seconds, ramping up over about 1 second.",
            "Rest 1–2 minutes and repeat for 3 trials.",
            "Log the best peak force in newtons (N).",
        ],
        "tips": "Avoid leaning back to add force. Keep the same handle and angle every time.",
    },
    "sleep_score_1_100": {
        "summary": "Overall sleep quality score from your wearable.",
        "equipment": "Sleep-tracking wearable",
        "steps": [
            "Wear the device snugly through the night.",
            "After waking, sync the device and open the sleep summary.",
            "Read the overall sleep score (1–100).",
            "Log the score for that night.",
        ],
        "tips": "Use the same device and wear position so scores stay comparable.",
    },
    "hrv_overnight_avg_ms": {
        "summary": "Average heart rate variability measured during sleep.",
        "equipment": "Wearable or chest strap with overnight HRV",
        "steps": [
            "Wear the device throughout the night.",
            "After waking, sync it and open the HRV summary.",
            "Read the overnight average HRV (usually RMSSD) in ms.",
            "Log the value.",
        ],
        "tips": "Do not compare values across different devices. Alcohol, illness and late meals can lower HRV.",
    },
    "vo2_max_estimate_ml_kg_min": {
        "summary": "Estimated maximal oxygen uptake, a measure of aerobic fitness.",
        "equipment": "Heart-rate wearable with VO₂ max estimation",
        "steps": [
            "Complete a steady, outdoor or treadmill run or brisk walk with heart rate tracking, as your device requires.",
            "Make sure your profile data (age, weight, max HR) is up to date.",
            "Open the device's fitness summary and read the VO₂ max estimate.",
            "Log the value in mL/kg/min.",
        ],
        "tips": "This is an estimate, not a lab measurement. Look at trends rather than single values.",
    },
    "heart_rate_bpm": {
        "summary": "Resting heart rate in beats per minute.",
        "equipment": "Wearable, chest strap or manual pulse check",
        "steps": [
            "Sit or lie quietly for 5 minutes without talking or moving.",
            "Measure for 30–60 seconds (or read a stable device value).",
            "Log the heart rate in bpm.",
        ],
        "tips": "Measure at a consistent time of day, away from exercise, caffeine and stress.",
    },
    "oxygen_saturation_pct": {
        "summary": "Blood oxygen saturation (SpO₂).",
        "equipment": "Fingertip pulse oximeter",
        "steps": [
            "Rest for a few minutes and warm your hand if it is cold. Remove nail polish.",
            "Clip the oximeter on a still fingertip with the hand resting at heart level.",
            "Wait 30 seconds or more until the reading is stable.",
            "Log the SpO₂ percentage.",
        ],
        "tips": "Cold fingers and movement give poor readings. Repeat if the signal is unstable.",
    },
    "basal_body_temp_c": {
        "summary": "Lowest resting body temperature, taken on waking.",
        "equipment": "Basal or digital thermometer",
        "steps": [
            "Measure immediately after waking, before getting up, eating, drinking or talking.",
            "Use the same method (e.g. oral) and the same time each day.",
            "Wait for the thermometer to finish and read the value to two decimals if possible.",
            "Log the temperature in °C.",
        ],
        "tips": "After poor sleep, illness or alcohol, note it, as these can shift the reading.",
    },
    "menstrual_flow": {
        "summary": "Observed menstrual flow level for the day.",
        "equipment": "None (self-observation)",
        "steps": [
            "Assess the day's flow using your protocol's scale (e.g. none, spotting, light, medium, heavy).",
            "Enter the observed level as text.",
        ],
        "tips": "Log consistently every day of the cycle, including days with no flow.",
    },
    "ovulation_lh_test": {
        "summary": "Urine LH test to detect the hormone surge before ovulation.",
        "equipment": "LH test strip or kit",
        "steps": [
            "Follow the kit instructions and test at a consistent time each day, avoiding the first morning urine unless the kit says otherwise.",
            "Limit fluids for 1–2 hours beforehand to avoid dilution.",
            "Dip or collect the sample as instructed and wait the stated time.",
            "Read the result within the window given in the instructions.",
            "Log the result (e.g. negative / positive).",
        ],
        "tips": "Do not read the strip after the time limit, as late lines can be misleading.",
    },
}

GROUP_FALLBACKS = {
    "Health tests": "Perform the test under the same conditions as previous sessions and follow the protocol or device instructions.",
    "Strength": "Warm up first, use the same setup and technique as before, and record the best valid trial.",
    "Recovery": "Take the value from your wearable or recovery log after waking, using the same device as before.",
    "Telemetry": "Take the reading at rest under consistent conditions and record the stable value.",
    "Cycle tracking": "Record the observation at a consistent time of day using the protocol's scale.",
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


def test_instructions(test):
    """Return structured instructions for a catalogue entry, with a generic fallback."""
    info = TEST_INSTRUCTIONS.get(test["id"])
    if info:
        return info
    return {
        "summary": f"Record a measurement for {test['label'].lower()}.",
        "equipment": "",
        "steps": [
            GROUP_FALLBACKS.get(test["group"], "Follow the protocol for this measurement."),
            "Enter the measured value" + (f" in {test['unit']}." if test["unit"] else "."),
        ],
        "tips": "Keep timing, equipment and conditions consistent so repeat tests can be compared.",
    }


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
