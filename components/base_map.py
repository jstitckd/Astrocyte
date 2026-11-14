"""Embed the editable map and return a newly selected page ID."""
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import declare_component

from models.areas import HABITAT_AREAS

_map = declare_component(
    "mars_base",
    path=str(Path(__file__).resolve().parents[1] / "frontend" / "map"),
)


def render_base_map(tasks=None):
    """Return an area ID once per activation, or None when just exploring."""
    event = _map(
        tasks=tasks or [],
        background=st.get_option("theme.backgroundColor") or "#111619",
        areas=[
            {
                "id": area_id,
                "code": area.code,
                "name": area.name,
                "label": area.label,
                "description": area.description,
                "features": list(area.features),
                "category": area.category,
            }
            for area_id, area in HABITAT_AREAS.items()
        ],
        accent=st.get_option("theme.primaryColor") or "#d093f6",
        default=None,
        key="mars_base_map",
    )
    if not isinstance(event, dict):
        return None
    area_id, event_id = event.get("area"), event.get("event_id")
    if not isinstance(area_id, str) or area_id not in HABITAT_AREAS:
        return None
    if not isinstance(event_id, str) or not 1 <= len(event_id) <= 120:
        return None
    if event_id == st.session_state.get("last_map_event"):
        return None
    st.session_state.last_map_event = event_id
    task_id = event.get("task")
    if isinstance(task_id, str) and task_id in {task["id"] for task in (tasks or [])}:
        st.session_state.selected_habitat_task = task_id
        st.rerun()
    return area_id
