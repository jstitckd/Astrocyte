"""Homepage environmental tiles: recorded weather, optional cabin demo and gaps."""
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

from components.environment_charts import history_figure
from services.environment import DEFAULT_DATA_PATH, converted, load_csv, take_snapshot

STYLE_PATH = Path(__file__).resolve().parents[1] / "frontend" / "environment.css"
SOURCE_LABELS = {"csv": "CSV", "demo": "DEMO", "missing": "NOT MEASURED"}


@st.cache_data(show_spinner=False, max_entries=4)
def _load(payload):
    return load_csv(payload)


def _remember_option(field, widget_key, sol=None):
    """Store choices separately from widgets, which Streamlit clears off-page."""
    preferences = dict(st.session_state.environment_preferences)
    if field == "times":
        preferences["times"] = {**preferences["times"], str(sol): st.session_state[widget_key]}
    else:
        preferences[field] = st.session_state[widget_key]
    st.session_state.environment_preferences = preferences


def _badge(reading):
    return f'<span class="env-badge env-badge-{reading.source}" title="{escape(reading.note, quote=True)}">{SOURCE_LABELS[reading.source]}</span>'


def _value(reading, digits=1):
    return "—" if reading.value is None else f"{reading.value:,.{digits}f}"


def _row(label, reading, digits=1):
    badge = '<small class="env-inline-demo">DEMO</small>' if reading.source == "demo" else ""
    return (
        f'<div class="env-reading"><span>{escape(label)} {badge}</span>'
        f'<strong>{_value(reading, digits)} <span>{escape(reading.unit)}</span></strong></div>'
    )


def _number(reading, digits=1):
    return f'<div class="env-value">{_value(reading, digits)}<span>{escape(reading.unit)}</span></div>'


def _temperature_gauge(reading, limits):
    """The testing.py 270-degree ring, rendered in CSS for Streamlit HTML."""
    fraction = 0.0
    if reading.value is not None and limits is not None:
        low, high = limits
        if high > low:
            fraction = max(0.0, min(1.0, (reading.value - low) / (high - low)))
    return (
        '<div class="env-gauge" role="img" '
        f'aria-label="Outside air: {_value(reading)} {escape(reading.unit)}. Arc shows position within this recorded Sol range, not a safety score.">'
        f'<div class="env-gauge-track" style="--env-angle:{270 * fraction:.2f}deg" aria-hidden="true"></div>'
        '<div class="env-gauge-center">'
        f'<span class="env-gauge-value">{_value(reading)}</span>'
        f'<span class="env-gauge-unit">{escape(reading.unit)}</span></div></div>'
    )


def cards_html(snapshot, temperature_unit="°C", pressure_unit="Pa"):
    """Keep source labels adjacent to every synthetic reading."""
    readings = snapshot.readings
    air = converted(readings["air"], temperature_unit, pressure_unit)
    ground = converted(readings["ground"], temperature_unit, pressure_unit)
    cabin_temp = converted(readings["cabin_temp"], temperature_unit, pressure_unit)
    pressure = converted(readings["pressure"], temperature_unit, pressure_unit)
    limits = snapshot.air_range
    if limits is not None and temperature_unit == "°F":
        limits = tuple(value * 9 / 5 + 32 for value in limits)
    range_text = f"Recorded Sol range: {limits[0]:.1f} to {limits[1]:.1f} {air.unit}." if limits else "No air-temperature profile in this file."

    temperature = (
        '<article class="env-card" aria-label="Temperature">'
        f'<div class="env-card-top"><h3>Temperature</h3>{_badge(air)}</div>'
        '<div class="env-scope">Outside air</div>'
        + _temperature_gauge(air, limits)
        + _row("Ground", ground) + _row("Cabin", cabin_temp)
        + f'<p class="env-card-note">{escape(range_text)}</p></article>'
    )
    radiation = (
        '<article class="env-card" aria-label="Radiation exposure and levels">'
        f'<div class="env-card-top"><h3>Radiation</h3>{_badge(readings["cabin_radiation"])}</div>'
        '<div class="env-scope">Cabin dose rate</div>'
        + _number(readings["cabin_radiation"])
        + _row("Outside", readings["surface_radiation"])
        + _row("Accumulated dose", readings["dose_total"], 3)
        + '</article>'
    )
    air_quality = readings["cabin_pm25"]
    air_quality_row = _row("Cabin PM₂.₅", air_quality) if air_quality.value is not None else '<div class="env-monitoring-gap"><span>Air quality</span><strong>Not monitored</strong></div>'
    atmosphere = (
        '<article class="env-card" aria-label="Atmospheric pressure, gas composition and air quality">'
        f'<div class="env-card-top"><h3>Atmosphere</h3>{_badge(pressure)}</div>'
        '<div class="env-scope">Outside pressure</div>' + _number(pressure, 2 if pressure_unit == "mbar" else 1)
        + _row("Cabin pressure", readings["cabin_pressure"])
        + _row("O₂ · cabin", readings["o2"])
        + _row("CO₂ · cabin", readings["co2"], 0)
        + air_quality_row
        + '</article>'
    )
    return '<section class="env-cards" aria-label="Environmental readings">' + temperature + radiation + atmosphere + '</section>'


