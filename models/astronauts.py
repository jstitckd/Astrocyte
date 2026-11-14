"""Building names and icons used by the sidebar and blank page titles."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Astronaut:
    name: str
    icon: str
    role: str


Astronauts = {
    "Alex": Astronaut("Alex Vance", "76", "Pilot"),
    "Petrov": Astronaut("Petrov Volkov", "90", "Commander"),
    "Amara": Astronaut("Dr. Amara Okafor", "97" ,"Medical Officer"),
    "Milou": Astronaut("Milou de Jong", "0", "Lead Engineer"),
    # "Four": Astronaut("Greenhouse / common room", "❋"),
}
