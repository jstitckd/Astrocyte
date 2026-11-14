from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_astronaut_header(
    name: str,
    country_code: str,
    gender: str,
    age: int,
    height_cm: int,
    weight_kg: float,
    health_score: float,
    time_outside: str,
):
    # Color based on health score (1.0 to 10.0 scale)
    if health_score >= 8.0:
        score_color = "#00c853"  # Green
    elif health_score >= 5.0:
        score_color = "#ffb300"  # Amber
    else:
        score_color = "#ff3d00"  # Red

    flag_url = f"https://flagcdn.com/w40/{country_code.lower()}.png"

    header_html = f"""
    <div style="display: flex; align-items: center; flex-wrap: wrap; gap: 48px; padding: 4px 0; font-family: sans-serif;">
        <!-- 1. Name, Flag & Demographics -->
        <div>
            <div style="font-size: 11px; font-weight: 700; letter-spacing: 1.2px; color: #888888; margin-bottom: 4px;">
                Medical Officer
            </div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="font-size: 26px; font-weight: 800; line-height: 1.1; color: #fafafa;">{name}</span>
                <img src="{flag_url}" width="28" style="border-radius: 2px; border: 1px solid #333;" alt="{country_code}">
            </div>
            <div style="display: flex; align-items: center; gap: 14px; font-size: 13px; color: #b0b0b0; font-weight: 500;">
                <span><strong style="color: #888888; font-size: 11px;">SEX:</strong> {gender}</span>
                <span style="color: #444444;">|</span>
                <span><strong style="color: #888888; font-size: 11px;">AGE:</strong> {age} yrs</span>
                <span style="color: #444444;">|</span>
                <span><strong style="color: #888888; font-size: 11px;">HEIGHT:</strong> {height_cm} cm</span>
                <span style="color: #444444;">|</span>
                <span><strong style="color: #888888; font-size: 11px;">WEIGHT:</strong> {weight_kg:.1f} kg</span>
            </div>
        </div>

        <!-- Vertical Divider -->
        <div style="width: 1px; height: 54px; background: #2d3139;"></div>

        <!-- 2. Health Score -->
        <div>
            <div style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #fafafa; opacity: 0.75; margin-bottom: 4px;">
                HEALTH SCORE
            </div>
            <div style="font-size: 36px; font-weight: 400; color: {score_color}; line-height: 1.15;">
                {health_score:.1f}<span style="font-size: 20px; font-weight: 500; color: #888888;"> / 10</span>
            </div>
        </div>

        <!-- 3. Total Time Outside -->
        <div>
            <div style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; color: #fafafa; opacity: 0.75; margin-bottom: 4px;">
                TOTAL TIME OUTSIDE
            </div>
            <div style="font-size: 36px; font-weight: 400; color: #fafafa; line-height: 1.15;">
                {time_outside}
            </div>
        </div>
    </div>
    """

    with st.container(border=True):
        st.html(header_html)

