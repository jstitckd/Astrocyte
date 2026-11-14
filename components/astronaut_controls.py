"""Shared profile-header actions and their Streamlit dialogs."""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st

from models.astronauts import Astronauts
from services.astronaut_tools import profile_data, profile_insights, test_catalogue


@st.dialog("Health summary", width="large")
def summary_dialog(astronaut_id, health_score):
    st.subheader(Astronauts[astronaut_id].name)
    try:
        frames = profile_data(astronaut_id)
        day, recovery = frames[""].iloc[-1], frames["_30days"].iloc[-1]
        score, heart, oxygen, sleep = st.columns(4)
        score.metric("Health score", f"{health_score:.1f}/10")
        heart.metric("Heart rate", f"{float(day['heart_rate_bpm']):g} bpm")
        oxygen.metric("SpO₂", f"{float(day['oxygen_saturation_pct']):g}%")
        sleep.metric("Sleep score", f"{float(recovery['sleep_score_1_100']):g}/100")
        st.caption(f"Telemetry: {day['date']} {day['time_station_clock']} · Recovery: {recovery['date']}")
        summary = st.session_state.get(f"health_summary_{astronaut_id}", {})
        if summary:
            st.caption(f"Recovery {summary['recovery_pillar']}% · Telemetry {summary['telemetry_pillar']}% · Health tests {summary['test_pillar']}%")
        insights, recommendations = profile_insights(frames)
        st.markdown("**Insights**")
        for insight in insights:
            st.markdown(f"- {insight}")
        st.markdown("**Recommendations**")
        for recommendation in recommendations:
            st.markdown(f"- {recommendation}")
    except (OSError, ValueError, KeyError) as exc:
        st.warning(f"Summary unavailable: {exc}")


@st.dialog("Log a test", width="large")
def test_log_dialog(astronaut_id):
    st.subheader(Astronauts[astronaut_id].name)
    try:
        tests = test_catalogue(profile_data(astronaut_id))
    except (OSError, ValueError) as exc:
        st.warning(f"Test list unavailable: {exc}")
        return
    if not tests:
        st.info("No tests are available for this profile.")
        return
    by_id = {test["id"]: test for test in tests}
    selected = st.selectbox("Choose a test", list(by_id), format_func=lambda key: f"{by_id[key]['group']} · {by_id[key]['label']}", key=f"log_test_{astronaut_id}", help="Scroll through the list or type to search.")
    test = by_id[selected]
    st.caption(f"{test['label']}" + (f" · Unit: {test['unit']}" if test["unit"] else ""))
    with st.form(f"test_log_form_{astronaut_id}_{selected}"):
        st.date_input("Date", value=datetime.now(ZoneInfo("Europe/Amsterdam")).date(), key=f"log_date_{astronaut_id}_{selected}")
        label = "Measured value" + (f" ({test['unit']})" if test["unit"] else "")
        if test["numeric"]:
            value = st.number_input(label, value=None, format="%.4f", key=f"log_value_{astronaut_id}_{selected}")
        else:
            value = st.text_input(label, key=f"log_value_{astronaut_id}_{selected}", placeholder="Enter the observed result")
        st.number_input("Test number", min_value=1, value=1, step=1, key=f"log_number_{astronaut_id}_{selected}")
        submitted = st.form_submit_button("Submit", type="primary")
    if submitted:
        if value is None or isinstance(value, str) and not value.strip():
            st.error("Enter a measured value before submitting.")
        else:
            st.success("Data being processed")
    st.caption("Demonstration entry · submitting does not change the datasets or health scores.")


def render_header_actions(astronaut_id, health_score):
    css = (Path(__file__).resolve().parents[1] / "frontend/astronaut_controls.css").read_text()
    st.html(f"<style>{css}</style>")
    if st.button("Summary & insights", key=f"profile_summary_{astronaut_id}", width="stretch"):
        summary_dialog(astronaut_id, health_score)
    if st.button("Log a test", key=f"profile_log_{astronaut_id}", width="stretch"):
        test_log_dialog(astronaut_id)
