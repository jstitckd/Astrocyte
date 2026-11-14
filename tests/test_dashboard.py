"""Integration checks for in-app task notifications and crew summaries."""
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class DashboardTests(unittest.TestCase):
    def test_overview_has_five_channels_and_real_crew_csv_values(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        self.assertFalse(app.exception)
        markup = "\n".join(item.proto.body for item in app.get("html"))
        self.assertEqual(markup.count('class="dash-metric"'), 5)
        self.assertIn("Cabin O₂", markup)
        self.assertNotIn("Recorded weather", markup)
        self.assertNotIn('class="dash-outside"', markup)
        self.assertNotIn("<small>Demo</small>", markup)
        self.assertIn("Sleep score", markup)
        self.assertNotIn("Synthetic telemetry", markup)
        self.assertEqual(len([button for button in app.button if button.key.startswith("complete_")]), 3)

    def test_task_notification_completion_and_navigation_persist(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        app.session_state["mars_base_map"] = {"area": "science", "task": "medical-check", "event_id": "task-notification"}
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.page, "home")
        self.assertEqual(app.session_state.selected_habitat_task, "medical-check")
        app.button(key="complete_medical-check").click().run()
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


if __name__ == "__main__":
    unittest.main()
