"""One registry for navigation, map previews and daily tasks."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    id: str
    label: str


@dataclass(frozen=True)
class Area:
    name: str
    short_name: str
    code: str
    icon: str
    subtitle: str
    description: str
    metrics: tuple[str, ...]
    tasks: tuple[Task, ...]
    form: str


AREAS = {
    "sleep": Area("Sleeping quarters", "Sleep & recovery", "01", "☾",
        "Make room for recovery.", "Review overnight heart rate, HRV and sleep duration.",
        ("heart_rate", "hrv", "sleep_hours"),
        (Task("review", "Review overnight heart rate, HRV and sleep duration"),
         Task("observe", "Record recovery observations")), "sleep"),
    "exercise": Area("Exercise area", "Movement", "02", "↗",
        "Keep moving, one sol at a time.", "Review activity duration, exercise heart rate and exercise logs.",
        ("activity_minutes", "exercise_heart_rate"),
        (Task("review", "Review activity and exercise heart rate"),
         Task("log", "Log an exercise session")), "exercise"),
    "medical": Area("Medical bay", "Vitals & symptoms", "03", "✚",
        "A clearer picture of how you feel.", "Review available vital signs and complete a symptom check-in.",
        ("heart_rate", "spo2", "body_temperature"),
        (Task("review", "Review available vital signs"),
         Task("checkin", "Complete a symptom check-in")), "medical"),
    "nutrition": Area("Kitchen", "Food & hydration", "04", "◒",
        "Fuel for the journey ahead.", "Log fluid intake and meals; review daily fluid and energy totals.",
        ("fluid_ml", "energy_kcal"),
        (Task("review", "Review fluid and energy intake totals"),
         Task("log", "Log a meal or drink")), "nutrition"),
    "wellbeing": Area("Greenhouse / common room", "Mind & connection", "05", "❋",
        "A little space to check in.", "Complete mood and stress check-ins and review previous entries.",
        (), (Task("checkin", "Complete a mood and stress check-in"),
             Task("connect", "Make time for a crew connection")), "wellbeing"),
    "eva": Area("Airlock / EVA area", "Outside the habitat", "06", "◎",
        "Prepare for the world outside.", "Review EVA duration, recorded exposure and your pre-EVA checklist.",
        ("eva_minutes", "radiation_msv"),
        (Task("review", "Review EVA duration and recorded exposure"),), "eva"),
}

DEFAULT_EVA_TASKS = (
    "Review the mission-approved EVA procedure",
    "Confirm equipment checks with the crew",
    "Confirm the communications plan",
    "Review the return plan with the crew",
)
