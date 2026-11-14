"""Building names and icons used by the sidebar and blank page titles."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Astronaut:
    name: str
    icon: str


Astronauts = {
    "Alex": Astronaut("Alex Vance", ""),
    "Petrov": Astronaut("Petrov Volkov", ""),
    # "Two": Astronaut("Medical bay", "✚"),
    # "Three": Astronaut("Kitchen", "◒"),
    # "Four": Astronaut("Greenhouse / common room", "❋"),
}
