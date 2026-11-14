"""Configurable visual bands, not mission-certified alarms or exposure limits."""
import math

GREEN = "#72d7aa"
AMBER = "#ffd078"
RED = "#ff706b"
BLUE = "#78c9ef"
GREY = "#8a959d"

# Illustrative cabin display bands, not instantaneous safety judgements.
O2_DISPLAY_RANGE = (19.5, 23.5)
CO2_DISPLAY_BANDS = (1000, 5000)
LOW_OUTSIDE_PRESSURE_PA = 1000


def environment_colour(channel, value):
    if value is None or not math.isfinite(value):
        return GREY, "Not measured"
    if channel == "uv_index":
        # EPA category boundaries; high and higher are red in this UI.
        if value < 3:
            return GREEN, "Low UV"
        if value < 6:
            return AMBER, "Moderate UV"
        if value < 8:
            return RED, "High UV"
        if value < 11:
            return RED, "Very high UV"
        return RED, "Extreme UV"
    if channel == "air":
        return (BLUE, "Outside temperature below freezing") if value < 0 else (AMBER, "Outside temperature at or above freezing")
    if channel == "pressure":
        return (AMBER, "Low-pressure outside atmosphere") if value < LOW_OUTSIDE_PRESSURE_PA else (BLUE, "Outside atmospheric pressure")
    if channel == "o2":
        low, high = O2_DISPLAY_RANGE
        if value < low:
            return RED, "Cabin O₂ below display band"
        if value > high:
            return RED, "Cabin O₂ above display band"
        return GREEN, "Cabin O₂ within display band"
    if channel == "co2":
        elevated, high = CO2_DISPLAY_BANDS
        if value >= high:
            return RED, "Cabin CO₂ in high display band"
        if value >= elevated:
            return AMBER, "Cabin CO₂ in elevated display band"
        return GREEN, "Cabin CO₂ in lower display band"
    return GREY, "No display band configured"
