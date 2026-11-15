"""Mission overview. Cards, map and crew tasks are independently editable."""
from pathlib import Path
import streamlit as st

from components.base_map import render_base_map
from components.dashboard import environmental_cards, crew_card
from services.dashboard import environmental_snapshot, crew_snapshots, pending_tasks


def render():
    styles = (Path(__file__).resolve().parents[1] / "frontend/dashboard.css").read_text()
    st.html(f"<style>{styles}</style>")
    with st.container(key="home_dashboard"):
        st.title("Dashboard", anchor=False)
        tasks = pending_tasks()
        with st.container(key="crew_overview"):
            st.html('<h2 class="crew-heading">Crew health</h2>')
            try:
                members = crew_snapshots()
                if members:
                    for column, member in zip(st.columns(len(members), gap="small"), members):
                        with column:
                            crew_card(member, tasks)
            except (OSError, KeyError, ValueError) as exc:
                st.warning(f"Crew snapshot unavailable: {exc}")
        habitat, environment = st.columns([3.2, 1.1], gap="large")
        with habitat:
            selected_area = render_base_map(tasks=tasks, background="#0b0f12")
            if selected_area:
                st.session_state.page = selected_area
                st.rerun()
        with environment, st.container(key="environment_sidebar"):
            st.html('<h2 class="crew-heading">Environment</h2>')
            try:
                environmental_cards(environmental_snapshot())
            except (OSError, ValueError) as exc:
                st.warning(f"Environmental readings unavailable: {exc}")
        st.html('<footer class="map-credit">Map design assisted by SI.</footer>')
