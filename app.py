"""Small integration point. Start with python -m streamlit run app.py."""
from pathlib import Path

import streamlit as st

from components.sidebar import render_sidebar
from models.areas import AREAS
from services.storage import SessionStore
from views.dashboard import render_dashboard
from views.data import render_data
from views.home import render_home

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Astrocyte · Your habitat, your health", page_icon="✳", layout="wide", initial_sidebar_state="expanded")
st.html(f"<style>{(ROOT / 'frontend' / 'styles.css').read_text()}</style>")
store = SessionStore(st.session_state)
context = render_sidebar(store)

source = "SIMULATED DATA" if context.is_demo else "IMPORTED CSV" if not context.all_readings.empty else "AWAITING IMPORT"
source_style = "" if context.is_demo else " imported"
st.markdown(f'<div class="topline"><span>ARES OUTPOST <strong>/</strong> CREW HEALTH</span><span class="source-pill{source_style}">○ &nbsp; {source}</span></div>', unsafe_allow_html=True)
if context.is_demo:
    st.caption("DEMO MISSION · 1–14 NOV 2026 · All readings are synthetic, including daily intake logs. No live sensors connected.")
elif context.all_readings.empty:
    st.info("Select a CSV in the sidebar to load measurements, or switch to Demo mission. You can explore the habitat while you wait.")
else:
    st.caption("IMPORTED SNAPSHOT · User-supplied measurements, not automatically refreshed or independently verified.")

if st.session_state.flash:
    st.success(st.session_state.flash)
    st.session_state.flash = None
page = st.session_state.page
if page in AREAS:
    render_dashboard(context, page)
elif page == "data":
    render_data(context)
else:
    render_home(context)
st.markdown('<div class="footer-line"><span>✳ ASTROCYTE · MADE FOR LIFE BEYOND EARTH</span><span>Student prototype · No medical assessments · Session storage</span></div>', unsafe_allow_html=True)
