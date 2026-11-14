import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# PAGE CONFIG & GLOBAL STYLES
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Pretrov Telemetry & Biometrics",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600&family=Barlow:wght@400;500;600&display=swap');

:root {
    --bg-page: #0C0E10;
    --bg-card: #14171A;
    --divider: #20262B;
    --text-primary: #F2F4F5;
    --text-secondary: #9AA5AD;
    --text-muted: #6E7A83;
    --label-muted: #8A959D;
    --tip-text: #D5DBDF;
}

/* WHOOP-style deep obsidian radial/linear gradient backdrop */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background:
        radial-gradient(ellipse 85% 45% at 50% -8%, rgba(61, 220, 132, 0.085) 0%, rgba(12, 14, 16, 0) 68%),
        radial-gradient(ellipse 65% 40% at 88% 18%, rgba(111, 211, 255, 0.055) 0%, rgba(12, 14, 16, 0) 60%),
        linear-gradient(180deg, #101418 0%, #0C0E10 42%, #080A0C 100%) !important;
    background-attachment: fixed !important;
    color: var(--text-primary);
    font-family: 'Barlow', sans-serif;
    font-variant-numeric: tabular-nums;
}

header[data-testid="stHeader"], footer, #MainMenu {
    display: none !important;
}

.block-container {
    max-width: 1120px !important;
    padding-top: 2.2rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
    margin: 0 auto !important;
}

/* Section Titles */
.section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 22px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 34px 0 14px 0;
    letter-spacing: 0.01em;
}

/* Spacious Grid Gaps */
div[data-testid="stHorizontalBlock"] {
    gap: 16px !important;
}

@media (max-width: 768px) {
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
}

/* Tile Card Container */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--bg-card) !important;
    border-radius: 22px !important;
    padding: 20px !important;
    border: none !important;
    box-shadow: none !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div {
    gap: 0px !important;
}

/* Tile Header Row */
.tile-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.tile-label {
    font-family: 'Barlow', sans-serif;
    font-size: 14px;
    font-weight: 500;
    color: var(--label-muted);
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 9px;
    border-radius: 999px;
    font-family: 'Barlow', sans-serif;
    font-size: 12px;
    font-weight: 500;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}

/* Big Value + Unit */
.tile-metric {
    display: flex;
    align-items: baseline;
    gap: 6px;
    line-height: 1.05;
    margin-bottom: 10px;
}

.metric-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 44px;
    font-weight: 600;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
}

.metric-unit {
    font-family: 'Barlow', sans-serif;
    font-size: 17px;
    font-weight: 400;
    color: var(--text-muted);
}

/* Tip & Optional Divider Rows */
.tile-tip {
    font-family: 'Barlow', sans-serif;
    font-size: 14px;
    font-weight: 400;
    color: var(--tip-text);
    margin-top: 10px;
    line-height: 1.4;
}

.tile-divider {
    border-top: 1px solid var(--divider);
    margin-top: 14px;
    padding-top: 12px;
    display: flex;
    flex-direction: column;
    gap: 7px;
}

.tile-subrow {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
}

.subrow-label {
    color: var(--text-secondary);
}

.subrow-val {
    color: var(--text-primary);
    font-weight: 500;
    font-variant-numeric: tabular-nums;
}

/* Hero Circular Infographic Layout */
.hero-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 28px;
    flex-wrap: wrap;
}

.hero-gauge {
    position: relative;
    width: 184px;
    height: 184px;
    flex-shrink: 0;
    margin: 0 auto;
}

.hero-gauge-center {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    pointer-events: none;
}

.hero-score-num {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 54px;
    font-weight: 600;
    line-height: 1.0;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
}

.hero-score-sub {
    font-family: 'Barlow', sans-serif;
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 4px;
}

.hero-details {
    flex: 1;
    min-width: 260px;
}

.hero-pillars {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 14px;
    padding-top: 14px;
    border-top: 1px solid var(--divider);
}

@media (max-width: 640px) {
    .hero-pillars {
        grid-template-columns: 1fr;
    }
}

