"""Homepage. The illustration and interactions live in frontend/map/."""
import streamlit as st

from components.base_map import render_base_map


def render():
    st.title("Base overview")
    selected_area = render_base_map()
    if selected_area:
        st.session_state.page = selected_area
        st.rerun()

    # Add any other homepage content below.
