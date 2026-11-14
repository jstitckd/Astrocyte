"""Science and workshops. Add your team's content below the title."""
import streamlit as st

from models.areas import HABITAT_AREAS


def render():
    st.title(HABITAT_AREAS["science"].name)
    # Add your laboratory and workshop content here.
