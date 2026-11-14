"""Mars Station Health & Weather — Python 3.10+.
Install: pip install 'streamlit>=1.50,<2' 'pandas>=2.2,<4' 'plotly>=5.20,<8'
Run: streamlit run app.py
Place mars_sol_1740_combined_20min_sensor_averages(2).csv beside this file.
"""
from pathlib import Path
from html import escape
from io import BytesIO
import re
import math
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Mars Station", page_icon="🔴", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Condensed:wght@500;600;700&display=swap');
:root{color-scheme:dark}
.stApp{background:#0C0E10;color:#F2F4F5}
html,body,[class*="css"],.stApp{font-family:Barlow,Arial,sans-serif;font-variant-numeric:tabular-nums}
header[data-testid="stHeader"],#MainMenu,footer{display:none}
.block-container{max-width:980px;padding:1.2rem 1.2rem 3rem}
[data-testid="stVerticalBlock"]{gap:.75rem}
[data-testid="stHorizontalBlock"]{gap:.75rem}
[data-testid="stColumn"]{min-width:0}

/* Units popover */
[data-testid="stPopover"]{display:flex;justify-content:flex-end}
[data-testid="stPopover"] button{background:#14171A;border:1px solid #23282D;border-radius:999px;color:#C9D1D6;min-height:34px;padding:0 14px;font-size:14px;font-weight:600}
[data-testid="stPopover"] button:hover{border-color:#3A4249;color:#F2F4F5}
[data-testid="stPopoverBody"]{background:#14171A;border:1px solid #23282D;border-radius:18px;min-width:260px}
[data-testid="stPopoverBody"] [data-testid="stWidgetLabel"] p{color:#8A959D;font-size:13px}

.brand{font-family:'Barlow Condensed',sans-serif;font-size:18px;font-weight:600;letter-spacing:.06em;padding:6px 0}
.brand i{display:inline-block;width:9px;height:9px;border-radius:50%;background:#FF6A3D;margin-right:10px}
.section{display:flex;align-items:center;gap:12px;flex-wrap:wrap;font-family:'Barlow Condensed',sans-serif;font-size:22px;font-weight:600;margin:18px 2px 2px}
.section .pill{font-family:Barlow,Arial,sans-serif}

/* Hero */
.hero{display:flex;flex-direction:column;align-items:center;padding:6px 0 14px}
.ring{position:relative;width:240px;height:240px}
.ring svg{width:100%;height:100%;transform:rotate(135deg)}
.ring .center{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.temp{font-family:'Barlow Condensed',sans-serif;font-size:92px;font-weight:600;line-height:.95;letter-spacing:-.02em}
.place{color:#9AA5AD;font-size:15px;margin-top:4px}
.hl{display:flex;gap:26px;margin-top:6px;font-size:16px;color:#C9D1D6}
.hl span{color:#6E7A83;margin-right:6px}
.verdict{margin-top:12px;font-size:15px;padding:6px 16px}
.reason{margin-top:8px;color:#8A959D;font-size:14px;text-align:center}

/* Hourly strip */
.strip{display:flex;gap:6px;overflow-x:auto;padding:2px}
.hour{flex:1 0 74px;text-align:center;padding:14px 6px;border-radius:16px;background:#14171A}
.hour.now{background:#F2F4F5;color:#0C0E10}
.hour .t{font-size:13px;color:#7F8A92}.hour.now .t{color:#4A545B}
.hour .v{font-family:'Barlow Condensed',sans-serif;font-size:26px;font-weight:600;margin-top:6px}
.hour.fc .v{color:#9AA5AD}

/* Status pills and dots */
.pill{display:inline-block;font-size:12px;font-weight:600;padding:4px 10px;border-radius:999px;white-space:nowrap}
.pill.l0{background:rgba(61,220,132,.14);color:#3DDC84}
.pill.l1{background:rgba(255,200,87,.14);color:#FFC857}
.pill.l2{background:rgba(255,90,77,.16);color:#FF6B5E}
.d{display:inline-block;flex:none;width:8px;height:8px;border-radius:50%}
.d.l0{background:#3DDC84}.d.l1{background:#FFC857}.d.l2{background:#FF5A4D}

/* Life-support gauges */
.ggs{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}
.gg{background:#14171A;border-radius:22px;padding:14px 14px 12px;min-width:0}
.gtop{display:flex;align-items:center;justify-content:space-between;gap:8px}
.gg svg{display:block;width:100%;max-width:150px;margin:4px auto 0}
.gr{text-align:center;font-size:12px;color:#6E7A83;margin-top:2px}

/* Tiles */
[data-testid="stVerticalBlock"][class*="st-key-card_"]{background:#14171A;border-radius:22px;padding:18px;box-sizing:border-box;overflow:hidden;gap:.4rem}
.top{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px 8px}
.label{color:#8A959D;font-size:14px;font-weight:500}
.value{font-family:'Barlow Condensed',sans-serif;font-size:44px;font-weight:600;line-height:1.05;margin-top:4px;letter-spacing:-.01em}
.unit{font-size:17px;font-weight:500;color:#6E7A83;margin-left:5px;letter-spacing:0}
.tip{font-size:14px;line-height:1.45;color:#D5DBDF;margin-top:2px}
.fxs{display:flex;flex-direction:column;gap:7px;margin-top:12px;padding-top:12px;border-top:1px solid #20262B}
.fx{display:grid;grid-template-columns:8px 92px 1fr;gap:8px;align-items:start;font-size:13px;line-height:1.35}
.fx .d{margin-top:5px}
.fx b{font-weight:600;color:#F2F4F5}
.fx span{color:#9AA5AD}

.sun-meta{display:flex;gap:28px;margin-top:10px}
.sun-meta div{font-size:14px;color:#8A959D}
.sun-meta b{display:block;font-family:'Barlow Condensed',sans-serif;font-size:30px;font-weight:600;color:#F2F4F5}

@media(max-width:640px){
.block-container{padding:1rem .7rem}.ring{width:210px;height:210px}.temp{font-size:78px}
[data-testid="stHorizontalBlock"]{flex-wrap:wrap}
[data-testid="stHorizontalBlock"]>[data-testid="stColumn"]{min-width:min(100%,260px)!important;flex:1 1 260px!important}}
/* Keep the top bar on one line, even on phones */
.st-key-topbar [data-testid="stHorizontalBlock"]{flex-wrap:nowrap!important;align-items:center}
.st-key-topbar [data-testid="stHorizontalBlock"]>[data-testid="stColumn"]{min-width:0!important}
.st-key-topbar [data-testid="stHorizontalBlock"]>[data-testid="stColumn"]:first-child{flex:1 1 auto!important}
.st-key-topbar [data-testid="stHorizontalBlock"]>[data-testid="stColumn"]:last-child{flex:0 0 auto!important;width:auto!important}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

ACCENT = "#FF6A3D"
COOL = "#6FD3FF"
LEVEL_COLORS = {0: "#3DDC84", 1: "#FFC857", 2: "#FF5A4D"}


def html(value):
    st.markdown(value, unsafe_allow_html=True)


def safe(value):
    return escape(str(value), quote=True)


def fmt(value, digits=1):
    return "—" if pd.isna(value) else f"{value:,.{digits}f}"


def norm(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def match(df, *aliases):
    names = {norm(c): c for c in df.columns}
    return next((names[norm(a)] for a in aliases if norm(a) in names), None)


def clock(value):
    m = re.fullmatch(r"(\d{1,2}):(\d{2})(?::(\d{2}(?:\.\d+)?))?", str(value).strip())
    if not m:
        return float("nan")
    h, minute, sec = int(m[1]), int(m[2]), float(m[3] or 0)
    return h + minute / 60 + sec / 3600 if h < 24 and minute < 60 and sec < 60 else float("nan")


def hhmm(hours):
    total = int(round(hours * 60))
    return f"{total // 60 % 24:02d}:{total % 60:02d}"


def rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{alpha})"


@st.cache_data(show_spinner=False, max_entries=8, ttl=3600)
def load_csv(payload):
    """Cache by bytes, preserve dropouts, reject malformed or excessive input."""
    if len(payload) > 25 * 1024 * 1024:
        raise ValueError("CSV exceeds the 25 MB dashboard limit.")
    df = pd.read_csv(BytesIO(payload), encoding="utf-8-sig", na_values=["null", "NULL", "N/A", "--"])
    if df.empty or len(df) > 250_000:
        raise ValueError("Supply 1–250,000 rows.")
    df.columns = df.columns.str.strip()
    if df.columns.duplicated().any() or any(c.startswith("__") for c in df):
        raise ValueError("Column names must be unique and must not start with '__'.")
    schema = {
        "sol": match(df, "Sol", "mission_sol"),
        "time": match(df, "LMST_Start", "LMST", "local_time"),
        "date": match(df, "UTC", "timestamp", "datetime", "date"),
        "site": match(df, "location", "station", "site", "rover"),
        "air": match(df, "Air_Temp_ATS_C", "Air_Temp_C", "air_temperature_c", "Air_Temp_TIRS_C"),
        "ground": match(df, "Ground_Temp_C", "surface_temperature_c"),
        "pressure": match(df, "Pressure_Pa", "atmospheric_pressure_pa"),
        "humidity": match(df, "Relative_Humidity_pct", "humidity_pct"),
        "up": match(df, "Upward_Shortwave_Irradiance"),
        "down": match(df, "Downward_Longwave_Irradiance"),
    }
    text_cols = {schema[k] for k in ("time", "date", "site") if schema[k]}
    for col in df:
        if col not in text_cols and col != "LMST_End":
            df[col] = pd.to_numeric(df[col], errors="coerce").replace([float("inf"), -float("inf"), -9999, -99999], float("nan"))
    df["__date"] = pd.to_datetime(df[schema["date"]], errors="coerce", utc=True) if schema["date"] else pd.NaT
    df["__hour"] = df[schema["time"]].map(clock) if schema["time"] else float("nan")
    if schema["sol"] and df[schema["sol"]].notna().any():
        df["__period"] = df[schema["sol"]]
        df["__x"] = df["__period"] + df["__hour"].fillna(0) / 24
    elif df["__date"].notna().any():
        df["__period"] = df["__date"].dt.strftime("%Y-%m-%d")
        df["__x"] = df["__date"]
    else:
        raise ValueError("A numeric Sol column or valid UTC/date/timestamp column is required.")
    df["__site"] = df[schema["site"]].fillna("Station").astype(str) if schema["site"] else "Station"
    df = df.dropna(subset=["__period"]).sort_values("__x", kind="stable").reset_index(drop=True)
    if df.empty:
        raise ValueError("No rows have a valid Sol/date.")
    return df, schema


DATA_FILE = "mars_sol_1740_combined_20min_sensor_averages(2).csv"
NOW_HOUR = 12.0
LATITUDE = 18.4446  # Jezero Crater


def sun_times(sol):
    """Sunrise/sunset in local mean solar time for the given Sol (Kepler orbit + hour angle)."""
    e, perihelion, year_sols = 0.0934, 251.0, 668.6
    nu0 = math.radians(5.2 - perihelion)
    e0 = 2 * math.atan2(math.sqrt(1 - e) * math.sin(nu0 / 2), math.sqrt(1 + e) * math.cos(nu0 / 2))
    mean = e0 - e * math.sin(e0) + 2 * math.pi * float(sol) / year_sols
    ecc = mean
    for _ in range(8):
        ecc = mean + e * math.sin(ecc)
    nu = 2 * math.atan2(math.sqrt(1 + e) * math.sin(ecc / 2), math.sqrt(1 - e) * math.cos(ecc / 2))
    ls = (math.degrees(nu) + perihelion) % 360
    dec = math.asin(math.sin(math.radians(25.19)) * math.sin(math.radians(ls)))
    lat = math.radians(LATITUDE)
    cos_h = (math.sin(math.radians(-0.35)) - math.sin(lat) * math.sin(dec)) / (math.cos(lat) * math.cos(dec))
    half_day = math.degrees(math.acos(max(-1.0, min(1.0, cos_h)))) / 15
    return 12 - half_day, 12 + half_day


def outlook(observed, col):
    """Damped continuation of the last hour's trend after 12:00 LMST."""
    current = observed.loc[observed["__hour"] == NOW_HOUR, col]
    if current.empty or pd.isna(current.iloc[-1]):
        return [], []
    valid = observed.dropna(subset=[col, "__hour"])
    recent = valid[valid["__hour"] >= NOW_HOUR - 1]
    slope = 0.0
    if len(recent) > 1:
        dt = recent["__hour"].iloc[-1] - recent["__hour"].iloc[0]
        if dt > 0:
            slope = (recent[col].iloc[-1] - recent[col].iloc[0]) / dt
    bound = max(float(valid[col].max() - valid[col].min()), 0.0) / 4
    slope = max(-bound, min(bound, slope))
    hours = [NOW_HOUR + i / 3 for i in range(37)]
    values = [float(current.iloc[-1]) + slope * 2 * (1 - math.exp(-(h - NOW_HOUR) / 2)) for h in hours]
    return hours, values


# ------------------------------------------------------------ outside health
# Levels: 0 = safe, 1 = caution, 2 = avoid.
LEVEL_NAMES = ["Safe for a walk", "Limit time outside", "Stay inside"]


def band(v, safe_range, caution_range):
    if safe_range[0] <= v <= safe_range[1]:
        return 0
    return 1 if caution_range[0] <= v <= caution_range[1] else 2


def assess(key, v, sunset=18.0):
    """Return (level, short status, advice) for one outside reading, or None without data."""
    if v is None or pd.isna(v):
        return None
    if key == "air":
        lv = band(v, (-35, 1e9), (-65, 1e9))
        return lv, ["Safe to walk", "Limit time", "Stay inside"][lv], [
            "Mild for Mars. Normal outing, check suit heaters before you go.",
            "Cold. Keep outings short and check suit heaters and battery.",
            "Extreme cold. Postpone any outing that isn't essential."][lv]
    if key == "ground":
        lv = band(v, (-50, 35), (-90, 60))
        return lv, ["Safe footing", "Check gear", "Avoid contact"][lv], [
            "Ground is within the range boots and tools are built for.",
            "Surface is cold or warm enough to stress boots and tools. Avoid long kneeling or resting hands on it.",
            "Surface temperature is beyond gear limits. Do not touch it with hands or tools."][lv]
    if key == "pressure":
        lv = 0 if 600 <= v <= 900 else 1
        return lv, ["Normal", "Unusual"][lv], [
            "Typical Mars pressure. A pressurized suit is always required outside.",
            "Outside the usual range, which can mean a weather change. Run a suit seal check before leaving."][lv]
    if key == "humidity":
        lv = 0 if v <= 70 else 1
        return lv, ["Dry and clear", "Frost risk"][lv], [
            "Dry air. No frost or visor fogging expected.",
            "Frost and fog are likely. Wipe the visor and watch for slippery surfaces and tools."][lv]
    if key == "light":
        if v < 30:
            return 1, "Low light", "Dim outside. Switch on suit lights and stay within sight of a partner."
        if v > 160:
            return 1, "Glare", "Bright surface. Use visor shading and rest your eyes between tasks."
        return 0, "Good light", "Clear visibility for walking and fine work."
    if key == "sky":
        lv = 0 if v >= 30 else 1 if v >= 15 else 2
        return lv, ["Normal heat", "Heat loss", "Severe heat loss"][lv], [
            "The sky returns normal heat. Suit heaters will manage.",
            "The sky is pulling heat from the suit. Keep moving and check heaters.",
            "Heat loss is very high. Stay near the airlock and keep outings very short."][lv]
    if key == "daylight":
        left = sunset - NOW_HOUR
        lv = 0 if left >= 3 else 1 if left >= 1.5 else 2
        return lv, ["Plenty of light", "Fading light", "Return now"][lv], [
            f"Daylight until {hhmm(sunset)}. Be back at base before sunset.",
            f"Light fades at {hhmm(sunset)}. Finish outside work and head back soon.",
            f"Sunset at {hhmm(sunset)}. Return to base now."][lv]
    return None


# Text per level [safe, caution, avoid]. None = nothing to show at that level.
EFFECTS = {
    "air": {
        "Heart rate": ["Steady", "Rises as the body works to stay warm", "Spikes under cold stress"],
        "HRV": ["Steady", "Drops under cold stress", "Drops sharply"],
        "Strength test": [None, "Keep it short, or grip will weaken", "Stay inside, or grip will drop sharply"],
    },
    "ground": {
        "Strength test": [None, "Limit ground contact, or grip will suffer", "Stay off it, or grip will be affected"],
        "Time outside": [None, "Skip long outings, or gear limits will cut them short", "Stay inside, or gear limits will cap outings"],
    },
    "pressure": {
        "Heart rate": ["Steady", "Suit pressure shifts raise effort", "Suit pressure shifts raise effort"],
        "VO₂ max": [None, "Avoid exertion outside, or VO₂ max will be affected", "Avoid exertion outside, or VO₂ max will be affected"],
        "Cognitive tests": [None, "Stay in, or mild decompression stress will slow reaction", "Stay in, or mild decompression stress will slow reaction"],
    },
    "humidity": {
        "Cognitive tests": [None, "Stay in, or a fogged visor will break focus", "Stay in, or a fogged visor will break focus"],
        "Strength test": [None, "Stay in, or frosted tools will lower grip", "Stay in, or frosted tools will lower grip"],
    },
    "light": {
        "Sleep": ["Body clock steady", "Odd light shifts the body clock", "Odd light shifts the body clock"],
        "Mental health": [None, "Stay in, or dim or harsh light will lower mood", "Stay in, or dim or harsh light will lower mood"],
        "Cognitive tests": [None, "Stay in, or glare and dimness will slow reaction", "Stay in, or glare and dimness will slow reaction"],
    },
    "sky": {
        "Heart rate": ["Steady", "Heat loss raises effort", "Heat loss raises effort sharply"],
        "HRV": ["Steady", "Cold load lowers HRV", "Cold load lowers HRV sharply"],
        "VO₂ max": [None, "Stay in, or oxygen burned for warmth will affect VO₂ max", "Stay in, or oxygen burned for warmth will sharply affect VO₂ max"],
    },
    "daylight": {
        "Sleep": ["Day cycle steady", "Late outings push bedtime back", "Dark outings disrupt sleep"],
        "Mental health": [None, "Come back soon, or fading light will lower mood", "Come back now, or darkness will lower mood"],
    },
}
TITLES = {
    "air": "Air temperature", "ground": "Ground temperature", "pressure": "Pressure",
    "humidity": "Humidity", "light": "Reflected light", "sky": "Sky infrared", "daylight": "Daylight",
}


def effect_rows(key, level):
    return [(name, texts[level]) for name, texts in EFFECTS[key].items() if texts[level]]


def tile_footer(key, level, tip):
    rows = "".join(
        f'<div class="fx"><i class="d l{level}"></i><b>{safe(name)}</b><span>{safe(text)}</span></div>'
        for name, text in effect_rows(key, level)
    )
    block = f'<div class="fxs">{rows}</div>' if rows else ""
    return f'<div class="tip">{safe(tip)}</div>{block}'


# ------------------------------------------------------------ base life support
STATION = [
    dict(key="o2", label="Oxygen", unit="%", lo=15, hi=25, safe=(19.5, 23.5), caution=(18, 25), digits=1),
    dict(key="co2", label="Carbon dioxide", unit="ppm", lo=0, hi=6000, safe=(0, 4000), caution=(0, 5000), digits=0),
    dict(key="humidity", label="Cabin humidity", unit="%", lo=0, hi=100, safe=(35, 60), caution=(25, 70), digits=0),
    dict(key="pressure", label="Cabin pressure", unit="kPa", lo=90, hi=110, safe=(97, 104), caution=(94, 106), digits=1),
    dict(key="temp", label="Cabin temperature", unit="°C", lo=10, hi=35, safe=(18, 27), caution=(15, 30), digits=1),
    dict(key="water", label="Water reserve", unit="%", lo=0, hi=100, safe=(30, 100), caution=(15, 100), digits=0),
    dict(key="power", label="Power reserve", unit="%", lo=0, hi=100, safe=(30, 100), caution=(15, 100), digits=0),
    dict(key="radiation", label="Radiation inside", unit="µSv/h", lo=0, hi=60, safe=(0, 25), caution=(0, 40), digits=0),
]
def station_values(sol):
    """Base life-support readings. Nominal values with small sol-to-sol drift."""
    try:
        s = float(sol)
    except (TypeError, ValueError):
        s = 0.0
    return {
        "o2": 20.9 + 0.2 * math.sin(s * 1.3),
        "co2": 2800 + 350 * math.sin(s * 0.7),
        "humidity": 46 + 4 * math.sin(s * 0.9),
        "pressure": 101.2 + 0.4 * math.sin(s * 1.1),
        "temp": 22.4 + 0.6 * math.sin(s * 0.5),
        "water": 78 + 3 * math.sin(s * 0.3),
        "power": 86 + 4 * math.sin(s * 0.4),
        "radiation": 14 + 2 * math.sin(s * 0.8),
    }


def gauge_svg(value_text, unit, frac, safe_frac, level):
    """270° ring gauge: filled value arc, outer band marks the safe range."""
    cx = cy = 65
    r, rb = 46, 57
    circ, circ_b = 2 * math.pi * r, 2 * math.pi * rb
    arc, arc_b = circ * 0.75, circ_b * 0.75
    color = LEVEL_COLORS[level]
    start_b, len_b = arc_b * safe_frac[0], arc_b * max(safe_frac[1] - safe_frac[0], 0.001)
    theta = math.radians(135 + 270 * frac)
    mx, my = cx + r * math.cos(theta), cy + r * math.sin(theta)
    return (
        f'<svg viewBox="0 0 130 130" role="img" aria-label="{safe(value_text)} {safe(unit)}">'
        f'<g transform="rotate(135 {cx} {cy})" fill="none">'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="#1C2126" stroke-width="9" stroke-linecap="round" stroke-dasharray="{arc:.1f} {circ:.1f}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{rb}" stroke="{rgba("#3DDC84", .55)}" stroke-width="3" stroke-dasharray="{len_b:.1f} {circ_b:.1f}" stroke-dashoffset="{-start_b:.1f}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{color}" stroke-width="9" stroke-linecap="round" stroke-dasharray="{max(arc * frac, 0.1):.1f} {circ:.1f}"/>'
        f'</g><circle cx="{mx:.1f}" cy="{my:.1f}" r="3.5" fill="#0C0E10"/>'
        f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" fill="#F2F4F5" font-size="27" font-weight="600" font-family="Barlow Condensed, Arial">{safe(value_text)}</text>'
        f'<text x="{cx}" y="{cy + 20}" text-anchor="middle" fill="#8A959D" font-size="11" font-family="Barlow, Arial">{safe(unit)}</text></svg>'
    )


def chart(day, col, unit, color, sunrise, sunset):
    observed = day.loc[day["__hour"] <= NOW_HOUR].copy()
    fig = go.Figure()
    valid = observed[col].notna()
    baseline = observed[col].min() if valid.any() else 0
    groups = (~valid).cumsum()
    for _, group in observed[valid].groupby(groups[valid]):
        fig.add_trace(go.Scatter(x=group["__hour"], y=[baseline] * len(group), mode="lines", line_width=0, hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(
            x=group["__hour"], y=group[col], mode="lines",
            line=dict(color=color, width=2.5, shape="spline", smoothing=.4),
            fill="tonexty", fillgradient=dict(type="vertical", colorscale=[[0, rgba(color, 0)], [1, rgba(color, .18)]]),
            hovertemplate="%{x:.2f} h<br>%{y:.2f} " + unit + "<extra></extra>", showlegend=False))
    hours, future = outlook(observed, col)
    if hours:
        fig.add_trace(go.Scatter(x=hours, y=future, mode="lines", line=dict(color=color, width=2, dash="dot", shape="spline"), opacity=.45,
                                 hovertemplate="%{x:.2f} h<br>%{y:.2f} " + unit + "<extra></extra>", showlegend=False))
        fig.add_trace(go.Scatter(x=[NOW_HOUR], y=[future[0]], mode="markers", marker=dict(size=10, color="#FFFFFF", line=dict(color=color, width=3)),
                                 hoverinfo="skip", showlegend=False))
    fig.add_vrect(x0=0, x1=sunrise, fillcolor="rgba(255,255,255,.035)", line_width=0)
    fig.add_vrect(x0=sunset, x1=24, fillcolor="rgba(255,255,255,.035)", line_width=0)
    fig.update_layout(height=110, margin=dict(l=0, r=0, t=8, b=18), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Barlow, Arial", size=11, color="#6E7A83"), hoverlabel=dict(bgcolor="#0C0E10"), dragmode=False)
    fig.update_xaxes(range=[0, 24], tickvals=[0, 6, 12, 18, 24], ticktext=["00", "06", "12", "18", "24"], showgrid=False, zeroline=False, fixedrange=True)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False, fixedrange=True)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False}, key=f"plot_{norm(col)}")


def main():
    with st.container(key="topbar"):
        brand, units = st.columns([5, 1])
        with brand:
            html('<div class="brand"><i></i>MARS STATION</div>')
        with units:
            with st.popover("Units", icon=":material/tune:"):
                tu = st.radio("Temperature", ["°C", "°F"], horizontal=True)
                pu = st.radio("Pressure", ["Pa", "mbar"], horizontal=True)
    try:
        df, schema = load_csv((Path(__file__).resolve().parent / DATA_FILE).read_bytes())
    except (ValueError, OSError, UnicodeError, pd.errors.ParserError) as exc:
        st.error(f"Place '{DATA_FILE}' beside app.py. Could not read data: {exc}")
        return

    frame = df[df["__site"] == df["__site"].iloc[0]]
    sol = frame["__period"].max()
    day = frame[frame["__period"] == sol].sort_values("__hour").copy()
    at_noon = day[day["__hour"] == NOW_HOUR]
    if at_noon.empty:
        st.error("No 12:00 LMST reading found in this file.")
        return
    row = at_noon.iloc[-1]
    observed = day[day["__hour"] <= NOW_HOUR]
    sol_label = int(sol) if isinstance(sol, (int, float)) and float(sol).is_integer() else sol
    try:
        sunrise, sunset = sun_times(sol)
    except (TypeError, ValueError):
        sunrise, sunset = 6.0, 18.0

    def temp(v):
        return v * 9 / 5 + 32 if tu == "°F" else v

    def raw(col):
        return row[col] if col else float("nan")

    # Outside assessment from raw (unconverted) readings.
    readings = {
        "air": raw(schema["air"]), "ground": raw(schema["ground"]), "pressure": raw(schema["pressure"]),
        "humidity": raw(schema["humidity"]), "light": raw(schema["up"]), "sky": raw(schema["down"]),
        "daylight": sunset,
    }
    ratings = {k: assess(k, v, sunset) for k, v in readings.items()}
    ratings = {k: r for k, r in ratings.items() if r}
    overall = max((r[0] for r in ratings.values()), default=0)
    drivers = [TITLES[k] for k, r in ratings.items() if r[0] == overall] if overall else []

    air_col = schema["air"]
    air = raw(air_col)
    low = observed[air_col].min() if air_col else float("nan")
    high = observed[air_col].max() if air_col else float("nan")
    span = high - low
    frac = 0.0 if pd.isna(span) or span <= 0 else max(0.0, min(1.0, (air - low) / span))

    r = 100
    circ = 2 * math.pi * r
    arc = circ * 0.75
    reason = "All readings in range" if not drivers else " · ".join(drivers)
    html(f'''<section class="hero"><div class="ring">
<svg viewBox="0 0 240 240"><circle cx="120" cy="120" r="{r}" fill="none" stroke="#1C2126" stroke-width="12" stroke-linecap="round" stroke-dasharray="{arc:.1f} {circ:.1f}"/>
<circle cx="120" cy="120" r="{r}" fill="none" stroke="{ACCENT}" stroke-width="12" stroke-linecap="round" stroke-dasharray="{max(arc*frac,0.1):.1f} {circ:.1f}"/></svg>
<div class="center"><div class="temp">{fmt(temp(air),0)}°</div></div></div>
<div class="place">Mars Station · Sol {safe(sol_label)}</div>
<div class="hl"><div><span>H</span>{fmt(temp(high),0)}°</div><div><span>L</span>{fmt(temp(low),0)}°</div></div>
<span class="pill verdict l{overall}">{LEVEL_NAMES[overall]}</span>
<div class="reason">{safe(reason)}</div></section>''')

    # Hourly temperature strip: measured to noon, trend after.
    if air_col:
        _, future = outlook(observed, air_col)
        cells = []
        for h in range(6, 19, 2):
            if h <= NOW_HOUR:
                hit = day.loc[day["__hour"] == h, air_col]
                val = hit.iloc[-1] if len(hit) else float("nan")
                cls = "hour now" if h == NOW_HOUR else "hour"
            else:
                idx = int((h - NOW_HOUR) * 3)
                val = future[idx] if future and idx < len(future) else float("nan")
                cls = "hour fc"
            label = "Now" if h == NOW_HOUR else f"{h:02d}:00"
            cells.append(f'<div class="{cls}"><div class="t">{label}</div><div class="v">{fmt(temp(val),0)}°</div></div>')
        html(f'<div class="strip">{"".join(cells)}</div>')

    # Base life support infographic.
    values = station_values(sol)
    gauges, station_levels = [], {}
    for g in STATION:
        v = values[g["key"]]
        level = band(v, g["safe"], g["caution"])
        station_levels[g["key"]] = level
        span_g = g["hi"] - g["lo"]
        f = max(0.0, min(1.0, (v - g["lo"]) / span_g))
        sf = (max(0.0, (g["safe"][0] - g["lo"]) / span_g), min(1.0, (g["safe"][1] - g["lo"]) / span_g))
        if g["key"] == "temp":
            shown, unit = temp(v), tu
            rng = f"{temp(g['safe'][0]):.0f}–{temp(g['safe'][1]):.0f} {unit}"
        else:
            shown, unit = v, g["unit"]
            rng = f"{g['safe'][0]:,.{g['digits']}f}–{g['safe'][1]:,.{g['digits']}f} {unit}"
        text = f"{shown:,.{g['digits']}f}"
        gauges.append(
            f'<div class="gg"><div class="gtop"><span class="label">{safe(g["label"])}</span><i class="d l{level}"></i></div>'
            f'{gauge_svg(text, unit, f, sf, level)}<div class="gr">Safe {safe(rng)}</div></div>')
    st_level = max(station_levels.values())
    html(f'<div class="section">Base life support<span class="pill l{st_level}">{["All systems nominal", "Check life support", "Life support alert"][st_level]}</span></div>')
    html(f'<div class="ggs">{"".join(gauges)}</div>')

    # Outside reading tiles with health guidance.
    html('<div class="section">Conditions outside</div>')
    cards = [
        ("air", schema["air"], tu, ACCENT),
        ("ground", schema["ground"], tu, COOL),
        ("pressure", schema["pressure"], pu, "#B7E36B"),
        ("humidity", schema["humidity"], "%", "#6FD3FF"),
        ("light", schema["up"], "W/m²", "#FFC857"),
        ("sky", schema["down"], "W/m²", ACCENT),
    ]
    cards = [c for c in cards if c[1]]
    for start in range(0, len(cards), 3):
        columns = st.columns(3)
        for column, (key, col, unit, color) in zip(columns, cards[start:start + 3]):
            with column, st.container(key=f"card_{key}"):
                display = day.copy()
                if col.lower().endswith("_c"):
                    display[col] = temp(display[col])
                elif col == schema["pressure"] and pu == "mbar":
                    display[col] = display[col] / 100
                reading = display.loc[at_noon.index[-1], col]
                digits = 2 if (col == schema["pressure"] and pu == "mbar") else (0 if col == schema["pressure"] else 1)
                rating = ratings.get(key)
                pill = f'<span class="pill l{rating[0]}">{safe(rating[1])}</span>' if rating else ""
                html(f'<div class="top"><span class="label">{safe(TITLES[key])}</span>{pill}</div>'
                     f'<div class="value">{fmt(reading, digits)}<span class="unit">{safe(unit)}</span></div>')
                chart(display, col, unit, color, sunrise, sunset)
                if rating:
                    html(tile_footer(key, rating[0], rating[2]))

    # Daylight tile: sunrise/sunset for this Sol, sun placed at the current time.
    dl = ratings["daylight"]
    with st.container(key="card_daylight"):
        text, arc_col = st.columns([1, 2])
        with text:
            length = sunset - sunrise
            html(f'<div class="top"><span class="label">Daylight</span><span class="pill l{dl[0]}">{safe(dl[1])}</span></div>'
                 f'<div class="value">{int(length)}h {int(round((length % 1) * 60)):02d}m</div>'
                 f'<div class="sun-meta"><div>Sunrise<b>{hhmm(sunrise)}</b></div><div>Sunset<b>{hhmm(sunset)}</b></div></div>')
        with arc_col:
            t_now = max(0.0, min(1.0, (NOW_HOUR - sunrise) / (sunset - sunrise)))
            pts = [(20 + 360 * i / 60, 130 - 95 * math.sin(math.pi * i / 60)) for i in range(61)]
            split = int(round(t_now * 60))
            past = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts[:split + 1])
            rest = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts[split:])
            sx, sy = 20 + 360 * t_now, 130 - 95 * math.sin(math.pi * t_now)
            html(f'<svg viewBox="0 0 400 160" role="img" aria-label="Sun position at noon, sunrise {hhmm(sunrise)}, sunset {hhmm(sunset)}">'
                 f'<line x1="10" y1="130" x2="390" y2="130" stroke="#2A3137" stroke-width="2"/>'
                 f'<polyline points="{rest}" fill="none" stroke="#3A4249" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 7"/>'
                 f'<polyline points="{past}" fill="none" stroke="#FFC857" stroke-width="3" stroke-linecap="round"/>'
                 f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="11" fill="#FFC857"/>'
                 f'<text x="20" y="152" fill="#8A959D" font-size="13" font-family="Barlow, Arial">{hhmm(sunrise)}</text>'
                 f'<text x="380" y="152" fill="#8A959D" font-size="13" text-anchor="end" font-family="Barlow, Arial">{hhmm(sunset)}</text></svg>')
        html(tile_footer("daylight", dl[0], dl[2]))


if __name__ == "__main__":
    main()