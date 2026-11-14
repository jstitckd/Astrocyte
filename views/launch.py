"""Spaceship and launch area. Add your team's content below the title."""
import streamlit as st

from models.areas import HABITAT_AREAS


def render():
    st.title(HABITAT_AREAS["launch"].name)
    # Add your spaceship and launch area content here.
