"""Profile dialogs must use the right astronaut and never write test data."""
import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from models.astronauts import Astronauts
from services.astronaut_tools import profile_data, test_catalogue

ROOT = Path(__file__).resolve().parents[1]


class ProfileControlTests(unittest.TestCase):
    def test_profile_headers_are_rendered_before_any_charts(self):
        import importlib
        import streamlit as st

        for name in Astronauts:
            with self.subTest(astronaut=name):
                view = importlib.import_module(f"views.{name}")
                original_header = view.render_astronaut_header
                original_chart = st.plotly_chart
                events = []

                def header(*args, **kwargs):
                    events.append("header")
                    return original_header(*args, **kwargs)

                def chart(*args, **kwargs):
                    events.append("chart")
                    return original_chart(*args, **kwargs)

                app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
                app.session_state.page = name
                with patch.object(view, "render_astronaut_header", side_effect=header), patch.object(st, "plotly_chart", side_effect=chart):
                    app.run()
                self.assertFalse(app.exception)
                self.assertEqual(events[0], "header")
                self.assertEqual(events.count("header"), 1)
                self.assertIn("chart", events)

    def test_every_profile_has_summary_and_log_controls(self):
        for name, astronaut in Astronauts.items():
            with self.subTest(astronaut=name):
                app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
                app.session_state.page = name
                app.run()
                self.assertFalse(app.exception)
                self.assertIn("Log a test", app.button(key=f"profile_log_{name}").label)
                app.button(key=f"profile_summary_{name}").click().run()
                self.assertFalse(app.exception)
                markup = "\n".join(item.value for item in app.markdown)
                self.assertIn(f'class="dlg-title">{astronaut.name}</div>', markup)
                self.assertIn('class="dlg-list"', markup)
                self.assertIn("Overnight HRV", markup)
                self.assertIn('class="dlg-list rec"', markup)

    def test_catalogue_covers_recorded_measurements_not_derived_fields(self):
        for name in Astronauts:
            tests = test_catalogue(profile_data(name))
            fields = {test["id"] for test in tests}
            self.assertIn("dominant_handgrip_best_of_3_kgf", fields)
            self.assertIn("seated_leg_press_1rm_kg", fields)
            self.assertIn("heart_rate_bpm", fields)
            self.assertNotIn("astronaut", fields)
            self.assertNotIn("established_hrv_baseline_low_ms", fields)
        self.assertIn("ovulation_lh_test", {test["id"] for test in test_catalogue(profile_data("Amara"))})

    def test_log_validates_required_value_and_leaves_csvs_unchanged(self):
        paths = list((ROOT / "data").glob("*.csv"))
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
        # AppTest reruns the whole script instead of the live dialog fragment.
        app = AppTest.from_string("from components.astronaut_controls import test_log_dialog\ntest_log_dialog('Alex')", default_timeout=30).run()
        self.assertFalse(app.exception)
        submit = next(button for button in app.button if button.label == "Log measurement")
        submit.click().run()
        self.assertEqual(app.error[0].value, "Enter a measured value before submitting.")
        app.number_input(key="log_value_Alex_dominant_handgrip_best_of_3_kgf").set_value(42.5)
        next(button for button in app.button if button.label == "Log measurement").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.success[0].value, "Measurement logged — data is being processed.")
        self.assertEqual(before, {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths})
