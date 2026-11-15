"""Shared profile-header actions and their Streamlit dialogs."""
import html as html_lib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st

from models.astronauts import Astronauts
from services.astronaut_tools import profile_data, profile_insights, test_catalogue, test_instructions


DIALOG_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&display=swap');

div[data-testid="stDialog"] div[role="dialog"] {
    background: linear-gradient(180deg, #12161B 0%, #0C0E10 100%) !important;
    border: 1px solid #20262B !important;
    border-radius: 22px !important;
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.75) !important;
    color: #F2F4F5 !important;
    font-family: 'Barlow', sans-serif !important;
    font-variant-numeric: tabular-nums;
}

div[data-testid="stDialog"] div[role="dialog"] h2 {
    font-family: 'Barlow Condensed', sans-serif !important;
    letter-spacing: 0.02em;
    color: #F2F4F5 !important;
}

/* Header block inside dialog */
.dlg-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    padding-bottom: 14px;
    margin-bottom: 16px;
    border-bottom: 1px solid #20262B;
}
.dlg-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6FD3FF;
    margin-bottom: 2px;
}
.dlg-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 28px;
    font-weight: 600;
    color: #F2F4F5;
    line-height: 1.1;
}
.dlg-meta {
    font-size: 12px;
    color: #8A959D;
    margin-top: 3px;
}

/* Metric cards grid */
.dlg-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}
@media (max-width: 720px) {
    .dlg-kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
.dlg-kpi-card {
    background: #14171A;
    border: 1px solid #20262B;
    border-radius: 16px;
    padding: 14px 16px;
}
.dlg-kpi-label {
    font-size: 12px;
    font-weight: 500;
    color: #8A959D;
    margin-bottom: 6px;
}
.dlg-kpi-val {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 32px;
    font-weight: 600;
    line-height: 1.05;
    color: #F2F4F5;
}
.dlg-kpi-unit {
    font-family: 'Barlow', sans-serif;
    font-size: 14px;
    font-weight: 400;
    color: #6E7A83;
    margin-left: 3px;
}

/* Pillar bar strip */
.dlg-pillars {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    background: #14171A;
    border: 1px solid #20262B;
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 16px;
}
@media (max-width: 640px) {
    .dlg-pillars { grid-template-columns: 1fr; }
}
.dlg-pillar-top {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #9AA5AD;
    margin-bottom: 6px;
}
.dlg-pillar-top strong {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 16px;
    color: #F2F4F5;
}
.dlg-bar-track {
    height: 4px;
    border-radius: 999px;
    background: #20262B;
    overflow: hidden;
}
.dlg-bar-fill {
    display: block;
    height: 100%;
    border-radius: 999px;
}

/* Insights & Recommendations panels */
.dlg-panel-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}
@media (max-width: 720px) {
    .dlg-panel-grid { grid-template-columns: 1fr; }
}
.dlg-panel {
    background: #14171A;
    border: 1px solid #20262B;
    border-radius: 16px;
    padding: 16px;
}
.dlg-panel-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: #F2F4F5;
    margin-bottom: 10px;
}
.dlg-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 9px;
}
.dlg-list li {
    position: relative;
    padding-left: 14px;
    font-size: 13px;
    line-height: 1.45;
    color: #D5DBDF;
}
.dlg-list li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 7px;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #3DDC84;
}
.dlg-list.rec li::before {
    background: #6FD3FF;
}

/* Test Log footnote */
.dlg-footnote {
    font-size: 12px;
    color: #6E7A83;
    margin-top: 10px;
}

/* Test instructions */
.dlg-instr {
    background: #14171A;
    border: 1px solid #20262B;
    border-radius: 12px;
    padding: 14px 16px;
}
.dlg-instr-summary {
    font-size: 13px;
    color: #D5DBDF;
    margin-bottom: 10px;
}
.dlg-instr-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6FD3FF;
    margin: 10px 0 4px 0;
}
.dlg-instr ol {
    margin: 0;
    padding-left: 20px;
    font-size: 13px;
    line-height: 1.5;
    color: #D5DBDF;
}
.dlg-instr ol li { margin-bottom: 4px; }
.dlg-instr-note {
    font-size: 12px;
    color: #9AA5AD;
}

