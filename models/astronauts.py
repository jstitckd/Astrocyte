"""Building names and icons used by the sidebar and blank page titles."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Astronaut:
    name: str
    icon: str
    role: str


Astronauts = {
    "Alex": Astronaut("Alex Vance", "7.3", "Pilot"),
    "Petrov": Astronaut("Petrov Volkov", "9.1", "Commander"),
    # "Two": Astronaut("Medical bay", "✚"),
    # "Three": Astronaut("Kitchen", "◒"),
    # "Four": Astronaut("Greenhouse / common room", "❋"),
}
