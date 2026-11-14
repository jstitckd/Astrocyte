import streamlit as st

from components.forms import checkin_history, render_checkin
from components.readings import history_chart, metric_cards
from components.tasks import render_tasks
from models.areas import AREAS


def render_dashboard(context, area_id):
    area = AREAS[area_id]
    st.markdown(f'<div class="eyebrow">HABITAT {area.code} / {area.name.upper()}</div>', unsafe_allow_html=True)
    st.title(area.subtitle)
    st.markdown(f'<div class="subtitle">{area.description}</div>', unsafe_allow_html=True)
    if context.readings.empty:
        st.info("No measurements in this window. Choose another date range or import readings. Missing measurements are not a health assessment.")
    if area.metrics:
        metric_cards(context.readings, area.metrics)
        st.write("")
    else:
        st.info("This space is for self-reported mood and stress. There are no mood sensors or automatically calculated wellbeing scores.")
    day = st.date_input("Check-in & checklist date · UTC", value=context.end_date,
                        min_value=context.start_date, max_value=context.end_date,
                        key=f"log_day_{context.dataset_id}_{context.crew_id}_{context.start_date}_{context.end_date}_{area_id}",
                        help="This date scopes task completion and new entries. Charts continue to use the whole sidebar window.")
    left, right = st.columns([1.8, 1], gap="large")
    with left:
        if area.metrics:
            history_chart(context.readings, area.metrics, area_id)
        render_checkin(context, area_id, day)
    with right:
        render_tasks(context, area_id, day)
    st.divider()
    checkin_history(context, area_id)
