"""Configurable gauge display bands, not certified mission alarm thresholds."""
from dataclasses import dataclass
import math

GREEN = "#72d7aa"
AMBER = "#ffd078"
RED = "#ff706b"
BLUE = "#78c9ef"
GREY = "#8a959d"
O2_DISPLAY_RANGE = (19.5, 23.5)
CO2_DISPLAY_BANDS = (1000, 5000)


@dataclass(frozen=True)
class GaugeScale:
    minimum: float
    low: float
    high: float
    maximum: float
    labels: tuple[str, str, str]
    colours: tuple[str, str, str]
    include_high_in_middle: bool = False

    def gradient_stops(self):
        """Keep the preferred band green and fade toward red at the extremes."""
        if self.colours[1] == GREEN:
            return (
                (self.minimum, RED),
                ((self.minimum + self.low) / 2, AMBER),
                (self.low, GREEN),
                (self.high, GREEN),
                ((self.high + self.maximum) / 2, AMBER),
                (self.maximum, RED),
            )
        return (
            (self.minimum, GREEN),
            (self.low, GREEN),
            ((self.low + self.high) / 2, AMBER),
            (self.high, RED),
            (self.maximum, RED),
        )

    def band(self, value):
        if value < self.low:
            return 0
        above_middle = value > self.high if self.include_high_in_middle else value >= self.high
        if above_middle:
            return 2
        return 1


# Outside ranges describe Mars conditions; "normal" does not mean breathable.
# Gas concentrations use illustrative cabin display bands, not dose/exposure limits.
GAUGE_SCALES = {
    "uv_index": GaugeScale(0, 3, 6, 12, ("Low", "Moderate", "High"), (GREEN, AMBER, RED)),
    "air": GaugeScale(-100, -60, -20, 20, ("Low", "Normal", "High"), (RED, GREEN, RED), True),
    "pressure": GaugeScale(350, 500, 600, 800, ("Low", "Normal", "High"), (RED, GREEN, RED), True),
    "o2": GaugeScale(18, *O2_DISPLAY_RANGE, 25, ("Low", "Normal", "High"), (RED, GREEN, RED), True),
    "co2": GaugeScale(0, *CO2_DISPLAY_BANDS, 6000, ("Low", "Elevated", "High"), (GREEN, AMBER, RED)),
}


def environment_colour(channel, value):
    if value is None or not math.isfinite(value):
        return GREY, "Not measured"
    scale = GAUGE_SCALES.get(channel)
    if scale is None:
        return GREY, "No display band configured"
    band = scale.band(value)
    label = scale.labels[band]
    if channel == "uv_index":
        label = "Extreme" if value >= 11 else "Very high" if value >= 8 else label
    return scale.colours[band], label
