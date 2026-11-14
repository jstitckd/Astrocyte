from pathlib import Path

import pandas as pd
import streamlit as st

from models.metrics import METRICS
from services.ingestion import readings_csv


def render_data(context):
    st.markdown('<div class="eyebrow">YOUR DATA / YOUR RECORDS</div>', unsafe_allow_html=True)
    st.title("Bring it in. Take it with you.")
    st.markdown('<div class="subtitle">Import measurements in a shared format. Keep observations separate.<br>Export your session before you disconnect.</div>', unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("### 01 / Import readings")
        st.write("Download the sample, then select **Imported CSV** in the sidebar and upload your file. A valid upload replaces the loaded readings. Invalid uploads leave your last valid import intact.")
        sample = Path(__file__).resolve().parents[1] / "data" / "sample_readings.csv"
        st.download_button("↓ Download sample CSV", sample.read_bytes(), file_name="astrocyte_sample_readings.csv", mime="text/csv", width="stretch")
        st.caption("The sample contains only synthetic data: 3 crew members · 14 days · 462 readings.")
    with right:
        st.markdown("### 02 / Export your work")
        st.download_button("↓ Export filtered readings (CSV)", readings_csv(context.readings), file_name="astrocyte_filtered_readings.csv", mime="text/csv", disabled=context.readings.empty, width="stretch")
        st.caption("Only the selected crew member and UTC date window; includes data-source labels.")
        st.download_button("↓ Export session check-ins & tasks (JSON)", context.store.export_json(), file_name="astrocyte_session.json", mime="application/json", width="stretch")
        st.caption("All crew members and datasets in this browser session, including notes, task dates and custom EVA checklists. Readings are exported separately.")
    st.divider()
    st.markdown("### The shared reading format")
    st.code("timestamp,crew_id,metric,value,unit,data_source\n2026-11-14T08:00:00Z,crew-01,heart_rate,64,bpm,wearable-export", language="csv")
    st.write("Use UTF-8 CSV, up to 5 MB and 50,000 rows. All six columns are required. Timestamps must be ISO 8601; include an offset or `Z`. Timestamps without an offset are interpreted as UTC. Units must match exactly; no automatic conversion is performed.")
    st.dataframe(pd.DataFrame([{"Metric": key, "Label": metric.label, "Unit": metric.unit, "Meaning": metric.meaning} for key, metric in METRICS.items()]), hide_index=True, width="stretch")
    st.caption("Individual measurements are not averaged by this app. Sleep duration belongs to the episode ending on that date. Daily totals allow one value per crew, UTC date and metric; they are not incremental events. Duplicate crew/timestamp/metric rows are rejected even when their sources differ.")
    with st.expander("Inspect readings in the current window"):
        if context.readings.empty:
            st.info("No readings to display. Load a CSV or switch to the demo.")
        else:
            st.dataframe(context.readings, hide_index=True, width="stretch")
    st.markdown("### What is saved?")
    st.info("Session memory only. Readings, check-ins, custom checklists and completed tasks survive navigation and normal Streamlit reruns. A browser refresh, disconnection, new tab or server restart can start a new session and lose them. Nothing is written to disk or shared between users. Export before closing. Session JSON is an archive, not a restore/import format in this prototype.")
    st.markdown("### Future connections")
    st.write("No wearable or live API is connected. Person 2 can implement the `ReadingAdapter.fetch()` interface in `services/adapters.py`; the output passes through the same validator. Keep provider credentials in Streamlit secrets or environment variables.")
