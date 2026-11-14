"""Start the blank template with python -m streamlit run app.py."""
from pathlib import Path

import streamlit as st

from components.sidebar import render_sidebar
from views import data, eva, exercise, home, medical, nutrition, sleep, wellbeing, Alex

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Astrocyte",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.html(f"<style>{(ROOT / 'frontend' / 'styles.css').read_text()}</style>")

# Each destination has its own file so teammates can edit independently.
VIEWS = {
    "home": home.render,
    "sleep": sleep.render,
    "exercise": exercise.render,
    "medical": medical.render,
    "nutrition": nutrition.render,
    "wellbeing": wellbeing.render,
    "eva": eva.render,
    "data": data.render,
    "Alex": Alex.render
}

if st.session_state.get("page") not in VIEWS:
    st.session_state.page = "home"

render_sidebar()
VIEWS[st.session_state.page]()