/* Style Streamlit form & inputs inside the dialog */
div[data-testid="stDialog"] [data-testid="stForm"] {
    background: #14171A !important;
    border: 1px solid #20262B !important;
    border-radius: 16px !important;
    padding: 18px !important;
}
div[data-testid="stDialog"] input,
div[data-testid="stDialog"] div[data-baseweb="select"] > div {
    background-color: #0C0E10 !important;
    border-color: #2A3138 !important;
    border-radius: 10px !important;
    color: #F2F4F5 !important;
}
</style>
"""


def _html(markup: str) -> str:
    return " ".join(line.strip() for line in markup.strip().splitlines())


def _score_color(score_10: float) -> str:
    if score_10 >= 8.0:
        return "#3DDC84"
    if score_10 >= 5.0:
        return "#FFC857"
    return "#FF5A4D"


def _pillar_color(pct: float) -> str:
    if pct >= 75:
        return "#3DDC84"
    if pct >= 55:
        return "#FFC857"
    return "#FF5A4D"


@st.dialog("Health summary", width="large")
def summary_dialog(astronaut_id, health_score):
    st.markdown(DIALOG_THEME_CSS, unsafe_allow_html=True)
    astronaut = Astronauts[astronaut_id]

    try:
        frames = profile_data(astronaut_id)
        day, recovery = frames[""].iloc[-1], frames["_30days"].iloc[-1]

        hr_val = float(day["heart_rate_bpm"])
        spo2_val = float(day["oxygen_saturation_pct"])
        sleep_val = float(recovery["sleep_score_1_100"])
        score_col = _score_color(health_score)

        st.markdown(
            _html(f"""
            <div class="dlg-header">
                <div>
                    <div class="dlg-eyebrow"></div>
                    <div class="dlg-title">{astronaut.name}</div>
                    <div class="dlg-meta"></div>
                </div>
            </div>

            <div class="dlg-kpi-grid">
                <div class="dlg-kpi-card">
                    <div class="dlg-kpi-label">Health score</div>
                    <div class="dlg-kpi-val" style="color: {score_col};">
                        {health_score:.1f}<span class="dlg-kpi-unit">/ 10</span>
                    </div>
                </div>
                <div class="dlg-kpi-card">
                    <div class="dlg-kpi-label">Heart rate</div>
                    <div class="dlg-kpi-val">
                        {hr_val:g}<span class="dlg-kpi-unit">bpm</span>
                    </div>
                </div>
                <div class="dlg-kpi-card">
                    <div class="dlg-kpi-label">Oxygen saturation</div>
                    <div class="dlg-kpi-val">
                        {spo2_val:g}<span class="dlg-kpi-unit">%</span>
                    </div>
                </div>
                <div class="dlg-kpi-card">
                    <div class="dlg-kpi-label">Sleep score</div>
                    <div class="dlg-kpi-val">
                        {sleep_val:g}<span class="dlg-kpi-unit">/ 100</span>
                    </div>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

        summary = st.session_state.get(f"health_summary_{astronaut_id}", {})
        if summary:
            rec_p = summary["recovery_pillar"]
            tel_p = summary["telemetry_pillar"]
            tst_p = summary["test_pillar"]
            st.markdown(
                _html(f"""
                <div class="dlg-pillars">
                    <div>
                        <div class="dlg-pillar-top"><span>30-day recovery</span><strong>{rec_p}%</strong></div>
                        <div class="dlg-bar-track"><span class="dlg-bar-fill" style="width:{rec_p}%; background:{_pillar_color(rec_p)};"></span></div>
                    </div>
                    <div>
                        <div class="dlg-pillar-top"><span>Station telemetry</span><strong>{tel_p}%</strong></div>
                        <div class="dlg-bar-track"><span class="dlg-bar-fill" style="width:{tel_p}%; background:{_pillar_color(tel_p)};"></span></div>
                    </div>
                    <div>
                        <div class="dlg-pillar-top"><span>Health tests</span><strong>{tst_p}%</strong></div>
                        <div class="dlg-bar-track"><span class="dlg-bar-fill" style="width:{tst_p}%; background:{_pillar_color(tst_p)};"></span></div>
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )

        insights, recommendations = profile_insights(frames)
        insights_items = "".join(f"<li>{item}</li>" for item in insights)
        rec_items = "".join(f"<li>{item}</li>" for item in recommendations)

        st.markdown(
            _html(f"""
            <div class="dlg-panel-grid">
                <div class="dlg-panel">
                    <div class="dlg-panel-title">Insights</div>
                    <ul class="dlg-list">{insights_items}</ul>
                </div>
                <div class="dlg-panel">
                    <div class="dlg-panel-title">Recommended Actions</div>
                    <ul class="dlg-list rec">{rec_items}</ul>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )
    except (OSError, ValueError, KeyError) as exc:
        st.warning(f"Summary unavailable: {exc}")


@st.dialog("Log a test", width="large")
def test_log_dialog(astronaut_id):
    st.markdown(DIALOG_THEME_CSS, unsafe_allow_html=True)
    astronaut = Astronauts[astronaut_id]

    st.markdown(
        _html(f"""
        <div class="dlg-header">
            <div>
                <div class="dlg-title">{astronaut.name}</div>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    try:
        tests = test_catalogue(profile_data(astronaut_id))
    except (OSError, ValueError) as exc:
        st.warning(f"Test list unavailable: {exc}")
        return
    if not tests:
        st.info("No tests are available for this profile.")
        return

    by_id = {test["id"]: test for test in tests}
    selected = st.selectbox(
        "Choose a test",
        list(by_id),
        format_func=lambda key: f"{by_id[key]['group']} · {by_id[key]['label']}",
        key=f"log_test_{astronaut_id}",
        help="Scroll through the list or type to search.",
    )
    test = by_id[selected]

    # How-to instructions for the selected test (updates when the selection changes)
    instr = test_instructions(test)
    esc = html_lib.escape
    steps_html = "".join(f"<li>{esc(step)}</li>" for step in instr["steps"])
    equipment_html = (
        f'<div class="dlg-instr-label">Equipment</div><div class="dlg-instr-note">{esc(instr["equipment"])}</div>'
        if instr.get("equipment") else ""
    )
    tips_html = (
        f'<div class="dlg-instr-label">Tips</div><div class="dlg-instr-note">{esc(instr["tips"])}</div>'
        if instr.get("tips") else ""
    )
    with st.expander("How to perform this test", expanded=True):
        st.markdown(
            _html(f"""
            <div class="dlg-instr">
                <div class="dlg-instr-summary">{esc(instr['summary'])}</div>
                {equipment_html}
                <div class="dlg-instr-label">Steps</div>
                <ol>{steps_html}</ol>
                {tips_html}
            </div>
            """),
            unsafe_allow_html=True,
        )

    with st.form(f"test_log_form_{astronaut_id}_{selected}"):
        col_date, col_trial = st.columns(2)
        with col_date:
            st.date_input(
                "Date",
                value=datetime.now(ZoneInfo("Europe/Amsterdam")).date(),
                key=f"log_date_{astronaut_id}_{selected}",
            )
        with col_trial:
            st.number_input(
                "Test / trial number",
                min_value=1,
                value=1,
                step=1,
                key=f"log_number_{astronaut_id}_{selected}",
            )

        label = "Measured value" + (f" ({test['unit']})" if test["unit"] else "")
        if test["numeric"]:
            value = st.number_input(
                label,
                value=None,
                format="%.4f",
                placeholder="0.0000",
                key=f"log_value_{astronaut_id}_{selected}",
            )
        else:
            value = st.text_input(
                label,
                key=f"log_value_{astronaut_id}_{selected}",
                placeholder="Enter the observed result",
            )

        submitted = st.form_submit_button("Log measurement", type="primary", use_container_width=True)

    if submitted:
        if value is None or (isinstance(value, str) and not value.strip()):
            st.error("Enter a measured value before submitting.")
        else:
            st.success("Measurement logged — data is being processed.")

    st.markdown(
        '<div class="dlg-footnote"></div>',
        unsafe_allow_html=True,
    )


def render_header_actions(astronaut_id, health_score):
    css = (Path(__file__).resolve().parents[1] / "frontend/astronaut_controls.css").read_text()
    plus_css = f"""
    .st-key-profile_log_{astronaut_id} button p {{
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        line-height: 1.1 !important;
    }}
    .st-key-profile_log_{astronaut_id} button p strong {{
        font-size: 1.45em !important;
        font-weight: 600 !important;
        line-height: 1 !important;
        display: inline-block !important;
        transform: translateY(-1px);
    }}
    """
    st.html(f"<style>{css}\n{plus_css}</style>")
    if st.button("Summary & insights", key=f"profile_summary_{astronaut_id}", width="stretch"):
        summary_dialog(astronaut_id, health_score)
    if st.button("**+** Log a test", key=f"profile_log_{astronaut_id}", width="stretch"):
        test_log_dialog(astronaut_id)