def graphs():
    # ---------------------------------------------------------------------------
    # PAGE CONFIG & GLOBAL STYLES
    # ---------------------------------------------------------------------------
    st.set_page_config(
        page_title="milou telemetry & biometrics",
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

    header[data-testid="stHeader"], footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
    }

    .block-container {
        max-width: 1120px !important;
        padding: 2.2rem 1.25rem 3.5rem 1.25rem !important;
        margin: 0 auto !important;
    }

    /* Section titles */
    .section-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 22px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 34px 0 14px 0;
        letter-spacing: 0.01em;
    }
    .section-sub {
        font-family: 'Barlow', sans-serif;
        font-size: 13px;
        font-weight: 400;
        color: var(--text-muted);
        margin: -8px 0 14px 0;
    }

    /* Grid: 3 across on desktop, 1 column on mobile, equal-height rows */
    div[data-testid="stHorizontalBlock"] {
        gap: 16px !important;
        align-items: stretch !important;
        flex-wrap: wrap !important;
    }
    div[data-testid="stColumn"], div[data-testid="column"] {
        min-width: 260px !important;
    }
    @media (max-width: 768px) {
        div[data-testid="stColumn"], div[data-testid="column"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 100% !important;
        }
    }

    /* Tile card container (keyed containers + legacy selector) */
    [class*="st-key-tile"], [class*="st-key-hero"],
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--bg-card) !important;
        border-radius: 22px !important;
        padding: 20px !important;
        border: none !important;
        box-shadow: none !important;
        overflow: visible !important;
    }
    [class*="st-key-tile"], [class*="st-key-hero"] {
        height: 100%;
    }
    [class*="st-key-tile"] > div, [class*="st-key-hero"] > div,
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        gap: 0 !important;
        overflow: visible !important;
    }
    /* Prevent nested wrappers from double-padding */
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0 !important;
    }

    /* Tile header row */
    .tile-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
        position: relative;
        z-index: 20;
    }
    .tile-label {
        font-size: 14px;
        font-weight: 500;
        color: var(--label-muted);
    }

    /* Info icon & hover popup */
    .info-wrap {
        position: relative;
        display: inline-flex;
        align-items: center;
        cursor: help;
    }
    .info-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        border: 1px solid #454E56;
        color: #8A959D;
        font-size: 11px;
        font-weight: 600;
        line-height: 1;
        transition: border-color 0.15s ease, color 0.15s ease;
    }
    .info-wrap:hover .info-icon {
        border-color: #6FD3FF;
        color: #F2F4F5;
    }
    .info-popup {
        visibility: hidden;
        opacity: 0;
        position: absolute;
        left: 0;
        top: 24px;
        width: 245px;
        background: #0C0E10;
        border: 1px solid #2A3138;
        border-radius: 12px;
        padding: 10px 12px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.72);
        z-index: 9999;
        pointer-events: none;
        transition: opacity 0.15s ease, transform 0.15s ease;
        transform: translateY(-4px);
    }
    .info-wrap:hover .info-popup {
        visibility: visible;
        opacity: 1;
        transform: translateY(0);
    }
    .info-popup-title {
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #6FD3FF;
        margin-bottom: 3px;
    }
    .info-popup-text {
        font-size: 12px;
        font-weight: 400;
        line-height: 1.4;
        color: #D5DBDF;
        white-space: normal;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 500;
        white-space: nowrap;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        display: inline-block;
    }

    /* Primary value */
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
    }
    .metric-unit {
        font-size: 17px;
        font-weight: 400;
        color: var(--text-muted);
    }

    /* Footer */
    .tile-tip {
        font-size: 14px;
        font-weight: 400;
        color: var(--tip-text);
        margin-top: 10px;
        line-height: 1.4;
        min-height: 2.8em;
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
    .subrow-label { color: var(--text-secondary); }
    .subrow-val { color: var(--text-primary); font-weight: 500; }

    /* Hero */
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
    }
    .hero-score-sub {
        font-size: 13px;
        color: var(--text-muted);
        margin-top: 4px;
    }
    .hero-details { flex: 1; min-width: 260px; }
    .hero-pillars {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-top: 16px;
        padding-top: 14px;
        border-top: 1px solid var(--divider);
    }
    @media (max-width: 640px) {
        .hero-pillars { grid-template-columns: 1fr; }
        .hero-wrap { justify-content: center; }
    }
    .pillar-box { display: flex; flex-direction: column; gap: 2px; }
    .pillar-name { font-size: 12px; color: var(--text-secondary); }
    .pillar-val {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 24px;
        font-weight: 600;
        color: var(--text-primary);
    }
    .pillar-bar {
        height: 3px;
        border-radius: 999px;
        background: var(--divider);
        margin: 2px 0 4px 0;
        overflow: hidden;
    }
    .pillar-bar > span { display: block; height: 100%; border-radius: 999px; }
    .pillar-sub { font-size: 12px; color: var(--text-muted); }

    div[data-testid="stPlotlyChart"] { margin: 0 !important; padding: 0 !important; }
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

    def html(markup: str) -> str:
        """Flatten indented HTML so Markdown never mistakes it for a code block."""
        return " ".join(line.strip() for line in markup.strip().splitlines())

    def pick_ticks(n: int, count: int = 5) -> list:
        return sorted(set(int(round(v)) for v in np.linspace(0, n - 1, count)))

    def resolve_csv(filename: str) -> Path:
        data_path = Path("data") / filename
        return data_path if data_path.exists() else Path(filename)

    @st.cache_data
    def load_data():
        df_day = pd.read_csv(resolve_csv("milou.csv"))
        df_30d = pd.read_csv(resolve_csv("milou_30days.csv"))
        df_test = pd.read_csv(resolve_csv("milou_test.csv"))
        df_extra = pd.read_csv(resolve_csv("milou_extra.csv"))
        return df_day, df_30d, df_test, df_extra

    # ---------------------------------------------------------------------------
    # DATA-DRIVEN HEALTH & RECOVERY INDEX (no hardcoded clinical constants)
    # ---------------------------------------------------------------------------
    def compute_composite_index(
        df_day: pd.DataFrame,
        df_30d: pd.DataFrame,
        df_test: pd.DataFrame,
        df_extra: pd.DataFrame,
    ) -> dict:
        latest_day = df_day.iloc[-1]
        latest_30 = df_30d.iloc[-1]
        latest_test = df_test.iloc[-1]
        latest_extra = df_extra.iloc[-1]

        def empirical_percentile_score(val: float, series: pd.Series, higher_is_better: bool = True) -> float:
            s_min, s_max = float(series.min()), float(series.max())
            if s_max == s_min:
                return 100.0
            ratio = (val - s_min) / (s_max - s_min)
            if not higher_is_better:
                ratio = 1.0 - ratio
            return float(np.clip(50.0 + 50.0 * ratio, 0.0, 100.0))

        # 1. Recovery (30-day file)
        base_low = float(latest_30["established_hrv_baseline_low_ms"])
        base_high = float(latest_30["established_hrv_baseline_high_ms"])
        hrv_now = float(latest_30["hrv_overnight_avg_ms"])
        hrv_7d = float(latest_30["hrv_7day_avg_ms"])
        width = max(base_high - base_low, 1.0)
        hrv_pos_now = np.clip((hrv_now - base_low) / width, 0.0, 1.0)
        hrv_pos_7d = np.clip((hrv_7d - base_low) / width, 0.0, 1.0)
        hrv_score = 50.0 + 50.0 * (0.6 * hrv_pos_now + 0.4 * hrv_pos_7d)

        sleep_score = float(latest_30["sleep_score_1_100"])
        vo2_score = empirical_percentile_score(
            float(latest_30["vo2_max_estimate_ml_kg_min"]), df_30d["vo2_max_estimate_ml_kg_min"], True
        )
        recovery_pillar = float(np.mean([hrv_score, sleep_score, vo2_score]))

        # 2. Live telemetry (daily file)
        sleep_rows = df_day[df_day["activity"] == "sleep"]
        resting_hr = float(sleep_rows["heart_rate_bpm"].mean()) if not sleep_rows.empty else float(df_day["heart_rate_bpm"].min())
        rhr_score = empirical_percentile_score(resting_hr, df_day["heart_rate_bpm"], False)

        spo2_now = float(latest_day["oxygen_saturation_pct"])
        spo2_max = float(df_day["oxygen_saturation_pct"].max())
        spo2_score = float(np.clip((spo2_now / max(spo2_max, 1.0)) * 100.0, 0.0, 100.0))
        telemetry_pillar = float(np.mean([rhr_score, spo2_score]))

        # 3. Monthly tests & strength metrics
        grip_score = empirical_percentile_score(
            float(latest_test["dominant_handgrip_best_of_3_kgf"]), df_test["dominant_handgrip_best_of_3_kgf"], True
        )
        pvt_score = empirical_percentile_score(
            float(latest_test["psychomotor_vigilance_median_reaction_time_ms"]),
            df_test["psychomotor_vigilance_median_reaction_time_ms"],
            False,
        )
        memory_score = float(latest_test["working_memory_2back_accuracy_pct"])
        dxa_score = empirical_percentile_score(
            float(latest_test["dxa_total_hip_bone_density_g_cm2"]), df_test["dxa_total_hip_bone_density_g_cm2"], True
        )
        imtp_score = empirical_percentile_score(
            float(latest_extra["isometric_mid_thigh_pull_peak_force_best_of_3_n"]),
            df_extra["isometric_mid_thigh_pull_peak_force_best_of_3_n"],
            True,
        )
        leg_press_score = empirical_percentile_score(
            float(latest_extra["seated_leg_press_1rm_kg"]),
            df_extra["seated_leg_press_1rm_kg"],
            True,
        )
        chest_score = empirical_percentile_score(
            float(latest_extra["chest_cable_isometric_peak_force_best_of_3_n"]),
            df_extra["chest_cable_isometric_peak_force_best_of_3_n"],
            True,
        )
        row_score = empirical_percentile_score(
            float(latest_extra["row_cable_isometric_peak_force_best_of_3_n"]),
            df_extra["row_cable_isometric_peak_force_best_of_3_n"],
            True,
        )

        test_pillar = float(np.mean([
            grip_score, pvt_score, memory_score, dxa_score,
            imtp_score, leg_press_score, chest_score, row_score,
        ]))

        overall = int(round(float(np.mean([
            hrv_score, sleep_score, vo2_score, rhr_score, spo2_score,
            grip_score, pvt_score, memory_score, dxa_score,
            imtp_score, leg_press_score, chest_score, row_score,
        ]))))

        return {
            "overall": overall,
            "recovery_pillar": int(round(recovery_pillar)),
            "telemetry_pillar": int(round(telemetry_pillar)),
            "test_pillar": int(round(test_pillar)),
            "astronaut": str(latest_day["astronaut"]),
            "date": str(latest_day["date"]),
            "clock": str(latest_day["time_station_clock"])[:5],
        }

    def level_for_score(score: float) -> str:
        if score >= 75:
            return "safe"
        if score >= 55:
            return "caution"
        return "danger"

    # ---------------------------------------------------------------------------
    # HERO RING
    # ---------------------------------------------------------------------------
    def render_circular_hero(summary: dict):
        score = summary["overall"]
        level = level_for_score(score)
        status_text = {"safe": "Optimal readiness", "caution": "Moderate readiness", "danger": "Low recovery"}[level]
        solid_col, bg_col = STATUS_STYLES[level]

        radius = 76
        circumference = 2 * np.pi * radius
        dash_offset = circumference * (1.0 - score / 100.0)

        svg_ring = f"""
        <svg width="184" height="184" viewBox="0 0 184 184" role="img" aria-label="Health and recovery score {score} percent">
            <defs>
                <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="{solid_col}" stop-opacity="1.0" />
                    <stop offset="100%" stop-color="#6FD3FF" stop-opacity="0.85" />
                </linearGradient>
            </defs>
            <circle cx="92" cy="92" r="{radius}" fill="none" stroke="#20262B" stroke-width="13" />
            <circle cx="92" cy="92" r="{radius}" fill="none" stroke="url(#ringGrad)" stroke-width="13"
                stroke-linecap="round" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{dash_offset:.2f}"
                transform="rotate(-90 92 92)" />
        </svg>
        """

        def pillar(name, value, sub):
            col = STATUS_STYLES[level_for_score(value)][0]
            return f"""
            <div class="pillar-box">
                <span class="pillar-name">{name}</span>
                <span class="pillar-val">{value}%</span>
                <div class="pillar-bar"><span style="width:{value}%; background:{col};"></span></div>
                <span class="pillar-sub">{sub}</span>
            </div>
            """

        with st.container(border=True, key="hero"):
            st.markdown(
                html(f"""
                <div class="hero-wrap">
                    <div class="hero-gauge">
                        {svg_ring}
                        <div class="hero-gauge-center">
                            <div class="hero-score-num">{score}%</div>
                            <div class="hero-score-sub">Health and recovery</div>
                        </div>
                    </div>
                    <div class="hero-details">
                        <div class="tile-top" style="margin-bottom: 10px;">
                            <span class="status-pill" style="background:{bg_col}; color:{solid_col};">
                                <span class="status-dot" style="background:{solid_col};"></span>{status_text}
                            </span>
                        </div>
                        <div class="hero-pillars">
                            {pillar("30-day recovery", summary['recovery_pillar'], "HRV · sleep · VO₂ max")}
                            {pillar("Station telemetry", summary['telemetry_pillar'], "Resting HR · SpO₂")}
                            {pillar("Health test readiness", summary['test_pillar'], "Grip · PVT · DXA · Strength")}
                        </div>
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )

    # ---------------------------------------------------------------------------
    # SPARKLINE BUILDER
    # ---------------------------------------------------------------------------
    def build_sparkline(
        x_vals, y_vals, hover_labels, unit, accent_hex, tick_vals, tick_text, x_range=None,
        forecast_x=None, forecast_y=None, forecast_labels=None, night_bands=None,
        baseline_band=None, now_x=None, now_y=None, now_label=None,
    ):
        fig = go.Figure()

        valid_y = [float(v) for v in y_vals if pd.notna(v)]
        if forecast_y is not None:
            valid_y += [float(v) for v in forecast_y if pd.notna(v)]
        if baseline_band is not None:
            valid_y += [float(baseline_band[0]), float(baseline_band[1])]
        y_min, y_max = min(valid_y), max(valid_y)
        span = (y_max - y_min) if y_max != y_min else max(abs(y_max) * 0.1, 1.0)
        y_floor = y_min - span * 0.34
        y_ceil = y_max + span * 0.28

        if night_bands:
            for start_x, end_x in night_bands:
                fig.add_vrect(x0=start_x, x1=end_x, fillcolor="rgba(255, 255, 255, 0.035)", layer="below", line_width=0)

        if baseline_band is not None:
            b_low, b_high = baseline_band
            fig.add_hrect(y0=b_low, y1=b_high, fillcolor=hex_to_rgba(accent_hex, 0.09), layer="below", line_width=0)
            for boundary in (b_low, b_high):
                fig.add_hline(y=boundary, line=dict(color=hex_to_rgba(accent_hex, 0.28), width=1, dash="dot"), layer="below")

        fig.add_trace(
            go.Scatter(
                x=x_vals, y=[y_floor] * len(x_vals), mode="lines",
                line=dict(width=0, color="rgba(0,0,0,0)"), hoverinfo="skip", showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x_vals, y=y_vals, mode="lines",
                line=dict(color=accent_hex, width=2.5, shape="spline", smoothing=0.4),
                fill="tonexty",
                fillgradient=dict(
                    type="vertical", start=y_floor, stop=y_max,
                    colorscale=[[0.0, hex_to_rgba(accent_hex, 0.0)], [1.0, hex_to_rgba(accent_hex, 0.18)]],
                ),
                connectgaps=False,
                customdata=hover_labels,
                hovertemplate=f"%{{customdata}}, %{{y}} {unit}<extra></extra>",
            )
        )

        if forecast_x is not None and forecast_y is not None:
            fig.add_trace(
                go.Scatter(
                    x=forecast_x, y=forecast_y, mode="lines",
                    line=dict(color=hex_to_rgba(accent_hex, 0.45), width=2, dash="dot", shape="spline", smoothing=0.4),
                    connectgaps=False, customdata=forecast_labels,
                    hovertemplate=f"%{{customdata}}, %{{y}} {unit}<extra></extra>",
                )
            )

        if now_x is not None and now_y is not None:
            fig.add_trace(
                go.Scatter(
                    x=[now_x], y=[now_y], mode="markers",
                    marker=dict(size=10, color="#FFFFFF", line=dict(color=accent_hex, width=3)),
                    customdata=[now_label],
                    hovertemplate=f"%{{customdata}}, %{{y}} {unit}<extra></extra>",
                )
            )

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
            hoverdistance=40,
            hoverlabel=dict(
                bgcolor="#0C0E10", bordercolor="#20262B",
                font=dict(family="Barlow, sans-serif", size=12, color="#F2F4F5"),
            ),
            xaxis=dict(
                range=padded_x_range, tickmode="array", tickvals=tick_vals, ticktext=tick_text,
                showgrid=False, zeroline=False, showline=False, fixedrange=True,
                tickfont=dict(family="Barlow, sans-serif", size=11, color="#6E7A83"),
            ),
            yaxis=dict(range=[y_floor, y_ceil], visible=False, showgrid=False, zeroline=False, fixedrange=True),
        )
        return fig

    # ---------------------------------------------------------------------------
    # TILE
    # ---------------------------------------------------------------------------
    def render_tile(label, status_text, status_level, value_str, unit, fig, tip, subrows=None, measures="", why=""):
        solid_col, bg_col = STATUS_STYLES[status_level]
        key = "tile_" + "".join(c if c.isalnum() else "_" for c in label.lower())

        info_html = ""
        if measures or why:
            info_html = f"""
            <span class="info-wrap">
                <span class="info-icon">i</span>
                <div class="info-popup">
                    <div class="info-popup-title">What it measures</div>
                    <div class="info-popup-text" style="margin-bottom: 6px;">{measures}</div>
                    <div class="info-popup-title">Why it matters</div>
                    <div class="info-popup-text">{why}</div>
                </div>
            </span>
            """

        with st.container(border=True, key=key):
            st.markdown(
                html(f"""
                <div class="tile-top">
                    <div style="display: inline-flex; align-items: center; gap: 7px;">
                        <span class="tile-label">{label}</span>
                        {info_html}
                    </div>
                    <span class="status-pill" style="background:{bg_col}; color:{solid_col};">
                        <span class="status-dot" style="background:{solid_col};"></span>{status_text}
                    </span>
                </div>
                <div class="tile-metric">
                    <span class="metric-value">{value_str}</span>
                    <span class="metric-unit">{unit}</span>
                </div>
                """),
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "staticPlot": False})

            subrows_html = ""
            if subrows:
                items = "".join(
                    f'<div class="tile-subrow"><span class="subrow-label">{k}</span><span class="subrow-val">{v}</span></div>'
                    for k, v in subrows
                )
                subrows_html = f'<div class="tile-divider">{items}</div>'

            st.markdown(html(f'<div class="tile-tip">{tip}</div>{subrows_html}'), unsafe_allow_html=True)

    # ---------------------------------------------------------------------------
    # MAIN
    # ---------------------------------------------------------------------------
    df_day, df_30d, df_test, df_extra = [d.copy() for d in load_data()]

    health_summary = compute_composite_index(df_day, df_30d, df_test, df_extra)
    render_circular_hero(health_summary)

    # --- Section 1: live telemetry ---------------------------------------------
    st.markdown('<div class="section-title">Live telemetry</div>', unsafe_allow_html=True)

    time_parts = df_day["time_station_clock"].str.split(":", expand=True).astype(int)
    df_day["hour_decimal"] = time_parts[0] + time_parts[1] / 60.0 + time_parts[2] / 3600.0
    df_day["time_short"] = df_day["time_station_clock"].str.slice(0, 5)

    full_hours = np.round(np.arange(0, 24.0 + 5 / 60, 5 / 60), 4)
    df_day["hour_key"] = df_day["hour_decimal"].round(4)
    grid_df = pd.DataFrame({"hour_key": full_hours}).merge(df_day, on="hour_key", how="left")

    latest_day = df_day.iloc[-1]
    now_hr = float(latest_day["hour_decimal"])
    now_time_str = latest_day["time_short"]

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

    hr_obs_min = float(df_day["heart_rate_bpm"].min())
    hr_obs_max = float(df_day["heart_rate_bpm"].max())
    hr_range = max(hr_obs_max - hr_obs_min, 1.0)

    def to_strain(hr):
        return (hr - hr_obs_min) / hr_range * 100.0

    col1, col2, col3 = st.columns(3)

    with col1:
        hr_now = int(latest_day["heart_rate_bpm"])
        hr_pct = to_strain(hr_now)
        hr_level, hr_text = (("safe", "Normal") if hr_pct < 70 else ("caution", "Elevated") if hr_pct < 85 else ("danger", "High"))
        activity = str(latest_day["activity"]).replace("_", " ")
        fig_hr = build_sparkline(
            x_vals=grid_df["hour_key"], y_vals=grid_df["heart_rate_bpm"], hover_labels=grid_df["time_short"].fillna(""),
            unit="bpm", accent_hex=ACCENTS["orange"], tick_vals=day_ticks, tick_text=day_tick_labels, x_range=[0, 24],
            forecast_x=fc_hours, forecast_y=hr_forecast, forecast_labels=fc_labels, night_bands=day_night_bands,
            now_x=now_hr, now_y=hr_now, now_label=now_time_str,
        )
        render_tile(
            "Heart rate", hr_text, hr_level, f"{hr_now}", "bpm", fig_hr,
            f"Currently {activity}; evening settles toward about {sleep_hr_med} bpm overnight.",
            subrows=[("Resting low", f"{int(hr_obs_min)} bpm"), ("Session peak", f"{int(hr_obs_max)} bpm")],
            measures="Continuous beats per minute across sleep, station tasks, and EVA blocks.",
            why="Flags acute physical exertion, dehydration, or cardiovascular deconditioning in reduced gravity.",
        )

    with col2:
        spo2_now = int(latest_day["oxygen_saturation_pct"])
        spo2_min = int(df_day["oxygen_saturation_pct"].min())
        spo2_level, spo2_text = (("safe", "Optimal") if spo2_now >= 95 else ("caution", "Low") if spo2_now >= 92 else ("danger", "Very low"))
        fig_spo2 = build_sparkline(
            x_vals=grid_df["hour_key"], y_vals=grid_df["oxygen_saturation_pct"], hover_labels=grid_df["time_short"].fillna(""),
            unit="%", accent_hex=ACCENTS["ice_blue"], tick_vals=day_ticks, tick_text=day_tick_labels, x_range=[0, 24],
            forecast_x=fc_hours, forecast_y=spo2_forecast, forecast_labels=fc_labels, night_bands=day_night_bands,
            now_x=now_hr, now_y=spo2_now, now_label=now_time_str,
        )
        render_tile(
            "Oxygen saturation", spo2_text, spo2_level, f"{spo2_now}", "%", fig_spo2,
            f"Lowest reading today was {spo2_min}%, across sleep and work blocks.",
            subrows=[("24h average", f"{df_day['oxygen_saturation_pct'].mean():.1f}%"), ("Minimum", f"{spo2_min}%")],
            measures="Percentage of oxygen-saturated hemoglobin in arterial blood (SpO₂).",
            why="Provides early warning of cabin air-scrubber faults, suit pressure drops, or respiratory hypoxia.",
        )

    with col3:
        grid_df["strain_pct"] = to_strain(grid_df["heart_rate_bpm"]).round(0)
        now_strain = int(round(to_strain(float(latest_day["heart_rate_bpm"]))))
        work_strain = int(round(to_strain(work_hr_med)))
        sleep_strain = int(round(to_strain(sleep_hr_med)))
        strain_forecast = [now_strain, work_strain, work_strain, sleep_strain + 4, sleep_strain]
        st_level, st_text = (("safe", "Low") if now_strain < 40 else ("safe", "Moderate") if now_strain < 70 else ("caution", "High"))
        fig_strain = build_sparkline(
            x_vals=grid_df["hour_key"], y_vals=grid_df["strain_pct"], hover_labels=grid_df["time_short"].fillna(""),
            unit="%", accent_hex=ACCENTS["lime"], tick_vals=day_ticks, tick_text=day_tick_labels, x_range=[0, 24],
            forecast_x=fc_hours, forecast_y=strain_forecast, forecast_labels=fc_labels, night_bands=day_night_bands,
            now_x=now_hr, now_y=now_strain, now_label=now_time_str,
        )
        render_tile(
            "Cardiovascular load", st_text, st_level, f"{now_strain}", "%", fig_strain,
            "Share of today's heart-rate range; projected to ease into the evening.",
            subrows=[("Current block", activity.capitalize()), ("Samples logged", f"{len(df_day)} pts")],
            measures="Normalized cardiac effort relative to the astronaut's 24-hour resting-to-peak heart-rate range.",
            why="Tracks cumulative metabolic workload so flight surgeons can prevent overexertion before EVA shifts.",
        )

    # --- Section 5: menstrual cycle (milou_menstrual_cycle.csv) ----------------
    # PASTE THIS BLOCK inside graphs(), directly above the final
    # `return round(health_summary["overall"] / 10.0, 1)` line.

    PHASES = {
        "menstrual": ("Menstrual", "#FF5A4D"),
        "follicular": ("Follicular", "#6FD3FF"),
        "ovulatory": ("Ovulatory", "#FFC857"),
        "luteal": ("Luteal", "#B7E36B"),
        "late_luteal": ("Late luteal", "#A78BFA"),
    }
    FLOW_LEVEL = {"none": 0, "spotting": 1, "light": 2, "moderate": 3, "heavy": 4}
    LH_LEVEL = {"negative": 0, "high": 1, "peak": 2}

    CYCLE_CSS = """
    <style>
    .phase-legend { display: flex; flex-wrap: wrap; gap: 6px 16px; margin-top: 16px; }
    .phase-chip { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-secondary); }
    .phase-chip i { width: 8px; height: 8px; border-radius: 50%; background: var(--c); display: inline-block; }

    .cy-grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 8px; margin-top: 6px; }
    @media (max-width: 900px) { .cy-grid { grid-template-columns: repeat(6, 1fr); } }
    @media (max-width: 520px) { .cy-grid { grid-template-columns: repeat(4, 1fr); } }
    .cy-cell {
        background: #0F1215; border-radius: 12px; border-top: 3px solid var(--ph);
        padding: 8px 9px 7px 9px; display: flex; flex-direction: column; gap: 1px; min-width: 0;
        transition: transform 0.12s ease, background 0.12s ease; cursor: default;
    }
    .cy-cell:hover { background: #181C20; transform: translateY(-2px); }
    .cy-cell.cy-today { outline: 1.5px solid #F2F4F5; outline-offset: -1px; background: #181C20; }
    .cy-date { font-size: 11px; color: var(--text-muted); }
    .cy-day { font-family: 'Barlow Condensed', sans-serif; font-size: 22px; font-weight: 600; color: var(--text-primary); line-height: 1.1; }
    .cy-day small { font-family: 'Barlow', sans-serif; font-size: 11px; font-weight: 400; color: var(--text-muted); margin-right: 1px; }
    .cy-marks { display: flex; align-items: center; gap: 3px; height: 10px; margin-top: 4px; }
    .cy-flow { width: 6px; height: 6px; border-radius: 50%; background: #FF5A4D; display: inline-block; }
    .cy-lh { width: 7px; height: 7px; background: #FFC857; transform: rotate(45deg); box-sizing: border-box; display: inline-block; margin: 0 2px; }
    .cy-lh.hollow { background: transparent; border: 1.5px solid #FFC857; }
    .cy-sym { width: 6px; height: 6px; border-radius: 2px; background: #F2F4F5; display: inline-block; }
    .cy-legend { display: flex; flex-wrap: wrap; gap: 8px 18px; margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--divider); }
    .cy-legend span { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-secondary); }
    </style>
    """
    st.markdown(CYCLE_CSS, unsafe_allow_html=True)

    @st.cache_data
    def load_cycle():
        return pd.read_csv(resolve_csv("milou_menstrual_cycle.csv"))

    def fmt_d(ts) -> str:
        return f"{ts.strftime('%b')} {ts.day}"

    def phase_info(key: str):
        return PHASES.get(key, (str(key).replace("_", " ").capitalize(), "#6E7A83"))

    def pretty_symptom(s: str) -> str:
        return s.replace("mild_", "").replace("_", " ")

    def arc_path(cx: float, cy: float, r: float, a0: float, a1: float) -> str:
        """SVG arc between two angles (degrees, 0 = top, clockwise)."""
        def pt(a):
            rad = np.radians(a - 90.0)
            return cx + r * np.cos(rad), cy + r * np.sin(rad)
        x0, y0 = pt(a0)
        x1, y1 = pt(a1)
        large = 1 if (a1 - a0) > 180 else 0
        return f"M {x0:.2f} {y0:.2f} A {r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}"

    # ---- data prep ------------------------------------------------------------
    df_cy = load_cycle().copy()
    df_cy["date_dt"] = pd.to_datetime(df_cy["date"], format="%m/%d/%Y")
    df_cy = df_cy.sort_values("date_dt").reset_index(drop=True)
    df_cy["idx"] = np.arange(len(df_cy))
    df_cy["date_short"] = df_cy["date_dt"].apply(fmt_d)
    df_cy["flow_lvl"] = df_cy["menstrual_flow"].map(FLOW_LEVEL).fillna(0).astype(int)
    df_cy["lh_lvl"] = df_cy["ovulation_lh_test"].map(LH_LEVEL).fillna(0).astype(int)
    df_cy["symptom_raw"] = df_cy["reported_symptoms"].fillna("none").astype(str)
    df_cy["symptom_list"] = df_cy["symptom_raw"].apply(lambda s: [x for x in s.split(";") if x and x != "none"])
    df_cy["symptom_n"] = df_cy["symptom_list"].apply(len)
    n_cy = len(df_cy)

    cur = df_cy.iloc[-1]
    cur_date = cur["date_dt"]
    cur_cycle = int(cur["cycle_number"])
    cur_day = int(cur["cycle_day"])
    cur_phase_name, cur_phase_col = phase_info(str(cur["cycle_phase"]))

    cyc = df_cy[df_cy["cycle_number"] == cur_cycle]
    prev = df_cy[df_cy["cycle_number"] < cur_cycle]
    cycle_len = int(prev["cycle_day"].max()) if not prev.empty else 28
    cycle_len = max(cycle_len, cur_day)
    cycle_start = cur_date - pd.Timedelta(days=cur_day - 1)
    next_period = cycle_start + pd.Timedelta(days=cycle_len)
    days_to_next = max((next_period - cur_date).days, 0)

    # ovulation / temperature shift
    peak_rows = cyc[cyc["ovulation_lh_test"] == "peak"]
    ovu = peak_rows.iloc[0] if not peak_rows.empty else None
    fol_t = cyc.loc[cyc["cycle_phase"] == "follicular", "basal_body_temp_c"].astype(float)
    coverline = float(fol_t.max()) + 0.05 if not fol_t.empty else None
    post = cyc[cyc["idx"] > ovu["idx"]] if ovu is not None else cyc.iloc[0:0]
    fol_mean = float(fol_t.mean()) if not fol_t.empty else None
    post_mean = float(post["basal_body_temp_c"].mean()) if not post.empty else None
    shift = (post_mean - fol_mean) if (fol_mean is not None and post_mean is not None) else None
    days_above = int((post["basal_body_temp_c"] > coverline).sum()) if (coverline is not None and not post.empty) else 0
    ovu_confirmed = ovu is not None and days_above >= 3

    if ovu is not None:
        fw_start = ovu["date_dt"] - pd.Timedelta(days=5)
        fw_end = ovu["date_dt"] + pd.Timedelta(days=1)
        fertile_txt = "Open" if fw_start <= cur_date <= fw_end else ("Closed" if cur_date > fw_end else "Upcoming")
        fw_range = f"{fmt_d(fw_start)} – {fmt_d(fw_end)}"
    else:
        fertile_txt, fw_range = "Not detected", ""

    st.markdown('<div class="section-title">Menstrual cycle</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-sub">Cycle {cur_cycle} · day {cur_day} of {cycle_len} · {cur_phase_name.lower()} phase</div>',
        unsafe_allow_html=True,
    )

    # ---- hero: phase ring + key milestones --------------------------------------
    prev_phase = {int(r.cycle_day): r.cycle_phase for r in prev.itertuples()}
    cur_phase_map = {int(r.cycle_day): r.cycle_phase for r in cyc.itertuples()}
    seg_deg = 360.0 / cycle_len
    seg_gap = 3.0
    segs = []
    for d in range(1, cycle_len + 1):
        observed = d in cur_phase_map
        ph = cur_phase_map.get(d, prev_phase.get(d, "luteal"))
        col = phase_info(str(ph))[1]
        a0, a1 = (d - 1) * seg_deg + seg_gap / 2, d * seg_deg - seg_gap / 2
        segs.append(
            f'<path d="{arc_path(92, 92, 76, a0, a1)}" fill="none" stroke="{col}" stroke-width="12" '
            f'stroke-opacity="{1.0 if observed else 0.26}" />'
        )
    mid = np.radians((cur_day - 0.5) * seg_deg - 90.0)
    mx, my = 92 + 76 * np.cos(mid), 92 + 76 * np.sin(mid)
    ring_svg = (
        f'<svg width="184" height="184" viewBox="0 0 184 184" role="img" aria-label="Cycle day {cur_day} of {cycle_len}">'
        + "".join(segs)
        + f'<circle cx="{mx:.2f}" cy="{my:.2f}" r="8" fill="#FFFFFF" stroke="{cur_phase_col}" stroke-width="3" />'
        + "</svg>"
    )

    def cy_pillar(name, value, sub, pct, col):
        return (
            f'<div class="pillar-box"><span class="pillar-name">{name}</span>'
            f'<span class="pillar-val">{value}</span>'
            f'<div class="pillar-bar"><span style="width:{pct:.0f}%; background:{col};"></span></div>'
            f'<span class="pillar-sub">{sub}</span></div>'
        )

    next_val = f"{days_to_next} day" + ("" if days_to_next == 1 else "s")
    pillars_html = cy_pillar(
        "Next period", next_val, f"Expected {fmt_d(next_period)}", cur_day / cycle_len * 100.0, cur_phase_col
    )
    if ovu is not None:
        pillars_html += cy_pillar(
            "Ovulation", fmt_d(ovu["date_dt"]), f"LH peak · cycle day {int(ovu['cycle_day'])}",
            100.0 if ovu_confirmed else 50.0, PHASES["ovulatory"][1],
        )
    else:
        pillars_html += cy_pillar("Ovulation", "Pending", "No LH peak yet", 0.0, PHASES["ovulatory"][1])
    if shift is not None:
        pillars_html += cy_pillar(
            "Temperature shift", f"{shift:+.2f} °C", "Post-ovulation vs follicular",
            min(max(shift / 0.5, 0.0), 1.0) * 100.0, ACCENTS["orange"],
        )
    else:
        pillars_html += cy_pillar("Temperature shift", "–", "Awaiting ovulation", 0.0, ACCENTS["orange"])

    legend_html = "".join(
        f'<span class="phase-chip" style="--c:{col};"><i></i>{name}</span>' for name, col in PHASES.values()
    )
    pill_bg = hex_to_rgba(cur_phase_col, 0.14)

    with st.container(border=True, key="hero_cycle"):
        st.markdown(
            html(f"""
            <div class="hero-wrap">
                <div class="hero-gauge">
                    {ring_svg}
                    <div class="hero-gauge-center">
                        <div class="hero-score-num">{cur_day}</div>
                        <div class="hero-score-sub">of {cycle_len}-day cycle</div>
                    </div>
                </div>
                <div class="hero-details">
                    <div class="tile-top" style="margin-bottom: 8px;">
                        <span class="status-pill" style="background:{pill_bg}; color:{cur_phase_col};">
                            <span class="status-dot" style="background:{cur_phase_col};"></span>{cur_phase_name} phase
                        </span>
                    </div>
                    <div class="tile-tip" style="min-height:0; margin-top:0;">
                        Cycle {cur_cycle} began {fmt_d(cycle_start)}. Faded segments are projected from the previous cycle.
                    </div>
                    <div class="hero-pillars">{pillars_html}</div>
                    <div class="phase-legend">{legend_html}</div>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

    # ---- basal body temperature chart (full width) --------------------------------
    temps = df_cy["basal_body_temp_c"].astype(float)
    t_min, t_max = float(temps.min()), float(temps.max())
    t_span = max(t_max - t_min, 0.1)
    y_floor_c = t_min - t_span * 0.30
    y_ceil_c = t_max + t_span * 0.24
    flow_y = y_floor_c + t_span * 0.07

    fig_bbt = go.Figure()

    # phase bands + labels
    runs = []
    for i, ph in enumerate(df_cy["cycle_phase"]):
        if runs and runs[-1][0] == ph:
            runs[-1][2] = i
        else:
            runs.append([ph, i, i])
    for ph, a, b in runs:
        p_name, p_col = phase_info(str(ph))
        fig_bbt.add_vrect(x0=a - 0.5, x1=b + 0.5, fillcolor=hex_to_rgba(p_col, 0.09), layer="below", line_width=0)
        fig_bbt.add_annotation(
            x=(a + b) / 2, y=1.0, yref="paper", yanchor="bottom", showarrow=False, text=p_name.upper(),
            font=dict(family="Barlow, sans-serif", size=10, color=p_col),
        )

    # new-cycle divider
    cyc_first_idx = int(cyc["idx"].min())
    if cyc_first_idx > 0:
        fig_bbt.add_vline(x=cyc_first_idx - 0.5, line=dict(color="rgba(255,255,255,0.22)", width=1, dash="dot"), layer="below")

    # coverline
    if coverline is not None:
        fig_bbt.add_hline(
            y=coverline, line=dict(color=hex_to_rgba(ACCENTS["amber"], 0.55), width=1, dash="dash"), layer="below",
            annotation_text="Coverline", annotation_position="top left",
            annotation_font=dict(family="Barlow, sans-serif", size=10, color=hex_to_rgba(ACCENTS["amber"], 0.85)),
        )

    # temperature line with gradient fill
    fig_bbt.add_trace(
        go.Scatter(x=df_cy["idx"], y=[y_floor_c] * n_cy, mode="lines", line=dict(width=0, color="rgba(0,0,0,0)"),
                   hoverinfo="skip", showlegend=False)
    )
    fig_bbt.add_trace(
        go.Scatter(
            x=df_cy["idx"], y=temps, mode="lines", name="Basal temperature",
            line=dict(color=ACCENTS["orange"], width=2.5, shape="spline", smoothing=0.4),
            fill="tonexty",
            fillgradient=dict(
                type="vertical", start=y_floor_c, stop=t_max,
                colorscale=[[0.0, hex_to_rgba(ACCENTS["orange"], 0.0)], [1.0, hex_to_rgba(ACCENTS["orange"], 0.16)]],
            ),
            hoverinfo="skip",
        )
    )
    # per-day markers coloured by phase
    fig_bbt.add_trace(
        go.Scatter(
            x=df_cy["idx"], y=temps, mode="markers", showlegend=False,
            marker=dict(size=7, color=[phase_info(str(p))[1] for p in df_cy["cycle_phase"]], line=dict(color="#14171A", width=1.5)),
            customdata=[[r.date_short, int(r.cycle_day), phase_info(str(r.cycle_phase))[0]] for r in df_cy.itertuples()],
            hovertemplate="%{customdata[0]} · cycle day %{customdata[1]}<br>%{customdata[2]} · %{y:.2f} °C<extra></extra>",
        )
    )
    # menstrual flow dots along the bottom
    flow_df = df_cy[df_cy["flow_lvl"] > 0]
    if not flow_df.empty:
        fig_bbt.add_trace(
            go.Scatter(
                x=flow_df["idx"], y=[flow_y] * len(flow_df), mode="markers", name="Menstrual flow",
                marker=dict(size=[6 + 3 * int(v) for v in flow_df["flow_lvl"]], color="#FF5A4D", opacity=0.9),
                customdata=[f"{r.date_short} · {r.menstrual_flow} flow" for r in flow_df.itertuples()],
                hovertemplate="%{customdata}<extra></extra>",
            )
        )
    # LH surge diamonds (filled = peak, hollow = high)
    lh_df = df_cy[df_cy["lh_lvl"] > 0]
    if not lh_df.empty:
        fig_bbt.add_trace(
            go.Scatter(
                x=lh_df["idx"], y=lh_df["basal_body_temp_c"].astype(float) + t_span * 0.13, mode="markers", name="LH surge",
                marker=dict(
                    symbol="diamond", size=12,
                    color=[ACCENTS["amber"] if v == 2 else "rgba(0,0,0,0)" for v in lh_df["lh_lvl"]],
                    line=dict(color=ACCENTS["amber"], width=2),
                ),
                customdata=[f"{r.date_short} · LH {r.ovulation_lh_test}" for r in lh_df.itertuples()],
                hovertemplate="%{customdata}<extra></extra>",
            )
        )
    # today marker
    fig_bbt.add_trace(
        go.Scatter(
            x=[int(cur["idx"])], y=[float(cur["basal_body_temp_c"])], mode="markers", showlegend=False,
            marker=dict(size=11, color="#FFFFFF", line=dict(color=ACCENTS["orange"], width=3)),
            customdata=[cur["date_short"]], hovertemplate="%{customdata}, %{y:.2f} °C<extra></extra>",
        )
    )

    cy_ticks = pick_ticks(n_cy, 7)
    cy_tick_text = [df_cy["date_short"].iloc[i] for i in cy_ticks]
    step = 0.1 if t_span <= 0.8 else 0.25
    y_ticks = [round(v, 2) for v in np.arange(np.ceil(t_min / step) * step, t_max + 1e-9, step)]

    fig_bbt.update_layout(
        height=300,
        margin=dict(l=8, r=8, t=26, b=64),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hovermode="closest", hoverdistance=40,
        hoverlabel=dict(bgcolor="#0C0E10", bordercolor="#20262B", font=dict(family="Barlow, sans-serif", size=12, color="#F2F4F5")),
        showlegend=True,
        legend=dict(orientation="h", x=0, y=-0.17, yanchor="top", font=dict(family="Barlow, sans-serif", size=11, color="#9AA5AD")),
        xaxis=dict(
            range=[-0.8, n_cy - 0.2], tickmode="array", tickvals=cy_ticks, ticktext=cy_tick_text,
            showgrid=False, zeroline=False, showline=False, fixedrange=True,
            tickfont=dict(family="Barlow, sans-serif", size=11, color="#6E7A83"),
        ),
        yaxis=dict(
            range=[y_floor_c, y_ceil_c], tickmode="array", tickvals=y_ticks, tickformat=".1f",
            showgrid=True, gridcolor="#20262B", gridwidth=1, zeroline=False, showline=False, fixedrange=True,
            tickfont=dict(family="Barlow, sans-serif", size=11, color="#6E7A83"),
        ),
    )

    bbt_now = float(cur["basal_body_temp_c"])
    if shift is not None and shift >= 0.2:
        bbt_lvl, bbt_txt = "safe", "Biphasic"
        bbt_tip = f"Up {shift:+.2f} °C from the follicular baseline, a clear post-ovulation rise."
    elif shift is not None:
        bbt_lvl, bbt_txt = "caution", "Flat"
        bbt_tip = f"Only {shift:+.2f} °C above the follicular baseline; the post-ovulation rise is weak."
    else:
        bbt_lvl, bbt_txt = "safe", "Tracking"
        bbt_tip = "Ovulation not yet detected; temperature is tracked against the follicular baseline."

    render_tile(
        "Basal body temperature", bbt_txt, bbt_lvl, f"{bbt_now:.2f}", "°C", fig_bbt, bbt_tip,
        subrows=[
            ("Follicular average", f"{fol_mean:.2f} °C" if fol_mean is not None else "–"),
            ("Post-ovulation average", f"{post_mean:.2f} °C" if post_mean is not None else "–"),
            ("Coverline", f"{coverline:.2f} °C" if coverline is not None else "–"),
        ],
        measures="Resting body temperature taken on waking, logged daily alongside LH tests and flow.",
        why="A sustained rise after the LH peak confirms ovulation and shows whether the cycle is stable under mission stress.",
    )

    # ---- three summary tiles --------------------------------------------------------
    x_cy = [0, max(n_cy - 1, 1)]
    flow_labels = [f"{r.date_short} · " + ("no flow" if r.flow_lvl == 0 else f"{r.menstrual_flow} flow") for r in df_cy.itertuples()]
    lh_labels = [f"{r.date_short} · LH {r.ovulation_lh_test}" for r in df_cy.itertuples()]
    sym_labels = [
        f"{r.date_short} · " + (", ".join(pretty_symptom(s) for s in r.symptom_list) if r.symptom_list else "no symptoms")
        for r in df_cy.itertuples()
    ]

    m1, m2, m3 = st.columns(3)

    with m1:
        bleed = cyc[cyc["flow_lvl"] > 0]
        bleed_days = len(bleed)
        flow_now = int(cur["flow_lvl"]) > 0
        if bleed_days:
            peak_row = bleed.loc[bleed["flow_lvl"].idxmax()]
            peak_flow, peak_day = str(peak_row["menstrual_flow"]), int(peak_row["cycle_day"])
            period_end = bleed["date_dt"].max()
            fl_lvl, fl_txt = ("safe", "Active") if flow_now else ("safe", "Completed")
            fl_tip = (
                f"Day {cur_day} of your period; flow has peaked at {peak_flow} so far."
                if flow_now else
                f"Peaked at {peak_flow} flow on cycle day {peak_day}; bleeding ended {fmt_d(period_end)}."
            )
            fl_sub = [("Period start", fmt_d(cycle_start)), ("Peak flow", f"{peak_flow.capitalize()} · day {peak_day}")]
        else:
            fl_lvl, fl_txt, fl_tip = "caution", "None logged", "No bleeding has been logged in the current cycle."
            fl_sub = [("Period start", "–"), ("Peak flow", "–")]
        fig_flow = build_sparkline(
            x_vals=df_cy["idx"], y_vals=df_cy["flow_lvl"], hover_labels=flow_labels, unit="of 4",
            accent_hex=ACCENTS["orange"], tick_vals=pick_ticks(n_cy), tick_text=[df_cy["date_short"].iloc[i] for i in pick_ticks(n_cy)],
            x_range=x_cy, now_x=int(cur["idx"]), now_y=int(cur["flow_lvl"]), now_label=cur["date_short"],
        )
        render_tile(
            "Menstrual flow", fl_txt, fl_lvl, f"{bleed_days}", "bleed days", fig_flow, fl_tip, subrows=fl_sub,
            measures="Daily bleeding intensity on a 0–4 scale: none, spotting, light, moderate, heavy.",
            why="Flow duration and volume flag hormonal disruption or heavy bleeding that could affect hydration and iron status.",
        )

    with m2:
        if ovu is not None:
            ov_lvl, ov_txt = ("safe", "Confirmed") if ovu_confirmed else ("caution", "Unconfirmed")
            ov_val, ov_unit = f"Day {int(ovu['cycle_day'])}", "LH peak"
            surge = cyc[cyc["lh_lvl"] > 0]
            surge_txt = fmt_d(surge["date_dt"].min()) if len(surge) == 1 else f"{fmt_d(surge['date_dt'].min())} – {fmt_d(surge['date_dt'].max())}"
            ov_tip = (
                f"LH surge peaked {fmt_d(ovu['date_dt'])}; temperature has stayed above the coverline for {days_above} days since."
                if ovu_confirmed else
                f"LH surge peaked {fmt_d(ovu['date_dt'])}; waiting on a sustained temperature rise to confirm."
            )
        else:
            ov_lvl, ov_txt, ov_val, ov_unit = "caution", "Not detected", "–", ""
            surge_txt, ov_tip = "–", "No LH peak has been logged in the current cycle."
        fig_lh = build_sparkline(
            x_vals=df_cy["idx"], y_vals=df_cy["lh_lvl"], hover_labels=lh_labels, unit="of 2",
            accent_hex=ACCENTS["amber"], tick_vals=pick_ticks(n_cy), tick_text=[df_cy["date_short"].iloc[i] for i in pick_ticks(n_cy)],
            x_range=x_cy, now_x=int(cur["idx"]), now_y=int(cur["lh_lvl"]), now_label=cur["date_short"],
        )
        render_tile(
            "Ovulation (LH test)", ov_txt, ov_lvl, ov_val, ov_unit, fig_lh, ov_tip,
            subrows=[("LH surge", surge_txt), ("Fertile window", f"{fertile_txt} · {fw_range}" if fw_range else fertile_txt)],
            measures="Urinary luteinising hormone test result: negative, high, or peak.",
            why="Confirms that ovulation is occurring, which matters for estrogen-dependent bone and cardiovascular health in flight.",
        )

    with m3:
        sym_days = int((df_cy["symptom_n"] > 0).sum())
        all_syms = [s for lst in df_cy["symptom_list"] for s in lst]
        if sym_days:
            counts = pd.Series([pretty_symptom(s) for s in all_syms]).value_counts()
            top_sym, top_n = str(counts.index[0]), int(counts.iloc[0])
            last_sym_date = df_cy.loc[df_cy["symptom_n"] > 0, "date_dt"].max()
            since = (cur_date - last_sym_date).days
            all_mild = all(s.startswith("mild_") or s == "fatigue" for s in all_syms)
            sy_lvl, sy_txt = ("safe", "Mild") if all_mild else ("caution", "Notable")
            sy_tip = f"Last reported {fmt_d(last_sym_date)} ({since} days ago)" + ("; every entry was mild." if all_mild else ".")
            sy_sub = [("Most frequent", f"{top_sym.capitalize()} ×{top_n}"), ("Last reported", fmt_d(last_sym_date))]
        else:
            sy_lvl, sy_txt, sy_tip = "safe", "Clear", "No symptoms have been reported in this log."
            sy_sub = [("Most frequent", "–"), ("Last reported", "–")]
        fig_sym = build_sparkline(
            x_vals=df_cy["idx"], y_vals=df_cy["symptom_n"], hover_labels=sym_labels, unit="reported",
            accent_hex=ACCENTS["ice_blue"], tick_vals=pick_ticks(n_cy), tick_text=[df_cy["date_short"].iloc[i] for i in pick_ticks(n_cy)],
            x_range=x_cy, now_x=int(cur["idx"]), now_y=int(cur["symptom_n"]), now_label=cur["date_short"],
        )
        render_tile(
            "Reported symptoms", sy_txt, sy_lvl, f"{sym_days}", f"of {n_cy} days", fig_sym, sy_tip, subrows=sy_sub,
            measures="Self-reported cycle symptoms such as cramping, bloating and fatigue.",
            why="Tracks how much cycle symptoms intrude on workload, sleep and performance during operations.",
        )

    # ---- daily log ----------------------------------------------------------------------
    cells = []
    for r in df_cy.itertuples():
        p_name, p_col = phase_info(str(r.cycle_phase))
        marks = "".join('<i class="cy-flow"></i>' for _ in range(int(r.flow_lvl)))
        if r.lh_lvl == 2:
            marks += '<i class="cy-lh"></i>'
        elif r.lh_lvl == 1:
            marks += '<i class="cy-lh hollow"></i>'
        if r.symptom_n > 0:
            marks += '<i class="cy-sym"></i>'
        parts = [r.date_short, f"Cycle {int(r.cycle_number)} · day {int(r.cycle_day)}", p_name, f"{r.basal_body_temp_c:.2f} °C"]
        if r.flow_lvl > 0:
            parts.append(f"{r.menstrual_flow} flow")
        if r.lh_lvl > 0:
            parts.append(f"LH {r.ovulation_lh_test}")
        if r.symptom_n > 0:
            parts.append(", ".join(pretty_symptom(s) for s in r.symptom_list))
        tip_txt = " · ".join(parts)
        today_cls = " cy-today" if int(r.idx) == n_cy - 1 else ""
        cells.append(
            f'<div class="cy-cell{today_cls}" style="--ph:{p_col};" title="{tip_txt}">'
            f'<span class="cy-date">{r.date_short}</span>'
            f'<span class="cy-day"><small>D</small>{int(r.cycle_day)}</span>'
            f'<span class="cy-marks">{marks}</span></div>'
        )

    log_legend = (
        '<div class="cy-legend">'
        + legend_html
        + '<span><i class="cy-flow"></i>Flow (1–4 dots: spotting → heavy)</span>'
        + '<span><i class="cy-lh"></i>LH peak</span>'
        + '<span><i class="cy-lh hollow"></i>LH high</span>'
        + '<span><i class="cy-sym"></i>Symptoms reported</span>'
        + "</div>"
    )

    cells_html = "".join(cells)
    with st.container(border=True, key="tile_daily_log"):
        st.markdown(
            html(f"""
            <div class="tile-top">
                <span class="tile-label">Daily log</span>
                <span class="status-pill" style="background:rgba(154,165,173,0.14); color:#9AA5AD;">{n_cy} days logged</span>
            </div>
            <div class="cy-grid">{cells_html}</div>
            {log_legend}
            """),
            unsafe_allow_html=True,
        )
    
    # --- Section 2: 30-day recovery & readiness --------------------------------
    st.markdown('<div class="section-title">30-day recovery & readiness</div>', unsafe_allow_html=True)

    df_30d["day_idx"] = np.arange(len(df_30d))
    df_30d["date_short"] = pd.to_datetime(df_30d["date"]).dt.strftime("%b %d")
    latest_30 = df_30d.iloc[-1]
    t30_vals = pick_ticks(len(df_30d))
    t30_text = [df_30d["date_short"].iloc[i] for i in t30_vals]
    x30 = [0, len(df_30d) - 1]

    c1, c2, c3 = st.columns(3)

    with c1:
        base_low = int(latest_30["established_hrv_baseline_low_ms"])
        base_high = int(latest_30["established_hrv_baseline_high_ms"])
        hrv_now = float(latest_30["hrv_overnight_avg_ms"])
        hrv_level = "safe" if hrv_now >= base_low else "caution"
        if hrv_now < base_low:
            hrv_tip = f"Below your {base_low}–{base_high} ms baseline band; go easy today."
        elif hrv_now > base_high:
            hrv_tip = f"Above your {base_low}–{base_high} ms baseline band, a strong recovery signal."
        else:
            hrv_tip = f"Inside your {base_low}–{base_high} ms baseline band (shaded)."
        fig_hrv = build_sparkline(
            x_vals=df_30d["day_idx"], y_vals=df_30d["hrv_overnight_avg_ms"], hover_labels=df_30d["date_short"],
            unit="ms", accent_hex=ACCENTS["lime"], tick_vals=t30_vals, tick_text=t30_text, x_range=x30,
            baseline_band=(base_low, base_high), now_x=int(latest_30["day_idx"]), now_y=hrv_now,
            now_label=latest_30["date_short"],
        )
        render_tile(
            "Overnight HRV", str(latest_30["hrv_status"]).capitalize(), hrv_level, f"{int(hrv_now)}", "ms", fig_hrv, hrv_tip,
            subrows=[("7-day average", f"{latest_30['hrv_7day_avg_ms']:.1f} ms"), ("Baseline range", f"{base_low}–{base_high} ms")],
            measures="Millisecond variation between consecutive heartbeats during overnight sleep compared to baseline.",
            why="Reflects autonomic nervous system balance, highlighting accumulated stress, illness, or under-recovery.",
        )

    with c2:
        sleep_val = int(latest_30["sleep_score_1_100"])
        sleep_avg = float(df_30d["sleep_score_1_100"].mean())
        sleep_level, sleep_text = (("safe", "Restorative") if sleep_val >= 80 else ("caution", "Fair") if sleep_val >= 65 else ("danger", "Poor"))
        diff = sleep_val - sleep_avg
        sleep_tip = (
            f"{abs(diff):.0f} pts {'above' if diff >= 0 else 'below'} your 30-day average"
            + ("; prioritise a wind-down before lights out." if diff < -3 else ".")
        )
        fig_sleep = build_sparkline(
            x_vals=df_30d["day_idx"], y_vals=df_30d["sleep_score_1_100"], hover_labels=df_30d["date_short"],
            unit="pts", accent_hex=ACCENTS["ice_blue"], tick_vals=t30_vals, tick_text=t30_text, x_range=x30,
            now_x=int(latest_30["day_idx"]), now_y=sleep_val, now_label=latest_30["date_short"],
        )
        render_tile(
            "Sleep score", sleep_text, sleep_level, f"{sleep_val}", "pts", fig_sleep, sleep_tip,
            subrows=[("30-day average", f"{sleep_avg:.0f} pts"), ("30-day peak", f"{int(df_30d['sleep_score_1_100'].max())} pts")],
            measures="Composite 1–100 score of sleep duration, deep/REM architecture, and nighttime awakenings.",
            why="Circadian disruption on Mars/orbit impairs executive judgment, mood stability, and physical tissue repair.",
        )

    with c3:
        vo2_val = float(latest_30["vo2_max_estimate_ml_kg_min"])
        vo2_change = vo2_val - float(df_30d["vo2_max_estimate_ml_kg_min"].iloc[0])
        vo2_level, vo2_text = (("safe", "Improving") if vo2_change > 0.1 else ("safe", "Stable") if vo2_change >= -0.1 else ("caution", "Declining"))
        fig_vo2 = build_sparkline(
            x_vals=df_30d["day_idx"], y_vals=df_30d["vo2_max_estimate_ml_kg_min"], hover_labels=df_30d["date_short"],
            unit="ml/kg/min", accent_hex=ACCENTS["orange"], tick_vals=t30_vals, tick_text=t30_text, x_range=x30,
            now_x=int(latest_30["day_idx"]), now_y=vo2_val, now_label=latest_30["date_short"],
        )
        render_tile(
            "VO₂ max estimate", vo2_text, vo2_level, f"{vo2_val:.1f}", "ml/kg/min", fig_vo2,
            f"Aerobic capacity changed {vo2_change:+.1f} ml/kg/min over the past 30 days.",
            subrows=[("30-day change", f"{vo2_change:+.1f} ml/kg/min"), ("30-day low", f"{df_30d['vo2_max_estimate_ml_kg_min'].min():.1f} ml/kg/min")],
            measures="Maximum rate of oxygen consumption per kilogram of body mass during aerobic exercise.",
            why="Verifies that daily treadmill and cycle countermeasures are preventing aerobic fitness loss.",
        )

    # --- Section 3: monthly health tests ---------------------------------------
    st.markdown('<div class="section-title">Monthly health tests</div>', unsafe_allow_html=True)

    df_test["test_idx"] = np.arange(len(df_test))
    df_test["month_short"] = pd.to_datetime(df_test["date"]).dt.strftime("%b %Y")
    latest_test = df_test.iloc[-1]
    n_tests = len(df_test)
    ttest_vals = pick_ticks(n_tests)
    ttest_text = [pd.to_datetime(df_test["date"].iloc[i]).strftime("%b") for i in ttest_vals]
    xt = [0, max(n_tests - 1, 1)]

    t1, t2, t3 = st.columns(3)

    with t1:
        g = df_test["dominant_handgrip_best_of_3_kgf"]
        grip_val = float(latest_test["dominant_handgrip_best_of_3_kgf"])
        grip_delta = grip_val - float(g.iloc[0])
        if grip_val >= float(g.max()):
            grip_level, grip_text, grip_tip = "safe", "Peak", f"Highest grip output across your {n_tests}-month mission."
        elif grip_delta >= 0:
            grip_level, grip_text, grip_tip = "safe", "Maintained", "Grip strength is at or above your starting level."
        else:
            grip_level, grip_text, grip_tip = "caution", "Below start", "Grip strength is below your first test; check resistive load."
        fig_grip = build_sparkline(
            x_vals=df_test["test_idx"], y_vals=g, hover_labels=df_test["month_short"], unit="kgf",
            accent_hex=ACCENTS["lime"], tick_vals=ttest_vals, tick_text=ttest_text, x_range=xt,
            now_x=int(latest_test["test_idx"]), now_y=grip_val, now_label=latest_test["month_short"],
        )
        render_tile(
            "Dominant handgrip", grip_text, grip_level, f"{grip_val:.1f}", "kgf", fig_grip, grip_tip,
            subrows=[("Mission delta", f"{grip_delta:+.1f} kgf"), ("Working memory", f"{int(latest_test['working_memory_2back_accuracy_pct'])}% (2-back)")],
            measures="Peak isometric squeeze force (kgf) across three dynamometer trials.",
            why="Tracks neuromuscular strength and forearm endurance critical for pressurized EVA glove operations.",
        )

    with t2:
        p = df_test["psychomotor_vigilance_median_reaction_time_ms"]
        pvt_val = int(latest_test["psychomotor_vigilance_median_reaction_time_ms"])
        if pvt_val <= float(p.iloc[0]):
            pvt_level, pvt_text, pvt_tip = "safe", "Sharp", "Reaction time is at or faster than your first test."
        elif pvt_val <= float(p.mean()) * 1.05:
            pvt_level, pvt_text, pvt_tip = "safe", "Typical", "Reaction time is within your usual range."
        else:
            pvt_level, pvt_text, pvt_tip = "caution", "Slower", "Reaction time is slower than your mission average."
        fig_pvt = build_sparkline(
            x_vals=df_test["test_idx"], y_vals=p, hover_labels=df_test["month_short"], unit="ms",
            accent_hex=ACCENTS["ice_blue"], tick_vals=ttest_vals, tick_text=ttest_text, x_range=xt,
            now_x=int(latest_test["test_idx"]), now_y=pvt_val, now_label=latest_test["month_short"],
        )
        render_tile(
            "Psychomotor vigilance", pvt_text, pvt_level, f"{pvt_val}", "ms", fig_pvt, pvt_tip,
            subrows=[(f"{n_tests}-month best", f"{int(p.min())} ms"), (f"{n_tests}-month average", f"{p.mean():.0f} ms")],
            measures="Median visual-stimulus reaction speed (ms) during a sustained attention task.",
            why="Detects subtle cognitive fatigue, sleep debt, or CO₂-induced alertness dips before high-risk maneuvers.",
        )

    with t3:
        d = df_test["dxa_total_hip_bone_density_g_cm2"]
        dxa_val = float(latest_test["dxa_total_hip_bone_density_g_cm2"])
        dxa_delta = dxa_val - float(d.iloc[0])
        dxa_pct = dxa_delta / max(float(d.iloc[0]), 1e-9) * 100.0
        if dxa_pct >= -0.5:
            dxa_level, dxa_text, dxa_tip = "safe", "Preserved", "No meaningful bone mineral loss since your first scan."
        elif dxa_pct >= -2.0:
            dxa_level, dxa_text, dxa_tip = "caution", "Minor loss", f"Hip density is down {abs(dxa_pct):.1f}% since your first scan."
        else:
            dxa_level, dxa_text, dxa_tip = "danger", "Declining", f"Hip density is down {abs(dxa_pct):.1f}% since your first scan."
        fig_dxa = build_sparkline(
            x_vals=df_test["test_idx"], y_vals=d, hover_labels=df_test["month_short"], unit="g/cm²",
            accent_hex=ACCENTS["amber"], tick_vals=ttest_vals, tick_text=ttest_text, x_range=xt,
            now_x=int(latest_test["test_idx"]), now_y=dxa_val, now_label=latest_test["month_short"],
        )
        render_tile(
            "Total hip bone density", dxa_text, dxa_level, f"{dxa_val:.3f}", "g/cm²", fig_dxa, dxa_tip,
            subrows=[("Net change", f"{dxa_delta:+.3f} g/cm²"), (f"{n_tests}-month mean", f"{d.mean():.3f} g/cm²")],
            measures="Dual-energy X-ray absorptiometry (DXA) bone mineral density (g/cm²) at the proximal femur.",
            why="Monitors skeletal demineralization caused by reduced mechanical loading on Mars and in transit.",
        )

    # --- Section 4: musculoskeletal & strength tests (milou_extra.csv) --------
    st.markdown('<div class="section-title">Musculoskeletal & strength tests</div>', unsafe_allow_html=True)

    df_extra["extra_idx"] = np.arange(len(df_extra))
    df_extra["month_short"] = pd.to_datetime(df_extra["date"]).dt.strftime("%b %Y")
    latest_extra = df_extra.iloc[-1]
    n_extra = len(df_extra)
    textra_vals = pick_ticks(n_extra)
    textra_text = [pd.to_datetime(df_extra["date"].iloc[i]).strftime("%b") for i in textra_vals]
    xe = [0, max(n_extra - 1, 1)]

    def strength_status(latest_val: float, series: pd.Series, unit_label: str):
        delta = latest_val - float(series.iloc[0])
        if latest_val >= float(series.max()):
            return "safe", "Peak", f"Highest {unit_label} output across your {n_extra}-month log.", delta
        if delta >= 0:
            return "safe", "Maintained", f"Force output is at or above your mission baseline.", delta
        return "caution", "Below start", f"Down {abs(delta):.1f} from baseline; review resistance load.", delta

    s1, s2, s3 = st.columns(3)

    with s1:
        imtp_s = df_extra["isometric_mid_thigh_pull_peak_force_best_of_3_n"]
        imtp_val = int(latest_extra["isometric_mid_thigh_pull_peak_force_best_of_3_n"])
        imtp_lvl, imtp_txt, imtp_tip, imtp_delta = strength_status(float(imtp_val), imtp_s, "peak pull")
        fig_imtp = build_sparkline(
            x_vals=df_extra["extra_idx"], y_vals=imtp_s, hover_labels=df_extra["month_short"], unit="N",
            accent_hex=ACCENTS["orange"], tick_vals=textra_vals, tick_text=textra_text, x_range=xe,
            now_x=int(latest_extra["extra_idx"]), now_y=imtp_val, now_label=latest_extra["month_short"],
        )
        render_tile(
            "Isometric mid-thigh pull", imtp_txt, imtp_lvl, f"{imtp_val}", "N", fig_imtp, imtp_tip,
            subrows=[("Mission delta", f"{imtp_delta:+.0f} N"), (f"{n_extra}-month mean", f"{imtp_s.mean():.0f} N")],
            measures="Peak vertical ground-reaction force (Newtons) across three maximal mid-thigh pull trials.",
            why="Evaluates whole-body posterior-chain power required for surface locomotion and sample recovery.",
        )

    with s2:
        lp_s = df_extra["seated_leg_press_1rm_kg"]
        lp_val = float(latest_extra["seated_leg_press_1rm_kg"])
        lp_lvl, lp_txt, lp_tip, lp_delta = strength_status(lp_val, lp_s, "leg press")
        fig_lp = build_sparkline(
            x_vals=df_extra["extra_idx"], y_vals=lp_s, hover_labels=df_extra["month_short"], unit="kg",
            accent_hex=ACCENTS["lime"], tick_vals=textra_vals, tick_text=textra_text, x_range=xe,
            now_x=int(latest_extra["extra_idx"]), now_y=lp_val, now_label=latest_extra["month_short"],
        )
        render_tile(
            "Seated leg press 1RM", lp_txt, lp_lvl, f"{lp_val:.1f}", "kg", fig_lp, lp_tip,
            subrows=[("Mission delta", f"{lp_delta:+.1f} kg"), (f"{n_extra}-month peak", f"{lp_s.max():.1f} kg")],
            measures="One-repetition maximum (1RM) lower-limb pushing load in kilograms on the resistive exercise unit.",
            why="Preserves quadriceps and gluteal mass against anti-gravity muscle atrophy during prolonged low-G stays.",
        )

    with s3:
        chest_s = df_extra["chest_cable_isometric_peak_force_best_of_3_n"]
        chest_val = int(latest_extra["chest_cable_isometric_peak_force_best_of_3_n"])
        chest_lvl, chest_txt, chest_tip, chest_delta = strength_status(float(chest_val), chest_s, "chest press")
        fig_chest = build_sparkline(
            x_vals=df_extra["extra_idx"], y_vals=chest_s, hover_labels=df_extra["month_short"], unit="N",
            accent_hex=ACCENTS["ice_blue"], tick_vals=textra_vals, tick_text=textra_text, x_range=xe,
            now_x=int(latest_extra["extra_idx"]), now_y=chest_val, now_label=latest_extra["month_short"],
        )
        render_tile(
            "Chest cable isometric force", chest_txt, chest_lvl, f"{chest_val}", "N", fig_chest, chest_tip,
            subrows=[("Mission delta", f"{chest_delta:+.0f} N"), (f"{n_extra}-month mean", f"{chest_s.mean():.0f} N")],
            measures="Best-of-three peak horizontal pushing force (Newtons) on the cable resistance rig.",
            why="Monitors upper-body anterior pressing strength needed for hatch operations and EVA suit donning.",
        )

    s4, _, _ = st.columns(3)

    with s4:
        row_s = df_extra["row_cable_isometric_peak_force_best_of_3_n"]
        row_val = int(latest_extra["row_cable_isometric_peak_force_best_of_3_n"])
        row_lvl, row_txt, row_tip, row_delta = strength_status(float(row_val), row_s, "cable row")
        fig_row = build_sparkline(
            x_vals=df_extra["extra_idx"], y_vals=row_s, hover_labels=df_extra["month_short"], unit="N",
            accent_hex=ACCENTS["amber"], tick_vals=textra_vals, tick_text=textra_text, x_range=xe,
            now_x=int(latest_extra["extra_idx"]), now_y=row_val, now_label=latest_extra["month_short"],
        )
        render_tile(
            "Row cable isometric force", row_txt, row_lvl, f"{row_val}", "N", fig_row, row_tip,
            subrows=[("Mission delta", f"{row_delta:+.0f} N"), (f"{n_extra}-month mean", f"{row_s.mean():.0f} N")],
            measures="Best-of-three peak horizontal pulling force (Newtons) on the seated cable row rig.",
            why="Tracks upper-back and scapular stabilizer strength to prevent shoulder injury during EVA tool handling.",
        )

    
    return round(health_summary["overall"] / 10.0, 1)
# --- Render milou's Header ---
def render():
    # 1. Reserve the top spot on the page first
    header_slot = st.empty()

    # 2. Run graphs() and get the calculated score
    calculated_score = graphs()

    # 3. Render the header back into the reserved top spot
    with header_slot.container():
        render_astronaut_header(
            name="Milou de Jong",
            country_code="nl",
            gender="Female",
            age=38,
            height_cm=157,
            weight_kg=49.2,
            health_score=calculated_score,
            time_outside="03h 18m",
        )