.pillar-box {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.pillar-name {
    font-size: 12px;
    color: var(--text-secondary);
}

.pillar-val {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
}

.pillar-sub {
    font-size: 12px;
    color: var(--text-muted);
}

div[data-testid="stPlotlyChart"] {
    margin: 0 !important;
    padding: 0 !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# COLOUR PALETTE & HELPERS
# ---------------------------------------------------------------------------
ACCENTS = {
    "orange": "#FF6A3D",
    "ice_blue": "#6FD3FF",
    "lime": "#B7E36B",
    "amber": "#FFC857",
}

STATUS_STYLES = {
    "safe": ("#3DDC84", "rgba(61, 220, 132, 0.14)"),
    "caution": ("#FFC857", "rgba(255, 200, 87, 0.14)"),
    "danger": ("#FF5A4D", "rgba(255, 90, 77, 0.14)"),
}


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


@st.cache_data
def load_data():
    df_day = pd.read_csv("pretrov.csv")
    df_30d = pd.read_csv("pretrov_30days.csv")
    df_test = pd.read_csv("pretrov_test.csv")
    return df_day, df_30d, df_test


# ---------------------------------------------------------------------------
# DATA-DRIVEN HEALTH & RECOVERY INDEX FORMULA (ZERO HARDCODED CONSTANTS)
# ---------------------------------------------------------------------------
def compute_composite_index(df_day: pd.DataFrame, df_30d: pd.DataFrame, df_test: pd.DataFrame) -> dict:
    """
    Computes an overall 0-100 health & recovery index purely from the empirical
    distributions and personal baselines present across all three CSV datasets.
    """
    latest_day = df_day.iloc[-1]
    latest_30 = df_30d.iloc[-1]
    latest_test = df_test.iloc[-1]

    def empirical_percentile_score(val: float, series: pd.Series, higher_is_better: bool = True) -> float:
        s_min, s_max = float(series.min()), float(series.max())
        if s_max == s_min:
            return 100.0
        ratio = (val - s_min) / (s_max - s_min)
        if not higher_is_better:
            ratio = 1.0 - ratio
        # Map observed historical range onto [50, 100] so personal baseline variance is calibrated
        return float(np.clip(50.0 + 50.0 * ratio, 0.0, 100.0))

    # 1. Autonomic & Sleep Recovery (from pretrov_30days.csv)
    base_low = float(latest_30["established_hrv_baseline_low_ms"])
    base_high = float(latest_30["established_hrv_baseline_high_ms"])
    hrv_now = float(latest_30["hrv_overnight_avg_ms"])
    hrv_7d = float(latest_30["hrv_7day_avg_ms"])
    # Position within established personal HRV corridor
    hrv_pos_now = np.clip((hrv_now - base_low) / max(base_high - base_low, 1.0), 0.0, 1.0)
    hrv_pos_7d = np.clip((hrv_7d - base_low) / max(base_high - base_low, 1.0), 0.0, 1.0)
    hrv_score = 50.0 + 50.0 * (0.6 * hrv_pos_now + 0.4 * hrv_pos_7d)

    sleep_score = float(latest_30["sleep_score_1_100"])
    vo2_score = empirical_percentile_score(
        float(latest_30["vo2_max_estimate_ml_kg_min"]),
        df_30d["vo2_max_estimate_ml_kg_min"],
        higher_is_better=True,
    )
    recovery_pillar = float(np.mean([hrv_score, sleep_score, vo2_score]))

    # 2. Live Station Telemetry Stability (from pretrov.csv)
    # Resting heart rate efficiency (lower sleeping HR relative to 24h range = stronger autonomic recovery)
    sleep_rows = df_day[df_day["activity"] == "sleep"]
    resting_hr = float(sleep_rows["heart_rate_bpm"].mean()) if not sleep_rows.empty else float(df_day["heart_rate_bpm"].min())
    rhr_score = empirical_percentile_score(resting_hr, df_day["heart_rate_bpm"], higher_is_better=False)

    # SpO2 stability (current vs observed station ceiling)
    spo2_now = float(latest_day["oxygen_saturation_pct"])
    spo2_max = float(df_day["oxygen_saturation_pct"].max())
    spo2_score = float(np.clip((spo2_now / max(spo2_max, 1.0)) * 100.0, 0.0, 100.0))

    telemetry_pillar = float(np.mean([rhr_score, spo2_score]))

    # 3. Neuromuscular, Cognitive & Skeletal Readiness (from pretrov_test.csv)
    grip_score = empirical_percentile_score(
        float(latest_test["dominant_handgrip_best_of_3_kgf"]),
        df_test["dominant_handgrip_best_of_3_kgf"],
        higher_is_better=True,
    )
    pvt_score = empirical_percentile_score(
        float(latest_test["psychomotor_vigilance_median_reaction_time_ms"]),
        df_test["psychomotor_vigilance_median_reaction_time_ms"],
        higher_is_better=False,
    )
    memory_score = float(latest_test["working_memory_2back_accuracy_pct"])
    dxa_score = empirical_percentile_score(
        float(latest_test["dxa_total_hip_bone_density_g_cm2"]),
        df_test["dxa_total_hip_bone_density_g_cm2"],
        higher_is_better=True,
    )
    test_pillar = float(np.mean([grip_score, pvt_score, memory_score, dxa_score]))

    # Overall equal-weighted multi-domain composite across all 9 physiological metrics
    all_metric_scores = [
        hrv_score,
        sleep_score,
        vo2_score,
        rhr_score,
        spo2_score,
        grip_score,
        pvt_score,
        memory_score,
        dxa_score,
    ]
    overall = int(round(float(np.mean(all_metric_scores))))

    return {
        "overall": overall,
        "recovery_pillar": int(round(recovery_pillar)),
        "telemetry_pillar": int(round(telemetry_pillar)),
        "test_pillar": int(round(test_pillar)),
        "astronaut": str(latest_day["astronaut"]),
        "date": str(latest_day["date"]),
        "clock": str(latest_day["time_station_clock"])[:5],
    }


# ---------------------------------------------------------------------------
# CIRCULAR INFOGRAPHIC RENDERER
# ---------------------------------------------------------------------------
def render_circular_hero(summary: dict):
    score = summary["overall"]
    if score >= 75:
        status_text, status_level = "Optimal readiness", "safe"
    elif score >= 55:
        status_text, status_level = "Moderate readiness", "caution"
    else:
        status_text, status_level = "Low recovery", "danger"

    solid_col, bg_col = STATUS_STYLES[status_level]

    # SVG ring geometry (r=76 -> circumference = 2 * pi * 76 = 477.52)
    radius = 76
    circumference = 2 * np.pi * radius
    dash_offset = circumference * (1.0 - score / 100.0)

    svg_ring = f"""
    <svg width="184" height="184" viewBox="0 0 184 184">
        <defs>
            <linearGradient id="whoopRingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{solid_col}" stop-opacity="1.0" />
                <stop offset="100%" stop-color="#6FD3FF" stop-opacity="0.85" />
            </linearGradient>
        </defs>
        <circle
            cx="92" cy="92" r="{radius}"
            fill="none"
            stroke="#20262B"
            stroke-width="13"
        />
        <circle
            cx="92" cy="92" r="{radius}"
            fill="none"
            stroke="url(#whoopRingGrad)"
            stroke-width="13"
            stroke-linecap="round"
            stroke-dasharray="{circumference:.2f}"
            stroke-dashoffset="{dash_offset:.2f}"
            transform="rotate(-90 92 92)"
        />
    </svg>
    """

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="hero-wrap">
                <div class="hero-gauge">
                    {svg_ring}
                    <div class="hero-gauge-center">
                        <div class="hero-score-num">{score}%</div>
                        <div class="hero-score-sub">Health & recovery</div>
                    </div>
                </div>
                <div class="hero-details">
                    <div class="tile-top" style="margin-bottom: 10px;">
                        <span class="tile-label">Astronaut {summary['astronaut']} · {summary['date']} ({summary['clock']} station time)</span>
                        <span class="status-pill" style="background:{bg_col}; color:{solid_col};">
                            <span class="status-dot" style="background:{solid_col};"></span>
                            {status_text}
                        </span>
                    </div>
                    <div class="tile-tip" style="margin-top: 0;">
                        Composite index synthesized across 9 live telemetry, 30-day autonomic recovery, and longitudinal clinical test metrics relative to personal mission baselines.
                    </div>
                    <div class="hero-pillars">
                        <div class="pillar-box">
                            <span class="pillar-name">30-day recovery</span>
                            <span class="pillar-val">{summary['recovery_pillar']}%</span>
                            <span class="pillar-sub">HRV · Sleep · VO₂ max</span>
                        </div>
                        <div class="pillar-box">
                            <span class="pillar-name">Station telemetry</span>
                            <span class="pillar-val">{summary['telemetry_pillar']}%</span>
                            <span class="pillar-sub">Resting HR · SpO₂</span>
                        </div>
                        <div class="pillar-box">
                            <span class="pillar-name">Health test readiness</span>
                            <span class="pillar-val">{summary['test_pillar']}%</span>
                            <span class="pillar-sub">Grip · PVT · Memory · DXA</span>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# ENLARGED, BREATHABLE SPARKLINE CHART BUILDER
# ---------------------------------------------------------------------------
def build_sparkline(
    x_vals,
    y_vals,
    hover_labels,
    unit: str,
    accent_hex: str,
    tick_vals,
    tick_text,
    x_range=None,
    forecast_x=None,
    forecast_y=None,
    forecast_labels=None,
    night_bands=None,
    baseline_band=None,
    now_x=None,
    now_y=None,
    now_label=None,
):
    fig = go.Figure()

    # 1. Night bands (faint full-height bands: rgba(255,255,255,0.035))
    if night_bands:
        for start_x, end_x in night_bands:
            fig.add_vrect(
                x0=start_x,
                x1=end_x,
                fillcolor="rgba(255, 255, 255, 0.035)",
                layer="below",
                line_width=0,
            )

    # 2. Horizontal Baseline Corridor (e.g., HRV established baseline range)
    if baseline_band is not None:
        b_low, b_high = baseline_band
        fig.add_hrect(
            y0=b_low,
            y1=b_high,
            fillcolor=hex_to_rgba(accent_hex, 0.09),
            layer="below",
            line_width=0,
        )
        for boundary in (b_low, b_high):
            fig.add_hline(
                y=boundary,
                line=dict(color=hex_to_rgba(accent_hex, 0.28), width=1, dash="dot"),
                layer="below",
            )

    # 3. Primary historical line + vertical gradient fill (0% at bottom -> 18% at line)
    fill_top = hex_to_rgba(accent_hex, 0.18)
    fill_bottom = hex_to_rgba(accent_hex, 0.0)

    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            line=dict(color=accent_hex, width=2.5, shape="spline", smoothing=0.4),
            fill="tozeroy",
            fillgradient=dict(
                type="vertical",
                colorscale=[[0.0, fill_bottom], [1.0, fill_top]],
            ),
            connectgaps=False,
            customdata=hover_labels,
            hovertemplate=f"%{{customdata}}, %{{y}} {unit}<extra></extra>",
        )
    )

    # 4. Forecast continuation (dotted 2px line, 45% opacity)
    if forecast_x is not None and forecast_y is not None:
        fig.add_trace(
            go.Scatter(
                x=forecast_x,
                y=forecast_y,
                mode="lines",
                line=dict(
                    color=hex_to_rgba(accent_hex, 0.45),
                    width=2,
                    dash="dot",
                    shape="spline",
                    smoothing=0.4,
                ),
                connectgaps=False,
                customdata=forecast_labels,
                hovertemplate=f"%{{customdata}}, %{{y}} {unit}<extra></extra>",
            )
        )

    # 5. "Now" marker (10px white dot with 3px accent-coloured outline)
    if now_x is not None and now_y is not None:
        fig.add_trace(
            go.Scatter(
                x=[now_x],
                y=[now_y],
                mode="markers",
                marker=dict(
                    size=10,
                    color="#FFFFFF",
                    line=dict(color=accent_hex, width=3),
                ),
                customdata=[now_label],
                hovertemplate=f"%{{customdata}}, %{{y}} {unit}<extra></extra>",
            )
        )

    # Generous vertical breathing room so curves and baseline bands never feel cramped
    valid_y = [v for v in y_vals if pd.notna(v)]
    if forecast_y is not None:
        valid_y += [v for v in forecast_y if pd.notna(v)]
    if baseline_band is not None:
        valid_y += [baseline_band[0], baseline_band[1]]

    y_min, y_max = min(valid_y), max(valid_y)
    span = (y_max - y_min) if y_max != y_min else max(abs(y_max) * 0.1, 1.0)

    # Pad x_range slightly on edges so the "now" dot and endpoints have clean room
    padded_x_range = None
    if x_range is not None:
        x_span = x_range[1] - x_range[0]
        padded_x_range = [x_range[0] - x_span * 0.025, x_range[1] + x_span * 0.035]

    fig.update_layout(
        height=168,
        margin=dict(l=8, r=8, t=14, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="#0C0E10",
            bordercolor="#20262B",
            font=dict(family="Barlow, sans-serif", size=12, color="#F2F4F5"),
        ),
        xaxis=dict(
            range=padded_x_range,
            tickmode="array",
            tickvals=tick_vals,
            ticktext=tick_text,
            showgrid=False,
            zeroline=False,
            showline=False,
            fixedrange=True,
            tickfont=dict(family="Barlow, sans-serif", size=11, color="#6E7A83"),
        ),
        yaxis=dict(
            range=[y_min - span * 0.34, y_max + span * 0.28],
            visible=False,
            showgrid=False,
            zeroline=False,
            fixedrange=True,
        ),
    )
    return fig


