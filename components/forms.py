import pandas as pd
import streamlit as st

FORM_TITLES = {
    "sleep": "Recovery observation", "exercise": "Exercise log", "medical": "Symptom check-in",
    "nutrition": "Meal & hydration log", "wellbeing": "Mood & stress check-in", "eva": "EVA observation",
}


def render_checkin(context, area_id, day):
    st.markdown("### " + FORM_TITLES[area_id])
    st.caption("SELF-REPORTED · Your entries stay separate from imported measurements. Nothing here measures your vital signs.")
    with st.form(f"checkin_{context.dataset_id}_{context.crew_id}_{area_id}", clear_on_submit=True):
        st.caption(f"Observation date: {day:%d %b %Y} · {context.crew_id}")
        fields = {}
        if area_id == "wellbeing":
            left, right = st.columns(2)
            fields["mood"] = left.slider("Mood · 1 low, 5 high", 1, 5, 3, key="mood")
            fields["stress"] = right.slider("Stress · 1 low, 5 high", 1, 5, 3, key="stress")
        elif area_id == "medical":
            fields["symptoms"] = st.multiselect("Symptoms to report", ["No symptoms to report", "Headache", "Fatigue", "Nausea", "Dizziness", "Discomfort", "Other"], key="symptoms")
        elif area_id == "exercise":
            fields["duration_minutes"] = st.number_input("Session duration (minutes) · self-reported", min_value=0, max_value=1440, value=0, step=5, key="exercise_duration")
        elif area_id == "nutrition":
            left, right = st.columns(2)
            fields["fluid_ml"] = left.number_input("Fluid in this entry (mL)", min_value=0, max_value=20000, value=0, step=100, key="nutrition_fluid")
            fields["energy_kcal"] = right.number_input("Energy in this entry (kcal)", min_value=0, max_value=20000, value=0, step=50, key="nutrition_energy")
            st.caption("Entry amounts, not daily totals. These do not overwrite the daily readings above.")
        placeholders = {"sleep": "How rested do you feel? Any recovery observations?", "exercise": "Activity type, effort and any observations…",
                        "medical": "Describe symptoms, observations or what to discuss with the crew…",
                        "nutrition": "What did you eat or drink? Add portion notes if useful…",
                        "wellbeing": "How are you feeling? What would help today?", "eva": "Observations to review with the crew…"}
        fields["notes"] = st.text_area("Notes", placeholder=placeholders[area_id], max_chars=2000, key="checkin_notes_" + area_id)
        submitted = st.form_submit_button("Save check-in", type="primary", disabled=context.all_readings.empty)
    if submitted:
        try:
            context.store.save_checkin(context.crew_id, area_id, day, context.dataset_id, fields)
            st.success("Check-in saved for this session. Export it from Data & exports before disconnecting.")
        except ValueError as exc:
            st.error(str(exc))


def checkin_history(context, area_id):
    records = context.store.checkins(context.dataset_id, context.crew_id, context.start_date, context.end_date, area_id)
    st.markdown("### Previous entries")
    st.caption("Self-reported entries · Selected crew, dataset and date window only.")
    if not records:
        st.info("No check-ins in this window yet. Save an entry above to begin your log.")
        return
    rows = []
    for record in reversed(records):
        row = {"Date": record["date"], "Saved at (UTC)": record["created_at"], **record["fields"]}
        if "symptoms" in row:
            row["symptoms"] = ", ".join(row["symptoms"])
        rows.append(row)
    if area_id == "wellbeing":
        # A descriptive history of the user's own ratings, never an invented score.
        import plotly.graph_objects as go

        figure = go.Figure()
        for field, color in (("mood", "#b9cba7"), ("stress", "#e4ac89")):
            figure.add_trace(go.Scatter(x=[record["date"] for record in records], y=[record["fields"][field] for record in records],
                                       name=field.title(), mode="lines+markers", line={"color": color},
                                       hovertemplate="%{x}<br>%{y} / 5<extra>%{fullData.name}</extra>"))
        figure.update_layout(height=240, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             font={"color": "#aebdb5"}, margin={"l": 0, "r": 0, "t": 8, "b": 0},
                             yaxis={"range": [0.5, 5.5], "dtick": 1, "gridcolor": "#303c40", "title": "Self-rating / 5"},
                             xaxis={"title": "Observation date (UTC)"}, legend={"orientation": "h"})
        st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