def render_environment_overview():
    """Show the overview above the map; data failures must not block navigation."""
    st.html(f"<style>{STYLE_PATH.read_text()}</style>")
    try:
        with st.spinner("Loading environmental snapshot…"):
            frame, schema = _load(DEFAULT_DATA_PATH.read_bytes())
    except (OSError, ValueError) as exc:
        st.warning(f"Environmental readings unavailable: {exc}. The habitat map is still available below.")
        return

    with st.container(key="environment_overview"):
        sols = sorted(frame["__sol"].unique().tolist())
        if "environment_preferences" not in st.session_state:
            st.session_state.environment_preferences = {
                "sol": sols[-1], "times": {}, "temperature_unit": "°C",
                "pressure_unit": "Pa", "show_demo": True,
            }
        preferences = st.session_state.environment_preferences
        selected_sol = preferences["sol"] if preferences["sol"] in sols else sols[-1]
        heading, options = st.columns([4, 1], vertical_alignment="center")
        with options:
            with st.popover("View options", icon=":material/tune:", width="stretch"):
                sol = st.selectbox("Recorded Sol", sols, index=sols.index(selected_sol), key="env_sol",
                                   on_change=_remember_option, args=("sol", "env_sol"))
                day = frame.loc[frame["__sol"].eq(sol)]
                times = day["__time"].tolist()
                closest_noon = min(range(len(times)), key=lambda index: abs(float(day.iloc[index]["__hour"]) - 12))
                saved_time = preferences["times"].get(str(sol))
                time_index = times.index(saved_time) if saved_time in times else closest_noon
                time_key = f"env_time_{sol}"
                time = st.selectbox("Observation · LMST", times, index=time_index, key=time_key,
                                    on_change=_remember_option, args=("times", time_key, sol))
                temperature_unit = st.radio("Temperature unit", ["°C", "°F"], horizontal=True, key="env_temperature_unit",
                                            index=["°C", "°F"].index(preferences["temperature_unit"]),
                                            on_change=_remember_option, args=("temperature_unit", "env_temperature_unit"))
                pressure_unit = st.radio("Outside pressure unit", ["Pa", "mbar"], horizontal=True, key="env_pressure_unit",
                                         index=["Pa", "mbar"].index(preferences["pressure_unit"]),
                                         on_change=_remember_option, args=("pressure_unit", "env_pressure_unit"))
                show_demo = st.toggle("Show synthetic cabin readings", value=preferences["show_demo"], key="env_show_demo",
                                      on_change=_remember_option, args=("show_demo", "env_show_demo"))
                st.caption("DEMO values use the cabin scenario from testing.py. Disable it to show only CSV measurements. Missing CSV values stay missing.")
        snapshot = take_snapshot(frame, schema, sol, time, show_demo)
        demo_visible = any(reading.source == "demo" for reading in snapshot.readings.values())
        with heading:
            label = "CSV + CABIN DEMO" if demo_visible else "RECORDED CSV"
            st.html(
                '<div class="env-heading"><div><span class="env-kicker">OUTSIDE &amp; HABITAT</span>'
                '<h2>Environmental overview</h2></div>'
                f'<span class="env-source-pill">{label}</span></div>'
            )
        window = snapshot.time + ("–" + snapshot.end_time if snapshot.end_time else "")
        source_note = "Cabin values are synthetic." if demo_visible else "Only supplied CSV values are shown."
        st.caption(f"Sol {snapshot.sol} · {window} LMST · Local CSV snapshot, not a live feed. {source_note}")
        st.html(cards_html(snapshot, temperature_unit, pressure_unit))

        with st.expander("Recorded trends & data notes"):
            temperature_tab, pressure_tab, sources_tab = st.tabs(["Temperature", "Pressure", "Sources & gaps"])
            accent = st.get_option("theme.primaryColor") or "#d093f6"
            for tab, kind in ((temperature_tab, "temperature"), (pressure_tab, "pressure")):
                with tab:
                    figure = history_figure(frame, schema, snapshot, kind, temperature_unit, pressure_unit, accent)
                    if figure.data:
                        st.plotly_chart(figure, width="stretch", key="env_chart_" + kind, config={"displayModeBar": False})
                    else:
                        st.info("No recorded profile for this measurement in the selected Sol.")
                    st.caption("Recorded full-Sol profile. The dotted marker is your selected observation; gaps remain gaps. No forecast or health threshold is applied.")
            with sources_tab:
                st.write(f"**Weather source:** `{DEFAULT_DATA_PATH.name}`. Values are displayed as supplied by the local file; their origin has not been independently verified.")
                st.write("**Cabin demo:** oxygen, carbon dioxide, pressure, temperature and dose rate use the deterministic `station_values()` formulas from `testing.py`. These vary by Sol, not by observation time. They are not sensors or clinical reference values.")
                st.write("**Monitoring gaps:** no ionising-radiation dosimeter, cabin particulate sensor, dust concentration or regolith-chemistry result is present in the bundled file. Accumulated exposure is not calculated from a single dose-rate value. No toxicity or outdoor-readiness judgement is made.")
                st.dataframe(pd.DataFrame([
                    {"Channel": key, "Value": reading.value, "Unit": reading.unit, "Source": reading.source, "Note": reading.note}
                    for key, reading in snapshot.readings.items()
                ]), hide_index=True, width="stretch")
                st.caption("Background reading: [NASA RAD radiation measurements](https://science.nasa.gov/resource/radiation-measurements-on-mars/) · [NASA Martian dust research](https://www.nasa.gov/missions/mars-2020-perseverance/perseverance-rover/nasas-perseverance-rover-gets-the-dirt-on-mars/). These links explain the topics; they are not the source of the demo numbers.")
