import json
import unittest

from services.demo import demo_readings
from services.ingestion import DataValidationError, readings_csv
from services.storage import SessionStore


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.state = {}
        self.store = SessionStore(self.state)

    def test_checkins_are_scoped_and_do_not_become_measurements(self):
        record = self.store.save_checkin("crew-01", "wellbeing", "2026-11-14", "demo", {"mood": 4, "stress": 2, "notes": "Settling in"})
        self.assertIn("+00:00", record["created_at"])
        self.assertEqual(len(self.store.checkins("demo", "crew-01", "2026-11-01", "2026-11-14")), 1)
        for dataset, crew, start, end, area in [
            ("csv-new", "crew-01", "2026-11-01", "2026-11-14", None),
            ("demo", "crew-02", "2026-11-01", "2026-11-14", None),
            ("demo", "crew-01", "2026-11-01", "2026-11-13", None),
            ("demo", "crew-01", "2026-11-01", "2026-11-14", "sleep"),
        ]:
            self.assertEqual(self.store.checkins(dataset, crew, start, end, area), [])
        self.assertIsNone(self.state["imported"])
        self.assertEqual(len(json.loads(self.store.export_json())["checkins"]), 1)

    def test_validation_happens_before_save(self):
        cases = [
            ("sleep", {"notes": "   "}),
            ("nutrition", {"fluid_ml": 0, "energy_kcal": 0, "notes": ""}),
            ("nutrition", {"fluid_ml": -1}),
            ("wellbeing", {"mood": 6, "stress": 2}),
            ("wellbeing", {"mood": True, "stress": 2}),
            ("medical", {"symptoms": ["No symptoms to report", "Fatigue"]}),
            ("medical", {"symptoms": []}),
            ("sleep", {"health_score": 90, "notes": "test"}),
        ]
        for area, fields in cases:
            with self.subTest(area=area, fields=fields), self.assertRaises(ValueError):
                self.store.save_checkin("crew-01", area, "2026-11-14", "demo", fields)
        self.assertEqual(self.state["checkins"], [])

    def test_task_completion_is_scoped_and_survives_reruns(self):
        scope = ("demo", "crew-01", "2026-11-14", "sleep", "review")
        self.store.set_task(*scope, True)
        again = SessionStore(self.state)
        self.assertTrue(again.task_done(*scope))
        for dataset, crew, day in [("csv-new", "crew-01", "2026-11-14"), ("demo", "crew-02", "2026-11-14"), ("demo", "crew-01", "2026-11-13")]:
            self.assertFalse(again.task_done(dataset, crew, day, "sleep", "review"))
        exported = json.loads(self.store.export_json())["tasks"][0]
        self.assertEqual(exported["date"], "2026-11-14")
        self.assertTrue(exported["completion"]["review"])

    def test_failed_import_preserves_last_valid_dataset(self):
        content = readings_csv(demo_readings())
        self.store.import_readings(content, "good.csv")
        original_id = self.state["imported_id"]
        with self.assertRaises(DataValidationError):
            self.store.import_readings(b"bad,headers\n1,2", "bad.csv")
        self.assertEqual(self.state["imported_id"], original_id)
        self.assertEqual(len(self.state["imported"]), 462)
        self.store.import_readings(content, "same-data-new-name.csv")
        self.assertEqual(self.state["imported_id"], original_id)

    def test_custom_eva_checklist_and_fresh_session(self):
        self.store.configure_eva("crew-01", "Inspect suit\nConfirm comms")
        self.assertEqual(self.store.eva_tasks("crew-01"), ["Inspect suit", "Confirm comms"])
        self.assertNotEqual(self.store.eva_tasks("crew-01"), self.store.eva_tasks("crew-02"))
        for invalid in ["", "duplicate\nduplicate", "x" * 161]:
            with self.assertRaises(ValueError):
                self.store.configure_eva("crew-01", invalid)
        self.assertEqual(SessionStore({}).state["checkins"], [])


if __name__ == "__main__":
    unittest.main()
