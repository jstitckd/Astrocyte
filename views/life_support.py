"""Life support. Add your team's content below the title."""
import streamlit as st

from models.areas import HABITAT_AREAS


def render():
    st.title(HABITAT_AREAS["life_support"].name)
    # Add your environmental control and life support content here.
