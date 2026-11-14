"""Shared branding and navigation. Page content belongs in views/."""

import base64
from pathlib import Path

import streamlit as st

from models.astronauts import Astronauts
from services.crew_health import health_score as _health_score, score_colour as _score_colour


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
    sidebar = 'html body section[data-testid="stSidebar"]'
    astronaut_styles = []

    for astronaut_id, astronaut in Astronauts.items():
        button = f"{sidebar} .st-key-nav_{astronaut_id} button"
        score = _health_score(astronaut)
        colour = _score_colour(score) if score is not None else "#8a959d"
        angle = (score or 0) * 3.6

        astronaut_styles.append(
            f"""
            {button} {{
                position: relative !important;
                width: 100% !important;
                min-height: 3.75rem !important;
                padding: 0.55rem 3.65rem 0.55rem 0.65rem !important;
            }}

            /* Anchor the score to the button, not its label wrapper. */
            {button} * {{
                position: static !important;
                transform: none !important;
            }}

            {button} > div,
            {button} [data-testid="stMarkdownContainer"],
            {button} p {{
                display: block !important;
                width: 100% !important;
                min-width: 0 !important;
                box-sizing: border-box !important;
                text-align: left !important;
                margin: 0 !important;
            }}

            /* Number in the centre of the ring. */
            {button} p strong {{
                position: absolute !important;
                right: 0.55rem !important;
                top: 50% !important;
                transform: translateY(-50%) !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;

                width: 2.65rem !important;
                height: 2.65rem !important;
                box-sizing: border-box !important;
                border: none !important;
                border-radius: 50% !important;
                background: transparent !important;

                margin: 0 !important;
                padding: 0 !important;
                float: none !important;

                font-size: 0.78rem !important;
                font-weight: 700 !important;
                font-variant-numeric: tabular-nums;
                line-height: 1 !important;
                white-space: nowrap !important;
                color: inherit !important;
                isolation: isolate;
            }}

            /* Mask out the centre, leaving a coloured progress ring. */
            {button} p strong::before {{
                content: "";
                position: absolute;
                inset: 0;
                border-radius: 50%;
                pointer-events: none;
                background: conic-gradient(
                    {colour} 0deg {angle:.2f}deg,
                    #293137 {angle:.2f}deg 360deg
                );
                -webkit-mask: radial-gradient(
                    farthest-side,
                    transparent calc(100% - 4px),
                    #000 calc(100% - 3.5px)
                );
                mask: radial-gradient(
                    farthest-side,
                    transparent calc(100% - 4px),
                    #000 calc(100% - 3.5px)
                );
            }}
            """
        )

    st.markdown(
        f"""
        <style>
            {sidebar} {{
                width: 4.5rem !important;
                min-width: 4.5rem !important;
                max-width: 4.5rem !important;
                transform: none !important;
                margin-left: 0 !important;
                visibility: visible !important;
                overflow: visible !important;
                z-index: 999999 !important;
            }}

            html body [data-testid="stSidebarCollapseButton"],
            html body [data-testid="stSidebarResizeHandle"] {{
                display: none !important;
            }}

            {sidebar} [data-testid="stSidebarContent"] {{
                position: absolute !important;
                top: 0;
                left: 0;
                height: 100%;
                width: 4.5rem;
                overflow-x: hidden !important;
                background-color: inherit;
                transition: width 0.22s ease, box-shadow 0.22s ease;
            }}

            {sidebar}:hover [data-testid="stSidebarContent"] {{
                width: 17.5rem;
                box-shadow: 8px 0 24px rgba(0, 0, 0, 0.45);
            }}

            {sidebar} .wordmark {{
                display: flex;
                align-items: center;
                gap: 0.65rem;
                white-space: nowrap;
                overflow: hidden;
            }}

            {sidebar} .brand-mark {{
                width: 28px;
                height: 28px;
                flex-shrink: 0;
            }}

            {sidebar}:not(:hover) .wordmark {{
                justify-content: center;
                gap: 0;
            }}

            {sidebar}:not(:hover) .brand-name {{
                display: none;
            }}

            {sidebar} .sidebar-dots {{
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
            }}

            {sidebar}:hover .sidebar-dots {{
                visibility: hidden;
            }}

            {sidebar} .sidebar-section-heading {{
                margin: 0;
                padding: 0 0.85rem;
                font-size: 0.8rem;
                font-weight: 600;
                line-height: 1.5rem;
                text-align: left;
                white-space: nowrap;
                overflow: hidden;
                opacity: 0.7;
            }}

            {sidebar}:not(:hover) .sidebar-section-heading {{
                visibility: hidden;
                opacity: 0;
                transition: none;
            }}

            {sidebar}:hover .sidebar-section-heading {{
                visibility: visible;
                opacity: 0.7;
                transition: opacity 0.1s ease 0.22s;
            }}

            {sidebar} [data-testid="stButton"] button {{
                height: auto !important;
                min-height: 2.75rem !important;
                min-width: 0 !important;
                justify-content: flex-start !important;
                text-align: left !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                padding: 0.45rem 0.85rem !important;
            }}

            {sidebar} [data-testid="stButton"] button > * {{
                flex-shrink: 0 !important;
            }}

            {sidebar} [data-testid="stButton"] button p {{
                margin: 0 !important;
                line-height: 1.25 !important;
                white-space: nowrap !important;
                word-spacing: normal !important;
            }}

            {sidebar} [data-testid="stButton"] button p em {{
                font-style: normal !important;
                font-size: 0.75rem !important;
                color: #8a959d !important;
            }}

            {"".join(astronaut_styles)}

            {sidebar}:not(:hover) [data-testid="stButton"] button * {{
                visibility: hidden !important;
                opacity: 0 !important;
                transition: none !important;
            }}

            {sidebar}:hover [data-testid="stButton"] button * {{
                visibility: visible !important;
                opacity: 1 !important;
                transition: opacity 0.1s ease 0.22s !important;
            }}

            {sidebar}:not(:hover) [data-testid="stButton"] button {{
                padding: 0 !important;
            }}
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
        _nav("home", "⌂   Dashboard")
        st.divider()

        st.markdown(
            '<h2 class="sidebar-section-heading">'
            'Astronaut profiles'
            '</h2>',
            unsafe_allow_html=True,
        )

        for astronaut_id, astronaut in Astronauts.items():
            score = _health_score(astronaut)
            score_label = f"{score:g}%" if score is not None else "n/a"

            _nav(
                astronaut_id,
                f"{astronaut.name} **{score_label}**  \n"
                f"*{astronaut.role}*",
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