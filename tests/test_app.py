from datetime import date
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

from models.areas import AREAS
from services.demo import demo_readings
from services.navigation import destination

ROOT = Path(__file__).resolve().parents[1]


def app():
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()


def save_button(at):
    return next(button for button in at.button if button.label == "Save check-in")


class AppFlowTests(unittest.TestCase):
    def test_all_sidebar_routes_render_and_export_controls_exist(self):
        at = app()
        self.assertFalse(at.exception)
        for area in AREAS:
            at.button(key="nav_" + area).click().run()
            self.assertFalse(at.exception, area)
        at.button(key="nav_data").click().run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.get("download_button")), 3)

    def test_all_map_destinations_open_the_correct_dashboard(self):
        for area_id, area in AREAS.items():
            with self.subTest(area=area_id):
                at = app()
                at.session_state["mars_map"] = {"area": area_id, "event_id": "test-" + area_id}
                at.run()
                self.assertFalse(at.exception)
                self.assertEqual(at.session_state["page"], area_id)
                self.assertEqual(at.title[0].value, area.subtitle)
        self.assertIsNone(destination({"area": "sleep", "event_id": "same"}, "same"))
        for event in [None, [], {"area": "bad", "event_id": "x"}, {"area": [], "event_id": "x"}, {"area": "sleep"}]:
            self.assertIsNone(destination(event, None))

    def test_forms_save_and_task_completion_survives_navigation(self):
        at = app()
        at.button(key="nav_wellbeing").click().run()
        at.slider(key="mood").set_value(4)
        at.slider(key="stress").set_value(2)
        at.text_area(key="checkin_notes_wellbeing").input("Ready for the day")
        save_button(at).click().run()
        self.assertFalse(at.exception)
        self.assertEqual(at.session_state["checkins"][0]["fields"]["mood"], 4)
        at.checkbox[0].check().run()
        self.assertTrue(any(any(tasks.values()) for tasks in at.session_state["tasks"].values()))
        at.button(key="nav_home").click().run()
        self.assertIn("1 of", at.get("progress")[0].proto.text)
        at.button(key="nav_wellbeing").click().run()
        self.assertTrue(at.checkbox[0].value)

    def test_each_form_accepts_a_valid_entry_and_rejects_empty_notes(self):
        at = app()
        for area in ["sleep", "exercise", "medical", "nutrition", "eva"]:
            at.button(key="nav_" + area).click().run()
            if area == "medical":
                at.multiselect(key="symptoms").select("No symptoms to report")
            if area == "nutrition":
                at.number_input(key="nutrition_fluid").set_value(250)
            at.text_area(key="checkin_notes_" + area).input("An observation for the crew")
            save_button(at).click().run()
            self.assertFalse(at.exception, area)
            self.assertEqual(at.session_state["checkins"][-1]["area"], area)
        before = len(at.session_state["checkins"])
        at.button(key="nav_sleep").click().run()
        at.text_area(key="checkin_notes_sleep").input("")
        save_button(at).click().run()
        self.assertEqual(len(at.session_state["checkins"]), before)
        self.assertTrue(at.error)

    def test_crew_and_date_filters_and_empty_import_state(self):
        at = app()
        at.selectbox(key="crew_choice").select("crew-02").run()
        at.date_input(key="window_demo_crew-02").set_value((date(2026, 11, 4), date(2026, 11, 5))).run()
        self.assertFalse(at.exception)
        at.button(key="nav_data").click().run()
        displayed = at.dataframe[-1].value
        self.assertEqual(set(displayed.crew_id), {"crew-02"})
        self.assertEqual(len(displayed), 22)
        self.assertEqual(displayed.timestamp.min().date(), date(2026, 11, 4))
        at.selectbox(key="source_choice").select("Imported CSV").run()
        self.assertFalse(at.exception)
        self.assertTrue(at.info)
        at.button(key="nav_sleep").click().run()
        self.assertTrue(save_button(at).disabled)

    def test_imported_readings_reach_charts_and_cards(self):
        at = app()
        frame = demo_readings()
        frame = frame[frame.crew_id.eq("crew-03")].copy()
        frame["data_source"] = "test-import"
        at.session_state["imported"] = frame
        at.session_state["imported_id"] = "csv-test"
        at.session_state["imported_filename"] = "fixture.csv"
        at.selectbox(key="source_choice").select("Imported CSV").run()
        at.button(key="nav_medical").click().run()
        self.assertFalse(at.exception)
        self.assertEqual(at.selectbox(key="crew_choice").value, "crew-03")
        self.assertEqual(len(at.metric), 3)
        self.assertTrue(at.get("plotly_chart"))


if __name__ == "__main__":
    unittest.main()
