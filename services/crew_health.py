"""Shared sidebar and dashboard score values and ring colours."""
import re


def health_score(astronaut):
    """Read the score currently stored in astronaut.icon."""
    match = re.search(r"-?\d+(?:\.\d+)?", str(astronaut.icon))
    if match is None:
        return None

    return max(0.0, min(100.0, float(match.group())))


def score_colour(score):
    """Smoothly interpolate red -> yellow -> green."""
    stops = (
        (0, (239, 101, 101)),
        (50, (232, 200, 108)),
        (100, (102, 201, 143)),
    )

    for (low, start), (high, end) in zip(stops, stops[1:]):
        if score <= high:
            fraction = (score - low) / (high - low)
            channels = [
                round(a + (b - a) * fraction)
                for a, b in zip(start, end)
            ]
            return "#{:02x}{:02x}{:02x}".format(*channels)

    return "#66c98f"


