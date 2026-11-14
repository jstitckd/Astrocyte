"""Browser-session storage. No database, disk writes or shared-user records."""
from datetime import date, datetime, timezone
import hashlib
import json
import math
import uuid

from models.areas import AREAS, DEFAULT_EVA_TASKS


class SessionStore:
    def __init__(self, state):
        self.state = state
        defaults = {"checkins": [], "tasks": {}, "eva_lists": {}, "imported": None,
                    "imported_id": None, "imported_filename": None, "upload_error": None,
                    "page": "home", "last_map_event": None, "flash": None}
        for key, value in defaults.items():
            if key not in state:
                state[key] = value

    def import_readings(self, content, filename):
        from services.ingestion import load_csv

        # Parse first. A failed upload never overwrites the existing frame.
        frame = load_csv(content)
        dataset_id = "csv-" + hashlib.sha256(content).hexdigest()[:16]
        self.state["imported"] = frame
        self.state["imported_id"] = dataset_id
        self.state["imported_filename"] = filename
        self.state["upload_error"] = None
        return frame

    @staticmethod
    def _scope(dataset_id, crew_id, day, area):
        if area not in AREAS:
            raise ValueError("Unknown area.")
        return json.dumps([str(dataset_id), str(crew_id), str(day), area])

    def task_done(self, dataset_id, crew_id, day, area, task_id):
        scope = self._scope(dataset_id, crew_id, day, area)
        return self.state["tasks"].get(scope, {}).get(task_id, False)

    def set_task(self, dataset_id, crew_id, day, area, task_id, done):
        scope = self._scope(dataset_id, crew_id, day, area)
        self.state["tasks"].setdefault(scope, {})[str(task_id)] = bool(done)

    def eva_tasks(self, crew_id):
        return list(self.state["eva_lists"].get(crew_id, DEFAULT_EVA_TASKS))

    def configure_eva(self, crew_id, text):
        tasks = [line.strip() for line in text.splitlines() if line.strip()]
        if not 1 <= len(tasks) <= 12:
            raise ValueError("Enter between 1 and 12 checklist items, one per line.")
        if any(len(task) > 160 for task in tasks):
            raise ValueError("Keep each checklist item to 160 characters or fewer.")
        if len(set(tasks)) != len(tasks):
            raise ValueError("Each checklist item must be unique.")
        self.state["eva_lists"][crew_id] = tasks

    @staticmethod
    def eva_task_id(label):
        return "eva-" + hashlib.sha256(label.encode()).hexdigest()[:12]

    def save_checkin(self, crew_id, area, day, dataset_id, fields):
        self._scope(dataset_id, crew_id, day, area)
        try:
            observation_date = date.fromisoformat(str(day)).isoformat()
        except ValueError as exc:
            raise ValueError("Choose a valid observation date.") from exc
        if not isinstance(fields, dict):
            raise ValueError("Check-in fields must be a dictionary.")
        allowed = {
            "sleep": {"notes"}, "medical": {"symptoms", "notes"},
            "exercise": {"duration_minutes", "notes"},
            "nutrition": {"fluid_ml", "energy_kcal", "notes"},
            "wellbeing": {"mood", "stress", "notes"}, "eva": {"notes"},
        }
        if set(fields) - allowed[area]:
            raise ValueError("Unexpected fields for this check-in type.")
        clean = dict(fields)
        notes = str(clean.get("notes", "")).strip()
        if len(notes) > 2000:
            raise ValueError("Keep notes to 2,000 characters or fewer.")
        clean["notes"] = notes
        for key in ("fluid_ml", "energy_kcal", "duration_minutes"):
            if key in clean:
                value = clean[key]
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                    raise ValueError(f"{key} must be a non-negative finite number.")
        if area == "wellbeing":
            for key in ("mood", "stress"):
                if type(clean.get(key)) is not int or not 1 <= clean[key] <= 5:
                    raise ValueError("Mood and stress must each be an integer from 1 to 5.")
        elif area == "medical":
            symptoms = clean.get("symptoms", [])
            if not isinstance(symptoms, list) or len(symptoms) > 10 or any(not isinstance(item, str) or len(item) > 80 for item in symptoms):
                raise ValueError("Choose valid symptoms or describe them in the notes.")
            if not symptoms and not notes:
                raise ValueError("Select 'No symptoms to report', choose a symptom, or add a note.")
            if "No symptoms to report" in symptoms and len(symptoms) > 1:
                raise ValueError("Choose either 'No symptoms to report' or the symptoms you experienced.")
        elif area == "nutrition":
            if not notes and not (clean.get("fluid_ml", 0) or clean.get("energy_kcal", 0)):
                raise ValueError("Add a meal note, fluid amount or energy amount before saving.")
        elif not notes:
            raise ValueError("Add an observation or a note before saving.")
        record = {"id": str(uuid.uuid4()), "created_at": datetime.now(timezone.utc).isoformat(),
                  "date": observation_date, "crew_id": crew_id, "area": area,
                  "dataset_id": dataset_id, "fields": clean}
        self.state["checkins"].append(record)
        return record

    def checkins(self, dataset_id, crew_id, start_date, end_date, area=None):
        return [record for record in self.state["checkins"]
                if record["dataset_id"] == dataset_id and record["crew_id"] == crew_id
                and str(start_date) <= record["date"] <= str(end_date)
                and (area is None or record["area"] == area)]

    def export_json(self):
        payload = {"schema_version": 1, "exported_at": datetime.now(timezone.utc).isoformat(),
                   "storage": "session-only", "checkins": self.state["checkins"],
                   "tasks": [{"dataset_id": parts[0], "crew_id": parts[1], "date": parts[2],
                              "area": parts[3], "completion": tasks}
                             for scope, tasks in self.state["tasks"].items()
                             for parts in [json.loads(scope)]],
                   "eva_checklists": self.state["eva_lists"]}
        return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
