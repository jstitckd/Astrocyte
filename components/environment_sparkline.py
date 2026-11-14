"""Tiny inline SVG charts for environmental cards, without chart iframe overhead."""
from html import escape
import re


def sparkline(history, selected_time, label, unit, chart_id, accent="#d093f6"):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", accent):
        accent = "#d093f6"
    values = [value for _, value in history if value is not None]
    single = len(values) <= 1
    description = f"{label}: " + ("no readings available" if not values else "single snapshot; no history available" if single else f"hourly CSV profile; selected time {selected_time}; independently scaled")
    low, high = (min(values), max(values)) if values else (0, 1)
    padding = (high - low) * .15 if high > low else max(abs(low) * .02, 1)
    low, high = low - padding, high + padding
    points = []
    for at, value in history:
        hour, minute = map(int, at.split(":"))
        x = 4 + (hour + minute / 60) / 24 * 100
        y = 29 - (value - low) / (high - low) * 24 if value is not None else None
        points.append((at, value, x, y))
    gradient = "env-spark-" + chart_id
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" class="env-sparkline" width="108" height="36" viewBox="0 0 108 36" role="img" aria-label="{escape(description, quote=True)}" style="color:{accent}"><title>{escape(description)}</title><style>.env-spark-line{{fill:none;stroke:currentColor;stroke-width:1.7;stroke-linejoin:round;stroke-linecap:round}}.env-spark-selected{{fill:currentColor;stroke:#1b2327;stroke-width:1}}.env-spark-sample{{fill:transparent}}.env-spark-note{{fill:#a5afb4;font:8px sans-serif}}</style><defs><linearGradient id="{gradient}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="currentColor" stop-opacity=".23"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient></defs>']
    segments, segment = [], []
    for _, value, x, y in points:
        if value is None:
            if segment:
                segments.append(segment)
            segment = []
        else:
            segment.append((x, y))
    if segment:
        segments.append(segment)
    for segment in segments:
        if len(segment) < 2:
            continue
        path = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in segment)
        parts.append(f'<path class="env-spark-fill" d="{path} L{segment[-1][0]:.2f},34 L{segment[0][0]:.2f},34 Z" fill="url(#{gradient})"/><path class="env-spark-line" d="{path}"/>')
    for at, value, x, y in points:
        if value is None:
            continue
        selected = at == selected_time
        parts.append(f'<circle class="env-spark-{"selected" if selected else "sample"}" cx="{x:.2f}" cy="{y:.2f}" r="{2.6 if selected else 3}"><title>{escape(at)} · {value:g} {escape(unit)}</title></circle>')
    if single:
        note = "Snapshot only" if values else "Not measured"
        parts.append(f'<text class="env-spark-note" x="54" y="35" text-anchor="middle">{note}</text>')
    parts.append('</svg>')
    return ''.join(parts)
