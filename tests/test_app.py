"""Navigation checks for the seven-zone map and the team's existing routes."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

from models.areas import HABITAT_AREAS

ROOT = Path(__file__).resolve().parents[1]


def new_app():
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=20).run()


class NavigationTests(unittest.TestCase):
    def test_blank_destination_pages_remain_renderable(self):
        app = new_app()
        expected_titles = {
            "home": "Dashboard",
            "sleep": "Sleeping quarters",
            "medical": "Medical bay",
            "nutrition": "Kitchen",
            "wellbeing": "Greenhouse / common room",
            "eva": "Airlock / EVA area",
            "data": "Data & exports",
            **{area_id: area.name for area_id, area in HABITAT_AREAS.items()},
        }
        self.assertFalse(app.exception)
        for page_id, title in expected_titles.items():
            with self.subTest(page=page_id):
                # Habitat routes are reached from the map, not the crew sidebar.
                app.session_state.page = page_id
                app.run()
                self.assertFalse(app.exception)
                self.assertEqual([item.value for item in app.main.title], [title])
                if page_id != "home":
                    # The shared sidebar injects a style block into the main tree.
                    content = [item for item in app.main.markdown if not item.value.lstrip().startswith("<style>")]
                    self.assertEqual(len(content), 0)
                    self.assertEqual(len(app.metric), 0)
                    self.assertEqual(len(app.get("file_uploader")), 0)
                    self.assertEqual(len(app.get("download_button")), 0)

    def test_crew_sidebar_and_return_home_still_work(self):
        app = new_app()
        app.button(key="nav_Alex").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.page, "Alex")
        app.button(key="nav_home").click().run()
        self.assertEqual(app.title[0].value, "Dashboard")
        self.assertFalse(app.exception)

    def test_map_opens_each_page_and_does_not_replay_on_return(self):
        for area_id, area in HABITAT_AREAS.items():
            with self.subTest(area=area_id):
                app = new_app()
                app.session_state["mars_base_map"] = {"area": area_id, "event_id": "test-" + area_id}
                app.run()
                self.assertFalse(app.exception)
                self.assertEqual(app.session_state.page, area_id)
                self.assertEqual(app.title[0].value, area.name)
                app.button(key="nav_home").click().run()
                self.assertFalse(app.exception)
                self.assertEqual(app.session_state.page, "home")

    def test_invalid_map_events_leave_homepage_open(self):
        events = (
            {"area": "unknown", "event_id": "x"},
            {"area": [], "event_id": "x"},
            {"area": "living"},
            {"area": "living", "event_id": 1},
            {"area": "living", "event_id": ""},
            {"area": "sleep", "event_id": "old-map-area"},
        )
        for event in events:
            with self.subTest(event=event):
                app = new_app()
                app.session_state["mars_base_map"] = event
                app.run()
                self.assertFalse(app.exception)
                self.assertEqual(app.session_state.page, "home")

    def test_svg_regions_match_the_python_registry(self):
        class RegionParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.regions = []

            def handle_starttag(self, tag, attrs):
                attributes = dict(attrs)
                if tag == "g" and "building" in attributes.get("class", "").split():
                    self.regions.append(attributes.get("data-area"))
                    self.assert_accessible(attributes)

            @staticmethod
            def assert_accessible(attributes):
                assert attributes.get("role") == "button"
                assert attributes.get("tabindex") == "0"

        parser = RegionParser()
        parser.feed((ROOT / "frontend/map/index.html").read_text())
        self.assertEqual(len(parser.regions), 7)
        self.assertEqual(set(parser.regions), set(HABITAT_AREAS))

    def test_unknown_page_returns_to_home(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20)
        app.session_state["page"] = "removed-page"
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.page, "home")


if __name__ == "__main__":
    unittest.main()
