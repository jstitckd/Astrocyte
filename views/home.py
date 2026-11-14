"""Mission overview. Cards, map and crew tasks are independently editable."""
from pathlib import Path
import streamlit as st

from components.base_map import render_base_map
from components.dashboard import environmental_cards, crew_card
from services.dashboard import environmental_snapshot, crew_snapshots, pending_tasks, complete_task


def _remember_task_panel():
    st.session_state.show_habitat_tasks = st.session_state.habitat_tasks_toggle


def render():
    styles = (Path(__file__).resolve().parents[1] / "frontend/dashboard.css").read_text()
    st.html(f"<style>{styles}</style>")
    with st.container(key="home_dashboard"):
        st.title("Base overview")
        st.html('<div class="dash-subtitle">Crew health &amp; habitat monitoring <span>Cabin &amp; crew: demo data</span></div>')
        try:
            environmental_cards(environmental_snapshot())
        except (OSError, ValueError) as exc:
            st.warning(f"Environmental readings unavailable: {exc}")
        tasks = pending_tasks()
        habitat, crew = st.columns([3.2, 1.1], gap="large")
        with habitat:
            selected_area = render_base_map(tasks=tasks)
            if selected_area:
                st.session_state.page = selected_area
                st.rerun()
        with crew:
            st.html('<h2 class="crew-heading">Crew health</h2><p class="crew-source">Synthetic telemetry · not a clinical assessment</p>')
            try:
                for member in crew_snapshots():
                    crew_card(member, tasks)
            except (OSError, KeyError, ValueError) as exc:
                st.warning(f"Crew snapshot unavailable: {exc}")
            st.html(f'<div class="today-heading">Today <strong>{len(tasks)} tasks remaining</strong><small>Sample assignments · this session</small></div>')
            st.toggle("View tasks", key="habitat_tasks_toggle", value=st.session_state.get("show_habitat_tasks", False), on_change=_remember_task_panel)
            if st.session_state.get("show_habitat_tasks"):
                if not tasks:
                    st.success("All tasks completed.")
                for task in sorted(tasks, key=lambda task: not task["urgent"]):
                    with st.container(border=True):
                        st.markdown(f"**{task['crew']} · {task['title']}**")
                        st.caption(f"{task['detail']} · Due {task['due']}")
                        st.button("Mark complete", key=f"complete_{task['id']}", on_click=complete_task, args=(task['id'],))