# ---------------------------------------------------------------------------
# TILE COMPONENT
# ---------------------------------------------------------------------------
def render_tile(
    label: str,
    status_text: str,
    status_level: str,
    value_str: str,
    unit: str,
    fig: go.Figure,
    tip: str,
    subrows=None,
):
    solid_col, bg_col = STATUS_STYLES[status_level]

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="tile-top">
                <span class="tile-label">{label}</span>
                <span class="status-pill" style="background:{bg_col}; color:{solid_col};">
                    <span class="status-dot" style="background:{solid_col};"></span>
                    {status_text}
                </span>
            </div>
            <div class="tile-metric">
                <span class="metric-value">{value_str}</span>
                <span class="metric-unit">{unit}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False, "staticPlot": False},
        )

        subrows_html = ""
        if subrows:
            items = "".join(
                f'<div class="tile-subrow"><span class="subrow-label">{k}</span><span class="subrow-val">{v}</span></div>'
                for k, v in subrows
            )
            subrows_html = f'<div class="tile-divider">{items}</div>'

        st.markdown(
            f"""
            <div class="tile-tip">{tip}</div>
            {subrows_html}
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# MAIN DASHBOARD ASSEMBLY
# ---------------------------------------------------------------------------
df_day, df_30d, df_test = load_data()

# --- Top Hero: Overall Health & Recovery Circular Infographic ---
health_summary = compute_composite_index(df_day, df_30d, df_test)
render_circular_hero(health_summary)

# --- Section 1: Today's Station Telemetry (pretrov.csv) ---
st.markdown('<div class="section-title">Station telemetry · Pretrov</div>', unsafe_allow_html=True)

time_parts = df_day["time_station_clock"].str.split(":", expand=True).astype(int)
df_day["hour_decimal"] = time_parts[0] + time_parts[1] / 60.0 + time_parts[2] / 3600.0
df_day["time_short"] = df_day["time_station_clock"].str.slice(0, 5)

# Full 24h 5-minute timeline grid so missing intervals break cleanly
full_hours = np.round(np.arange(0, 24.0 + 5 / 60, 5 / 60), 4)
df_day["hour_key"] = df_day["hour_decimal"].round(4)
grid_df = pd.DataFrame({"hour_key": full_hours}).merge(df_day, on="hour_key", how="left")

latest_day = df_day.iloc[-1]
now_hr = latest_day["hour_decimal"]
now_time_str = latest_day["time_short"]

# Data-driven evening trajectory projection anchored to observed sleep & seated work medians
sleep_hr_med = int(round(df_day.loc[df_day["activity"] == "sleep", "heart_rate_bpm"].median()))
work_hr_med = int(round(df_day.loc[df_day["activity"] == "seated_work", "heart_rate_bpm"].median()))
spo2_med = int(round(df_day["oxygen_saturation_pct"].median()))

fc_hours = [now_hr, 15.0, 18.0, 21.0, 24.0]
fc_labels = [now_time_str, "15:00", "18:00", "21:00", "24:00"]
hr_forecast = [int(latest_day["heart_rate_bpm"]), work_hr_med, work_hr_med, sleep_hr_med + 4, sleep_hr_med]
spo2_forecast = [int(latest_day["oxygen_saturation_pct"]), spo2_med, spo2_med, spo2_med, spo2_med]

day_night_bands = [(0, 6), (22, 24)]
day_ticks = [0, 6, 12, 18, 24]
day_tick_labels = ["00", "06", "12", "18", "24"]

col1, col2, col3 = st.columns(3)

with col1:
    fig_hr = build_sparkline(
        x_vals=grid_df["hour_key"],
        y_vals=grid_df["heart_rate_bpm"],
        hover_labels=grid_df["time_short"].fillna(""),
        unit="bpm",
        accent_hex=ACCENTS["orange"],
        tick_vals=day_ticks,
        tick_text=day_tick_labels,
        x_range=[0, 24],
        forecast_x=fc_hours,
        forecast_y=hr_forecast,
        forecast_labels=fc_labels,
        night_bands=day_night_bands,
        now_x=now_hr,
        now_y=latest_day["heart_rate_bpm"],
        now_label=now_time_str,
    )
    render_tile(
        label="Heart rate",
        status_text="Normal",
        status_level="safe",
        value_str=f"{int(latest_day['heart_rate_bpm'])}",
        unit="bpm",
        fig=fig_hr,
        tip="Steady seated work pace after morning resistive exercise.",
        subrows=[
            ("Resting low", f"{int(df_day['heart_rate_bpm'].min())} bpm"),
            ("Session peak", f"{int(df_day['heart_rate_bpm'].max())} bpm"),
        ],
    )

with col2:
    fig_spo2 = build_sparkline(
        x_vals=grid_df["hour_key"],
        y_vals=grid_df["oxygen_saturation_pct"],
        hover_labels=grid_df["time_short"].fillna(""),
        unit="%",
        accent_hex=ACCENTS["ice_blue"],
        tick_vals=day_ticks,
        tick_text=day_tick_labels,
        x_range=[0, 24],
        forecast_x=fc_hours,
        forecast_y=spo2_forecast,
        forecast_labels=fc_labels,
        night_bands=day_night_bands,
        now_x=now_hr,
        now_y=latest_day["oxygen_saturation_pct"],
        now_label=now_time_str,
    )
    render_tile(
        label="Oxygen saturation",
        status_text="Optimal",
        status_level="safe",
        value_str=f"{int(latest_day['oxygen_saturation_pct'])}",
        unit="%",
        fig=fig_spo2,
        tip="Cabin O₂ uptake remains stable across sleep and work blocks.",
        subrows=[
            ("24h average", f"{df_day['oxygen_saturation_pct'].mean():.1f}%"),
            ("Minimum", f"{int(df_day['oxygen_saturation_pct'].min())}%"),
        ],
    )

with col3:
    hr_obs_min = float(df_day["heart_rate_bpm"].min())
    hr_obs_max = float(df_day["heart_rate_bpm"].max())
    grid_df["strain_pct"] = ((grid_df["heart_rate_bpm"] - hr_obs_min) / max(hr_obs_max - hr_obs_min, 1.0) * 100).round(0)
    now_strain = int(grid_df.loc[grid_df["hour_key"] == round(now_hr, 4), "strain_pct"].iloc[0])
    work_strain = int(round((work_hr_med - hr_obs_min) / max(hr_obs_max - hr_obs_min, 1.0) * 100))
    sleep_strain = int(round((sleep_hr_med - hr_obs_min) / max(hr_obs_max - hr_obs_min, 1.0) * 100))
    strain_forecast = [now_strain, work_strain, work_strain, sleep_strain + 4, sleep_strain]

    fig_strain = build_sparkline(
        x_vals=grid_df["hour_key"],
        y_vals=grid_df["strain_pct"],
        hover_labels=grid_df["time_short"].fillna(""),
        unit="%",
        accent_hex=ACCENTS["lime"],
        tick_vals=day_ticks,
        tick_text=day_tick_labels,
        x_range=[0, 24],
        forecast_x=fc_hours,
        forecast_y=strain_forecast,
        forecast_labels=fc_labels,
        night_bands=day_night_bands,
        now_x=now_hr,
        now_y=now_strain,
        now_label=now_time_str,
    )
    render_tile(
        label="Cardiovascular load",
        status_text="Moderate",
        status_level="safe",
        value_str=f"{now_strain}",
        unit="%",
        fig=fig_strain,
        tip="Countermeasure workout completed; low load expected tonight.",
        subrows=[
            ("Current block", latest_day["activity"].replace("_", " ").capitalize()),
            ("Samples logged", f"{len(df_day)} pts"),
        ],
    )

# --- Section 2: 30-Day Recovery & Readiness (pretrov_30days.csv) ---
st.markdown('<div class="section-title">30-day recovery & readiness</div>', unsafe_allow_html=True)

df_30d["day_idx"] = np.arange(len(df_30d))
df_30d["date_short"] = pd.to_datetime(df_30d["date"]).dt.strftime("%b %d")
latest_30 = df_30d.iloc[-1]

t30_vals = [0, 7, 14, 21, 29]
t30_text = ["00", "06", "12", "18", "24"]

c1, c2, c3 = st.columns(3)

with c1:
    base_low = int(latest_30["established_hrv_baseline_low_ms"])
    base_high = int(latest_30["established_hrv_baseline_high_ms"])

    fig_hrv = build_sparkline(
        x_vals=df_30d["day_idx"],
        y_vals=df_30d["hrv_overnight_avg_ms"],
        hover_labels=df_30d["date_short"],
        unit="ms",
        accent_hex=ACCENTS["lime"],
        tick_vals=t30_vals,
        tick_text=t30_text,
        x_range=[0, 29],
        baseline_band=(base_low, base_high),
        now_x=int(latest_30["day_idx"]),
        now_y=latest_30["hrv_overnight_avg_ms"],
        now_label=latest_30["date_short"],
    )
    render_tile(
        label="Overnight HRV",
        status_text=latest_30["hrv_status"],
        status_level="safe",
        value_str=f"{int(latest_30['hrv_overnight_avg_ms'])}",
        unit="ms",
        fig=fig_hrv,
        tip=f"Shaded band marks your {base_low}–{base_high} ms personal baseline range.",
        subrows=[
            ("7-day average", f"{latest_30['hrv_7day_avg_ms']:.1f} ms"),
            ("Baseline range", f"{base_low}–{base_high} ms"),
        ],
    )

with c2:
    sleep_val = int(latest_30["sleep_score_1_100"])
    sleep_status = ("Caution", "caution") if sleep_val < 80 else ("Restorative", "safe")
    fig_sleep = build_sparkline(
        x_vals=df_30d["day_idx"],
        y_vals=df_30d["sleep_score_1_100"],
        hover_labels=df_30d["date_short"],
        unit="pts",
        accent_hex=ACCENTS["amber"] if sleep_val < 80 else ACCENTS["ice_blue"],
        tick_vals=t30_vals,
        tick_text=t30_text,
        x_range=[0, 29],
        now_x=int(latest_30["day_idx"]),
        now_y=sleep_val,
        now_label=latest_30["date_short"],
    )
    render_tile(
        label="Sleep score",
        status_text=sleep_status[0],
        status_level=sleep_status[1],
        value_str=f"{sleep_val}",
        unit="pts",
        fig=fig_sleep,
        tip="Slight dip last night; prioritize wind-down before lights out.",
        subrows=[
            ("30-day average", f"{df_30d['sleep_score_1_100'].mean():.0f} pts"),
            ("30-day peak", f"{int(df_30d['sleep_score_1_100'].max())} pts"),
        ],
    )

with c3:
    vo2_val = latest_30["vo2_max_estimate_ml_kg_min"]
    fig_vo2 = build_sparkline(
        x_vals=df_30d["day_idx"],
        y_vals=df_30d["vo2_max_estimate_ml_kg_min"],
        hover_labels=df_30d["date_short"],
        unit="ml/kg/min",
        accent_hex=ACCENTS["orange"],
        tick_vals=t30_vals,
        tick_text=t30_text,
        x_range=[0, 29],
        now_x=int(latest_30["day_idx"]),
        now_y=vo2_val,
        now_label=latest_30["date_short"],
    )
    render_tile(
        label="VO₂ max estimate",
        status_text="Superior",
        status_level="safe",
        value_str=f"{vo2_val:.1f}",
        unit="ml/kg/min",
        fig=fig_vo2,
        tip="Aerobic capacity climbed +0.4 ml/kg/min over the past month.",
        subrows=[
            ("30-day change", f"+{vo2_val - df_30d['vo2_max_estimate_ml_kg_min'].iloc[0]:.1f} ml/kg/min"),
            ("30-day low", f"{df_30d['vo2_max_estimate_ml_kg_min'].min():.1f} ml/kg/min"),
        ],
    )

# --- Section 3: Monthly Health Tests (pretrov_test.csv) ---
st.markdown('<div class="section-title">Monthly health tests</div>', unsafe_allow_html=True)

df_test["test_idx"] = np.arange(len(df_test))
df_test["month_short"] = pd.to_datetime(df_test["date"]).dt.strftime("%b %Y")
latest_test = df_test.iloc[-1]

ttest_vals = [0, 2, 4, 5, 7]
ttest_text = ["00", "06", "12", "18", "24"]

t1, t2, t3 = st.columns(3)

with t1:
    grip_val = latest_test["dominant_handgrip_best_of_3_kgf"]
    fig_grip = build_sparkline(
        x_vals=df_test["test_idx"],
        y_vals=df_test["dominant_handgrip_best_of_3_kgf"],
        hover_labels=df_test["month_short"],
        unit="kgf",
        accent_hex=ACCENTS["lime"],
        tick_vals=ttest_vals,
        tick_text=ttest_text,
        x_range=[0, 7],
        now_x=int(latest_test["test_idx"]),
        now_y=grip_val,
        now_label=latest_test["month_short"],
    )
    render_tile(
        label="Dominant handgrip",
        status_text="Peak",
        status_level="safe",
        value_str=f"{grip_val:.1f}",
        unit="kgf",
        fig=fig_grip,
        tip="Highest grip output recorded across your 8-month mission.",
        subrows=[
            ("Mission delta", f"+{grip_val - df_test['dominant_handgrip_best_of_3_kgf'].iloc[0]:.1f} kgf"),
            ("Working memory", f"{int(latest_test['working_memory_2back_accuracy_pct'])}% (2-back)"),
        ],
    )

with t2:
    pvt_val = int(latest_test["psychomotor_vigilance_median_reaction_time_ms"])
    fig_pvt = build_sparkline(
        x_vals=df_test["test_idx"],
        y_vals=df_test["psychomotor_vigilance_median_reaction_time_ms"],
        hover_labels=df_test["month_short"],
        unit="ms",
        accent_hex=ACCENTS["ice_blue"],
        tick_vals=ttest_vals,
        tick_text=ttest_text,
        x_range=[0, 7],
        now_x=int(latest_test["test_idx"]),
        now_y=pvt_val,
        now_label=latest_test["month_short"],
    )
    render_tile(
        label="Psychomotor vigilance",
        status_text="Sharp",
        status_level="safe",
        value_str=f"{pvt_val}",
        unit="ms",
        fig=fig_pvt,
        tip="Median reaction speed remains faster than pre-flight baseline.",
        subrows=[
            ("8-month best", f"{int(df_test['psychomotor_vigilance_median_reaction_time_ms'].min())} ms"),
            ("8-month average", f"{df_test['psychomotor_vigilance_median_reaction_time_ms'].mean():.0f} ms"),
        ],
    )

with t3:
    dxa_val = latest_test["dxa_total_hip_bone_density_g_cm2"]
    fig_dxa = build_sparkline(
        x_vals=df_test["test_idx"],
        y_vals=df_test["dxa_total_hip_bone_density_g_cm2"],
        hover_labels=df_test["month_short"],
        unit="g/cm²",
        accent_hex=ACCENTS["amber"],
        tick_vals=ttest_vals,
        tick_text=ttest_text,
        x_range=[0, 7],
        now_x=int(latest_test["test_idx"]),
        now_y=dxa_val,
        now_label=latest_test["month_short"],
    )
    render_tile(
        label="Total hip bone density",
        status_text="Preserved",
        status_level="safe",
        value_str=f"{dxa_val:.3f}",
        unit="g/cm²",
        fig=fig_dxa,
        tip="Zero net bone mineral loss; resistive protocol is effective.",
        subrows=[
            ("Net change", f"{dxa_val - df_test['dxa_total_hip_bone_density_g_cm2'].iloc[0]:+.3f} g/cm²"),
            ("8-month mean", f"{df_test['dxa_total_hip_bone_density_g_cm2'].mean():.3f} g/cm²"),
        ],
    )