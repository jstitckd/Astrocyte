"""Shared branding and navigation. Page content belongs in views/."""
import streamlit as st

from models.areas import AREAS


def go(page):
    st.session_state.page = page


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="wordmark"><span>✳</span> astrocyte'
            '<span class="brand-dot">.</span></div>',
            unsafe_allow_html=True,
        )
        st.divider()
        _nav("home", "⌂   Base overview")
        for area_id, area in AREAS.items():
            _nav(area_id, f"{area.icon}   {area.name}")
        st.divider()
        _nav("data", "↧   Data & exports")


def _nav(page, label):
    st.button(
        label,
        key="nav_" + page,
        type="primary" if st.session_state.page == page else "secondary",
        width="stretch",
        on_click=go,
        args=(page,),
    )
