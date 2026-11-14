"""Blank exercise page. Keep this page's content in this file."""
import streamlit as st

from models.areas import HABITAT_AREAS


def render():
    st.title(HABITAT_AREAS["exercise"].name)
    # Add your page content below.
