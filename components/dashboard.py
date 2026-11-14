"""Compact homepage cards. Layout styles live in frontend/dashboard.css."""
from html import escape

import streamlit as st


def environmental_cards(snapshot):
    cards = []
    channels = [("cabin_radiation", "Radiation", "◈", 1), ("o2", "Cabin O₂", "◎", 1), ("co2", "Cabin CO₂", "♧", 0), ("cabin_temp", "Temperature", "♨", 1), ("cabin_pressure", "Pressure", "◴", 1)]
    for key, label, icon, digits in channels:
        reading = snapshot.readings[key]
        value = "—" if reading.value is None else f"{reading.value:,.{digits}f}"
        source = {"demo": "Demo", "csv": "Recorded", "missing": "Not measured"}[reading.source]
        cards.append(f'<article class="dash-metric"><div class="dash-metric-top"><span class="dash-icon">{icon}</span>{label}<small>{source}</small></div><div class="dash-number">{value} <span>{escape(reading.unit)}</span></div></article>')
    st.html('<section class="dash-metrics" aria-label="Environmental and cabin readings">' + ''.join(cards) + '</section>')
    air, pressure = snapshot.readings["air"], snapshot.readings["pressure"]
    air_text = "Not measured" if air.value is None else f"{air.value:.1f} °C"
    pressure_text = "Not measured" if pressure.value is None else f"{pressure.value:.0f} Pa"
    st.html(f'<div class="dash-outside"><span class="dash-live-dot"></span> Outside · {air_text} · {pressure_text}<span>Recorded weather · Sol {snapshot.sol} · {escape(snapshot.time)} LMST</span></div>')


def crew_card(crew, tasks):
    name = crew["name"]
    count = sum(task["crew"] == name for task in tasks)
    status = f'{count} task{"s" if count != 1 else ""} due' if count else "Tasks clear"
    tone = "amber" if any(task["crew"] == name and task["urgent"] for task in tasks) else "green"
    st.html(f'''<article class="crew-summary"><div class="crew-top"><h3>{name}</h3><span class="crew-status {tone}">{status}</span></div><div class="crew-body"><div class="crew-ring" style="--score:{crew['sleep_score']};"><div><strong>{crew['sleep_score']}</strong><small>/100</small></div></div><div class="crew-vitals"><span>Heart rate <b>{crew['hr']} bpm</b></span><span>SpO₂ <b>{crew['spo2']:.0f}%</b></span><span>HRV <b>{crew['hrv']:.0f} ms</b></span></div></div><div class="crew-foot">Sleep score · latest recovery record</div></article>''')
    st.button(f"Open {name}'s health →", key=f"summary_{name}", width="stretch", on_click=_open_crew, args=(name,))


def _open_crew(name):
    st.session_state.page = name
