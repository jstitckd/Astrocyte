"""Blank medical page. Keep this page's content in this file."""
import streamlit as st

from models.areas import AREAS


def render():
    st.title(AREAS["medical"].name)
    # Add your page content below.
