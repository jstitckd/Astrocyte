"""Power systems. Add your team's content below the title."""
import streamlit as st

from models.areas import HABITAT_AREAS


def render():
    st.title(HABITAT_AREAS["power"].name)
    # Add your power generation and storage content here.
