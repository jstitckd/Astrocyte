"""Building names and icons used by the sidebar and blank page titles."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Astronaut:
    name: str
    icon: str
    role: str


Astronauts = {
    "Alex": Astronaut("Alex Vance", "73", "Pilot"),
    "Petrov": Astronaut("Petrov Volkov", "91", "Commander"),
    # "Two": Astronaut("Medical bay", "✚"),
    # "Three": Astronaut("Kitchen", "◒"),
    # "Four": Astronaut("Greenhouse / common room", "❋"),
}
