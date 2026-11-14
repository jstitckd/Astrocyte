"""Habitat-map content and the team's original page-name definitions."""
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


@dataclass(frozen=True)
class HabitatArea:
    """Map content, shared by labels, the space guide and page titles."""

    code: str
    name: str
    label: str
    description: str
    features: tuple[str, ...]
    category: str


# Original AREAS above remain available to the team's existing pages.
HABITAT_AREAS = {
    "living": HabitatArea(
        "01", "Main living & working quarters", "Living & working",
        "The heart of the outpost: a shared place to rest, eat, plan missions and spend time with the crew.",
        ("Crew cabins", "Galley & common room", "Mission planning"), "Crew habitat",
    ),
    "life_support": HabitatArea(
        "02", "Environmental control & life support", "Life support",
        "The habitat's utility core, bringing air circulation, water recycling and environmental control together.",
        ("Air & oxygen", "Water recycling", "Climate control"), "Habitat systems",
    ),
    "science": HabitatArea(
        "03", "Science laboratories & maintenance workshops", "Science & workshops",
        "A connected research and engineering space for samples, experiments, repairs and equipment preparation.",
        ("Sample laboratory", "Engineering workshop", "Rover maintenance"), "Research & engineering",
    ),
    "exercise": HabitatArea(
        "04", "Exercise quarters", "Exercise quarters",
        "A dedicated crew training space for movement, conditioning and a break from the working day.",
        ("Cardio training", "Resistance training", "Recovery space"), "Crew wellbeing",
    ),
    "power": HabitatArea(
        "05", "Power generation & storage", "Solar & power",
        "An external solar array and battery station that connect to the habitat through a service conduit.",
        ("Solar arrays", "Battery storage", "Power distribution"), "Energy infrastructure",
    ),
    "greenhouse": HabitatArea(
        "06", "Greenhouse", "Greenhouse",
        "A glazed growing space for food cultivation, plant research and a little greenery far from Earth.",
        ("Growing beds", "Plant research", "Cultivation space"), "Food & cultivation",
    ),
    "launch": HabitatArea(
        "07", "Spaceship & launch area", "Spaceport",
        "A separate surface operations area with a lander, landing apron and access route back to the habitat.",
        ("Crew lander", "Landing apron", "Surface logistics"), "Surface operations",
    ),
}
