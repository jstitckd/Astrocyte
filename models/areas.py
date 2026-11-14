"""Building names and icons used by the sidebar and blank page titles."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Area:
    name: str
    icon: str


AREAS = {
    "sleep": Area("Sleeping quarters", "☾"),
    "exercise": Area("Exercise area", "↗"),
    "medical": Area("Medical bay", "✚"),
    "nutrition": Area("Kitchen", "◒"),
    "wellbeing": Area("Greenhouse / common room", "❋"),
    "eva": Area("Airlock / EVA area", "◎"),
}
