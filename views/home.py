from html import escape

import streamlit as st

from components.base_map import render_base_map
from components.readings import metric_cards
from components.tasks import completion
from models.metrics import CREW_NAMES
from services.navigation import destination


def render_home(context):
    st.markdown('<div class="eyebrow">YOUR SPACE TO THRIVE</div>', unsafe_allow_html=True)
    st.title("A little closer to home.")
    st.markdown('<div class="subtitle">Explore your habitat. Check in with yourself. Make every sol count.<br>Your daily health routines, connected in one place.</div>', unsafe_allow_html=True)
    crew_name = escape(CREW_NAMES.get(context.crew_id, context.crew_id))
    st.markdown(f'<div class="mission-line"><span>CREW <b>{crew_name}</b></span><span>WINDOW <b>{context.start_date:%d %b} — {context.end_date:%d %b %Y}</b></span><span><b>{len(context.readings):,}</b> readings in view</span></div>', unsafe_allow_html=True)
    event = render_base_map()
    area = destination(event, st.session_state.last_map_event)
    if area:
        st.session_state.last_map_event = event["event_id"]
        st.session_state.page = area
        st.rerun()
    st.markdown('<div class="section-title"><h2>A moment for your health</h2><span>Latest in the selected window · UTC</span></div>', unsafe_allow_html=True)
    metric_cards(context.readings, ("heart_rate", "sleep_hours", "fluid_ml"))
    st.write("")
    left, right = st.columns([1.25, 1], gap="large")
    with left:
        st.markdown("### Small steps, every day.")
        done, total = completion(context, context.end_date)
        st.caption(f"Checklist for {context.end_date:%d %b %Y} · {crew_name}")
        st.progress(done / total if total else 0, text=f"{done} of {total} tasks completed")
        st.caption("Open a building to review its readings and mark tasks complete. Progress reflects your checklist, not your health.")
    with right:
        count = len(context.store.checkins(context.dataset_id, context.crew_id, context.start_date, context.end_date))
        st.markdown(f'<div class="note-card"><div class="kicker">A NOTE TO YOUR FUTURE SELF</div><h3>{count} check-in{"s" if count != 1 else ""} in this window</h3><p>A short observation can help you remember how a day felt. Visit the greenhouse to start a mood & stress check-in.</p></div>', unsafe_allow_html=True)
