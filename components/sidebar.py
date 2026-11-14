from datetime import date

import streamlit as st

from components.context import ViewContext
from models.areas import AREAS
from models.metrics import CREW_NAMES
from services.demo import demo_readings
from services.ingestion import DataValidationError, filter_readings


@st.cache_data(show_spinner=False)
def _demo():
    return demo_readings()


def go(page):
    st.session_state.page = page


def render_sidebar(store):
    with st.sidebar:
        st.markdown('<div class="wordmark"><span>✳</span> astrocyte<span class="brand-dot">.</span></div><div class="brand-caption">A LITTLE CLOSER TO HOME</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-heading">YOUR MISSION</div>', unsafe_allow_html=True)
        source = st.selectbox("Data source", ["Demo mission", "Imported CSV"], key="source_choice")
        if source == "Imported CSV":
            st.file_uploader("Upload readings", type="csv", key="readings_upload", on_change=_on_upload, args=(store,), help="UTF-8 CSV, up to 5 MB. See Data & exports for the sample and contract.")
            if st.session_state.upload_error:
                st.error(st.session_state.upload_error)
            if st.session_state.imported is not None:
                st.caption(f"Loaded: {st.session_state.imported_filename}. Uploading another file replaces the readings after validation.")
            else:
                st.info("Upload a CSV to begin. The demo remains available under Data source.")
        imported = source == "Imported CSV" and st.session_state.imported is not None
        if source == "Demo mission":
            frame, dataset_id = _demo(), "demo"
        elif imported:
            frame, dataset_id = st.session_state.imported, st.session_state.imported_id
        else:
            frame, dataset_id = _demo().iloc[:0], "no-import"
        crew_ids = sorted(frame.crew_id.unique()) if not frame.empty else ["crew-01"]
        if st.session_state.get("crew_choice") not in crew_ids:
            st.session_state.crew_choice = crew_ids[0]
        crew = st.selectbox("Crew member", crew_ids, key="crew_choice", format_func=lambda value: f"{CREW_NAMES.get(value, value)} · {value}")
        crew_frame = frame[frame.crew_id.eq(crew)]
        minimum = crew_frame.timestamp.min().date() if not crew_frame.empty else date(2026, 11, 1)
        maximum = crew_frame.timestamp.max().date() if not crew_frame.empty else date(2026, 11, 14)
        dates = st.date_input("Reading window · UTC", (minimum, maximum), min_value=minimum, max_value=maximum, key=f"window_{dataset_id}_{crew}", format="DD/MM/YYYY")
        if len(dates) == 2:
            start, end = dates
            filtered = filter_readings(frame, crew, start, end)
        else:
            start = end = dates[0] if dates else minimum
            filtered = frame.iloc[:0].copy()
            st.info("Choose an end date to display your reading window.")
        st.markdown('<div class="sidebar-heading">THE HABITAT</div>', unsafe_allow_html=True)
        _nav("home", "⌂   Base overview")
        for key, area in AREAS.items():
            _nav(key, f"{area.icon}   {area.short_name}")
        st.divider()
        _nav("data", "↧   Data & exports")
        st.caption("SESSION STORAGE\n\nCheck-ins and tasks stay in this browser session. Export before disconnecting or restarting.")
        st.caption("Student prototype · Synthetic demo · No connected sensors")
    return ViewContext(filtered, frame, crew, start, end, dataset_id, store)


def _nav(page, label):
    st.button(label, key="nav_" + page, type="primary" if st.session_state.page == page else "secondary", width="stretch", on_click=go, args=(page,))


def _on_upload(store):
    uploaded = st.session_state.readings_upload
    if uploaded is None:
        return
    try:
        with st.spinner("Validating readings…"):
            store.import_readings(uploaded.getvalue(), uploaded.name)
    except DataValidationError as exc:
        st.session_state.upload_error = str(exc) + (" Your previous import is still loaded." if st.session_state.imported is not None else "")
