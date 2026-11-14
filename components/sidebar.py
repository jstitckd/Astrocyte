"""Shared branding and navigation. Page content belongs in views/."""

import base64
from pathlib import Path

import streamlit as st

from models.astronauts import Astronauts


LOGO_PATH = (
    Path(__file__).resolve().parents[1]
    / "frontend"
    / "astrocyte-mark.png"
)


def _brand_mark():
    """Frame the supplied mark as SVG; leave the source PNG unchanged."""
    colour = st.get_option("theme.primaryColor") or "#d093f6"
    red, green, blue = (
        int(colour[index:index + 2], 16) / 255
        for index in (1, 3, 5)
    )

    source = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'viewBox="517 31 718 685">'
        '<defs><filter id="mark" color-interpolation-filters="sRGB">'
        '<feColorMatrix in="SourceGraphic" type="matrix" result="purple" '
        f'values="0 0 0 0 {red} '
        f'0 0 0 0 {green} '
        f'0 0 0 0 {blue} '
        '0 -4 4 0 -0.3"/>'
        '<feComposite in="purple" in2="SourceGraphic" operator="in"/>'
        '</filter></defs>'
        f'<image width="1717" height="916" '
        f'href="data:image/png;base64,{source}" filter="url(#mark)"/>'
        '</svg>'
    )

    return (
        "data:image/svg+xml;base64,"
        + base64.b64encode(svg.encode()).decode("ascii")
    )


def go(page):
    st.session_state.page = page


def _inject_sidebar_styles():
    st.markdown(
        """
        <style>
            /* Keep a narrow sidebar footprint. */
            html body section[data-testid="stSidebar"] {
                width: 4.5rem !important;
                min-width: 4.5rem !important;
                max-width: 4.5rem !important;
                transform: none !important;
                margin-left: 0 !important;
                visibility: visible !important;
                overflow: visible !important;
                z-index: 999999 !important;
            }

            /* Hide Streamlit's collapse and resize controls. */
            html body [data-testid="stSidebarCollapseButton"],
            html body [data-testid="stSidebarResizeHandle"] {
                display: none !important;
            }

            /* Expand over the page when hovered. */
            html body section[data-testid="stSidebar"]
            [data-testid="stSidebarContent"] {
                position: absolute !important;
                top: 0;
                left: 0;
                height: 100%;
                width: 4.5rem;
                overflow-x: hidden !important;
                background-color: inherit;
                transition:
                    width 0.22s ease,
                    box-shadow 0.22s ease;
            }

            html body section[data-testid="stSidebar"]:hover
            [data-testid="stSidebarContent"] {
                width: 17.5rem;
                box-shadow: 8px 0 24px rgba(0, 0, 0, 0.45);
            }

            /* Branding. */
            html body section[data-testid="stSidebar"] .wordmark {
                display: flex;
                align-items: center;
                gap: 0.65rem;
                white-space: nowrap;
                overflow: hidden;
            }

            html body section[data-testid="stSidebar"] .brand-mark {
                width: 28px;
                height: 28px;
                flex-shrink: 0;
            }

            html body section[data-testid="stSidebar"]:not(:hover)
            .wordmark {
                justify-content: center;
                gap: 0;
            }

            html body section[data-testid="stSidebar"]:not(:hover)
            .brand-name {
                display: none;
            }

            /* Three dots beneath the logo when compressed.
               Reserve their space so navigation does not jump. */
            html body section[data-testid="stSidebar"]
            .sidebar-dots {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 1.5rem;
                margin-top: 0.35rem;
                font-size: 1.5rem;
                line-height: 1;
                opacity: 0.65;
                user-select: none;
                pointer-events: none;
            }

            html body section[data-testid="stSidebar"]:hover
            .sidebar-dots {
                visibility: hidden;
            }

            /* Section heading. */
            html body section[data-testid="stSidebar"]
            .sidebar-section-heading {
                margin: 0;
                padding: 0 0.85rem;
                font-size: 0.8rem;
                font-weight: 600;
                line-height: 1.5rem;
                white-space: nowrap;
                overflow: hidden;
                opacity: 0.7;
            }

            html body section[data-testid="stSidebar"]:not(:hover)
            .sidebar-section-heading {
                visibility: hidden;
                opacity: 0;
                transition: none;
            }

            html body section[data-testid="stSidebar"]:hover
            .sidebar-section-heading {
                visibility: visible;
                opacity: 0.7;
                transition: opacity 0.1s ease 0.22s;
            }

            /* Navigation button boxes keep a consistent height. */
            html body section[data-testid="stSidebar"]
            [data-testid="stButton"] button {
                height: 2.75rem !important;
                min-height: 2.75rem !important;
                min-width: 0 !important;
                justify-content: flex-start !important;
                text-align: left !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                padding: 0 0.85rem !important;
            }

            /* Prevent labels from wrapping or shrinking. */
            html body section[data-testid="stSidebar"]
            [data-testid="stButton"] button > * {
                flex-shrink: 0 !important;
            }

            html body section[data-testid="stSidebar"]
            [data-testid="stButton"] button p {
                margin: 0 !important;
                width: auto !important;
                white-space: nowrap !important;
                word-spacing: normal !important;
            }

            /* Hide all text and icons immediately when compressed. */
            html body section[data-testid="stSidebar"]:not(:hover)
            [data-testid="stButton"] button * {
                visibility: hidden !important;
                opacity: 0 !important;
                transition: none !important;
            }

            /* Reveal labels after the sidebar finishes expanding. */
            html body section[data-testid="stSidebar"]:hover
            [data-testid="stButton"] button * {
                visibility: visible !important;
                opacity: 1 !important;
                transition: opacity 0.1s ease 0.22s !important;
            }

            html body section[data-testid="stSidebar"]:not(:hover)
            [data-testid="stButton"] button {
                padding: 0 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.session_state.setdefault("page", "home")
    _inject_sidebar_styles()

    with st.sidebar:
        st.markdown(
            '<div class="wordmark" role="img" aria-label="Astrocyte">'
            f'<img class="brand-mark" src="{_brand_mark()}" alt=""/>'
            '<span class="brand-name">'
            'astrocyte<span class="brand-dot">.</span>'
            '</span>'
            '</div>'
            '<div class="sidebar-dots" aria-hidden="true">⋮</div>',
            unsafe_allow_html=True,
        )

        st.divider()

        _nav("home", "⌂   Base overview")

        st.divider()

        st.markdown(
            '<h2 class="sidebar-section-heading">'
            'Astronaut profiles'
            '</h2>',
            unsafe_allow_html=True,
        )

        for astronaut_id, astronaut in Astronauts.items():
            _nav(
                astronaut_id,
                f"{astronaut.icon}   {astronaut.name}",
            )

        st.divider()

        _nav("data", "↧   Data & exports")


def _nav(page, label):
    st.button(
        label,
        key="nav_" + page,
        type=(
            "primary"
            if st.session_state.page == page
            else "secondary"
        ),
        width="stretch",
        on_click=go,
        args=(page,),
    )