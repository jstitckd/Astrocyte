"""Shared branding and navigation. Page content belongs in views/."""
import base64
from pathlib import Path

import streamlit as st

from models.areas import AREAS

LOGO_PATH = Path(__file__).resolve().parents[1] / "frontend" / "astrocyte-mark.png"


def _brand_mark():
    """Frame the supplied mark as SVG; leave the source PNG unchanged.

    The colour filter uses blue-minus-green to keep the purple silhouette
    and discard neutral white/black residue in the supplied cutout.
    """
    colour = st.get_option("theme.primaryColor") or "#d093f6"
    red, green, blue = (int(colour[index:index + 2], 16) / 255 for index in (1, 3, 5))
    source = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="517 31 718 685">'
        '<defs><filter id="mark" color-interpolation-filters="sRGB">'
        '<feColorMatrix in="SourceGraphic" type="matrix" result="purple" '
        f'values="0 0 0 0 {red} 0 0 0 0 {green} 0 0 0 0 {blue} 0 -4 4 0 -0.3"/>'
        '<feComposite in="purple" in2="SourceGraphic" operator="in"/>'
        '</filter></defs>'
        f'<image width="1717" height="916" href="data:image/png;base64,{source}" filter="url(#mark)"/>'
        '</svg>'
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode("ascii")


def go(page):
    st.session_state.page = page


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="wordmark" role="img" aria-label="Astrocyte">'
            f'<img class="brand-mark" src="{_brand_mark()}" alt=""/>'
            '<span class="brand-name">astrocyte<span class="brand-dot">.</span></span>'
            '</div>',
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
