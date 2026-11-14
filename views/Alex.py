import streamlit as st

def render_astronaut_header(
    name: str,
    country_code: str,
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
                CREW TELEMETRY // ACTIVE OPERATOR
            </div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="font-size: 26px; font-weight: 800; line-height: 1.1; color: #fafafa;">{name}</span>
                <img src="{flag_url}" width="28" style="border-radius: 2px; border: 1px solid #333;" alt="{country_code}">
            </div>
            <div style="display: flex; align-items: center; gap: 14px; font-size: 13px; color: #b0b0b0; font-weight: 500;">
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


# --- Render Alex's Header ---
def render():
    render_astronaut_header(
        name="Cmdr. Alex Vance",
        country_code="us",
        age=38,
        height_cm=182,
        weight_kg=74.5,
        health_score=9.8,
        time_outside="04h 18m",
    )