"""Integration checks for in-app task notifications and crew summaries."""
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class DashboardTests(unittest.TestCase):
    def test_overview_has_five_channels_and_real_crew_csv_values(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        self.assertFalse(app.exception)
        markup = "\n".join(item.proto.body for item in app.get("html")) + "\n" + "\n".join(item.value for item in app.markdown)
        self.assertEqual(markup.count('class="dash-metric"'), 5)
        self.assertIn("Cabin O₂", markup)
        self.assertNotIn("Recorded weather", markup)
        self.assertNotIn('class="dash-outside"', markup)
        self.assertNotIn("<small>Demo</small>", markup)
        self.assertIn("Sleep score", markup)
        self.assertNotIn("Synthetic telemetry", markup)
        self.assertIn("Amara", markup)
        from models.astronauts import Astronauts
        self.assertEqual(markup.count('class="crew-health-gauge"'), len(Astronauts))
        from services.crew_health import health_score
        for astronaut in Astronauts.values():
            score = health_score(astronaut)
            self.assertIn(f'aria-label="Health score {score:g}%"', markup)
        self.assertEqual(len([button for button in app.button if button.key.startswith("complete_")]), 3)

    def test_amara_dashboard_card_opens_existing_health_page(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        app.button(key="summary_Amara").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.page, "Amara")

    def test_task_notification_completion_and_navigation_persist(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        app.session_state["mars_base_map"] = {"area": "science", "task": "medical-check", "event_id": "task-notification"}
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.page, "task_guide")
        self.assertEqual(app.session_state.selected_habitat_task, "medical-check")
        self.assertEqual(app.title[0].value, "Medical check")
        app.button(key="finish_task_guide").click().run()
        self.assertFalse(app.exception)
        self.assertIn("medical-check", app.session_state.completed_habitat_tasks)
        self.assertEqual(len([button for button in app.button if button.key.startswith("complete_")]), 2)
        app.button(key="summary_Alex").click().run()
        self.assertEqual(app.session_state.page, "Alex")
        app.button(key="nav_home").click().run()
        self.assertEqual(app.session_state.page, "home")
        self.assertFalse(app.exception)
        self.assertEqual(len([button for button in app.button if button.key.startswith("complete_")]), 2)
        for task in ("sleep-check", "exercise-check"):
            app.button(key=f"complete_{task}").click().run()
        self.assertEqual(app.success[0].value, "All tasks completed.")

    def test_each_map_task_opens_its_guide_and_back_does_not_replay(self):
        from services.dashboard import SAMPLE_TASKS
        from models.task_guides import TASK_GUIDES
        for task in SAMPLE_TASKS:
            with self.subTest(task=task["id"]):
                app = AppTest.from_file(str(ROOT / "app.py")).run()
                app.session_state["mars_base_map"] = {"area": task["area"], "task": task["id"], "event_id": "guide-" + task["id"]}
                app.run()
                self.assertFalse(app.exception)
                self.assertEqual(app.session_state.page, "task_guide")
                self.assertEqual(app.title[0].value, task["title"])
                for title, _ in TASK_GUIDES[task["id"]]["steps"]:
                    self.assertTrue(any(title in item.value for item in app.markdown))
                app.button(key="task_back").click().run()
                self.assertEqual(app.session_state.page, "home")
                self.assertFalse(app.exception)

    def test_invalid_task_notification_stays_on_dashboard(self):
        for task_id, area in (("unknown", "living"), ([], "living"), ("sleep-check", "science")):
            with self.subTest(task=task_id):
                app = AppTest.from_file(str(ROOT / "app.py")).run()
                app.session_state["mars_base_map"] = {"area": area, "task": task_id, "event_id": "invalid-task"}
                app.run()
                self.assertFalse(app.exception)
                self.assertEqual(app.session_state.page, "home")


if __name__ == "__main__":
    unittest.main()
