"""Shared environmental reading type and deterministic cabin demo values."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Reading:
    value: float | None
    unit: str
    source: str  # csv, demo or missing
    note: str = ""


def station_values(sol):
    """Synthetic cabin scenario for the demo dashboard. These are not sensor readings."""
    sol = float(sol)
    return {
        "o2": 20.9 + 0.2 * math.sin(sol * 1.3),
        "co2": 2800 + 350 * math.sin(sol * 0.7),
    }
