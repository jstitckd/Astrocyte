"""Compact HTML/CSS gauges for the homepage environmental panel."""
from html import escape
import math

from services.environment_colours import GAUGE_SCALES


def gauge(channel, value, unit, status):
    scale = GAUGE_SCALES[channel]
    span = scale.maximum - scale.minimum
    valid = value is not None and math.isfinite(value)
    boundaries = (scale.minimum, scale.low, scale.high, scale.maximum)
    widths = [(right - left) / span * 100 for left, right in zip(boundaries, boundaries[1:])]
    labels = []
    for width, label in zip(widths, scale.labels):
        labels.append(f'<span style="width:{width:.4f}%">{label}</span>')
    stops = ",".join(f"{colour} {(at - scale.minimum) / span * 100:.4f}%" for at, colour in scale.gradient_stops())
    background = f"linear-gradient(90deg,{stops})"
    marker = ""
    if valid:
        clamped = min(scale.maximum, max(scale.minimum, value))
        position = (clamped - scale.minimum) / span * 100
        marker = f'<span class="env-gauge-marker" style="left:{position:.4f}%"></span>'
        text = escape(f"{value:g} {unit}: {status}. Display scale {scale.minimum:g} to {scale.maximum:g} {unit}", quote=True)
        semantics = f'role="meter" aria-label="{channel.replace("_", " ")} display gauge" aria-valuemin="{scale.minimum:g}" aria-valuemax="{scale.maximum:g}" aria-valuenow="{clamped:g}" aria-valuetext="{text}"'
    else:
        semantics = 'role="img" aria-label="No measurement available"'
    tooltip = escape(f"Display bands: low below {scale.low:g}; middle band {scale.low:g}–{scale.high:g}; high above the middle band. Units: {unit}.", quote=True)
    upper = f"{scale.maximum:g}+" if channel == "uv_index" or valid and value > scale.maximum else f"{scale.maximum:g}"
    empty = " empty" if not valid else ""
    return f'<div class="env-gauge{empty}" {semantics} title="{tooltip}"><div class="env-gauge-track" style="background:{background}">{marker}</div><div class="env-gauge-labels">{"".join(labels)}</div><div class="env-gauge-range"><span>{scale.minimum:g}</span><span>{upper}</span></div></div>'
