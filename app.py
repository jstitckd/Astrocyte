"""Start Astrocyte with python -m streamlit run app.py."""
from pathlib import Path

import streamlit as st

from components.sidebar import render_sidebar
from views import data, eva, exercise, home, medical, nutrition, sleep, wellbeing, Alex, Petrov, Amara, Milou
from views import greenhouse, launch, life_support, living, power, science, Petrov
from views import task_guide

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Astrocyte",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded",
)
styles = (ROOT / "frontend" / "styles.css").read_text()
accent = st.get_option("theme.primaryColor") or "#d093f6"
st.html(f"<style>{styles}\n:root{{--brand-accent:{accent};}}</style>")

# Each destination has its own file so teammates can edit independently.
VIEWS = {
    "task_guide": task_guide.render,
    "home": home.render,
    "sleep": sleep.render,
    "exercise": exercise.render,
    "medical": medical.render,
    "nutrition": nutrition.render,
    "wellbeing": wellbeing.render,
    "eva": eva.render,
    "Petrov": Petrov.render,
    "data": data.render,
    "Alex": Alex.render,
    "Amara": Amara.render,
    "Milou": Milou.render,
    "Petrov": Petrov.render
}

# Habitat-map destinations; existing crew and health routes remain available.
VIEWS.update({
    "living": living.render,
    "life_support": life_support.render,
    "science": science.render,
    "power": power.render,
    "greenhouse": greenhouse.render,
    "launch": launch.render,
})

if st.session_state.get("page") not in VIEWS:
    st.session_state.page = "home"

render_sidebar()
VIEWS[st.session_state.page]()
