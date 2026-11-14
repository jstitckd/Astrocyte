"""Compact homepage cards. Layout styles live in frontend/dashboard.css."""
from html import escape

import streamlit as st
from services.dashboard import complete_task
from services.crew_health import score_colour


def environmental_cards(snapshot):
    cards = []
    channels = [("cabin_radiation", "Radiation", "◈", 1), ("o2", "Cabin O₂", "◎", 1), ("co2", "Cabin CO₂", "♧", 0), ("cabin_temp", "Temperature", "♨", 1), ("cabin_pressure", "Pressure", "◴", 1)]
    for key, label, icon, digits in channels:
        reading = snapshot.readings[key]
        value = "—" if reading.value is None else f"{reading.value:,.{digits}f}"
        source = {"demo": "", "csv": "Recorded", "missing": "Not measured"}[reading.source]
        source_label = f"<small>{source}</small>" if source else ""
        cards.append(f'<article class="dash-metric"><div class="dash-metric-top"><span class="dash-icon">{icon}</span>{label}{source_label}</div><div class="dash-number">{value} <span>{escape(reading.unit)}</span></div></div></article>')
    st.html('<section class="dash-metrics" aria-label="Environmental and cabin readings">' + ''.join(cards) + '</section>')


def crew_card(crew, tasks):
    name = crew["name"]
    assigned = sorted((task for task in tasks if task["crew"] == name), key=lambda task: not task["urgent"])
    count = len(assigned)
    status = f'{count} task{"s" if count != 1 else ""} due' if count else "Tasks clear"
    tone = "amber" if any(task["crew"] == name and task["urgent"] for task in tasks) else "green"
    score = crew["health_score"]
    score_text = f"{score:g}%" if score is not None else "—"
    colour = score_colour(score) if score is not None else "#8a959d"
    gauge = f'<div class="crew-health-gauge" role="img" aria-label="Health score {score_text}" style="--health-colour:{colour};--health-angle:{(score or 0) * 3.6:.2f}deg"><strong>{score_text}</strong></div>'
    with st.container(border=True, key=f"crew_card_{name}"):
        st.html(f'''<article class="crew-summary"><div class="crew-top"><h3>{name}</h3><span class="crew-status {tone}">{status}</span></div><div class="crew-health-row">{gauge}<div class="crew-compact-vitals"><span>Sleep score <b>{crew['sleep_score']}/100</b></span><span>Heart rate <b>{crew['hr']} bpm</b></span><span>SpO₂ <b>{crew['spo2']:.0f}%</b></span><span>HRV <b>{crew['hrv']:.0f} ms</b></span></div></div></article>''')
        if not assigned:
            st.success("All tasks completed.")
        for task in assigned:
            selected = st.session_state.get("selected_habitat_task") == task["id"]
            prefix = "task_selected" if selected else "crew_task"
            with st.container(border=True, key=f"{prefix}_{task['id']}"):
                label, action = st.columns([5, 1], gap="small", vertical_alignment="center")
                with label:
                    st.html(f'<div class="crew-task-line" title="{escape(task["detail"], quote=True)}"><strong>{escape(task["title"])}</strong><span>Due {escape(task["due"])}</span></div>')
                with action:
                    st.button("✓", help="Mark complete", key=f"complete_{task['id']}", on_click=complete_task, args=(task['id'],))
        st.button(f"Open {name}'s health →", key=f"summary_{name}", width="stretch", on_click=_open_crew, args=(name,))


def _open_crew(name):
    st.session_state.page = name
