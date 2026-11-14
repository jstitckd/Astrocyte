"""Living and working quarters. Add your team's content below the title."""
import streamlit as st

from models.areas import HABITAT_AREAS


def render():
    st.title(HABITAT_AREAS["living"].name)
    # Add your living and working quarters content here.
