"""Smoke checks for the blank template's navigation."""
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class NavigationTests(unittest.TestCase):
    def test_all_pages_are_reachable_and_blank(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20).run()
        expected_titles = {
            "home": "Base overview",
            "sleep": "Sleeping quarters",
            "exercise": "Exercise area",
            "medical": "Medical bay",
            "nutrition": "Kitchen",
            "wellbeing": "Greenhouse / common room",
            "eva": "Airlock / EVA area",
            "data": "Data & exports",
        }
        self.assertFalse(app.exception)
        for page_id, title in expected_titles.items():
            with self.subTest(page=page_id):
                app.button(key="nav_" + page_id).click().run()
                self.assertFalse(app.exception)
                self.assertEqual([item.value for item in app.main.title], [title])
                self.assertEqual(len(app.main.markdown), 0)
                self.assertEqual(len(app.main.button), 0)
                self.assertEqual(len(app.metric), 0)
                self.assertEqual(len(app.get("plotly_chart")), 0)
                self.assertEqual(len(app.get("file_uploader")), 0)
                self.assertEqual(len(app.get("download_button")), 0)

    def test_unknown_page_returns_to_home(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20)
        app.session_state["page"] = "removed-page"
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["page"], "home")


if __name__ == "__main__":
    unittest.main()
