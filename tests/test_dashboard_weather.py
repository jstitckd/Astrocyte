"""Validate the supplied CSV's values, units and scope on the homepage."""
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest

from services.dashboard_weather import WEATHER_PATH, weather_snapshot

ROOT = Path(__file__).resolve().parents[1]


class DashboardWeatherTests(unittest.TestCase):
    def test_noon_snapshot_uses_supplied_outside_readings(self):
        snapshot = weather_snapshot(WEATHER_PATH.read_bytes())
        self.assertEqual(snapshot.time, "12:00")
        for key, value, unit in (("air", -32, "°C"), ("pressure", 504.8, "Pa"), ("uv_index", 51, "UV index")):
            self.assertEqual(snapshot.readings[key].value, value)
            self.assertEqual(snapshot.readings[key].unit, unit)
            self.assertEqual(snapshot.readings[key].source, "csv")
        self.assertEqual(snapshot.readings["o2"].source, "demo")
        self.assertEqual(snapshot.readings["co2"].source, "demo")
        self.assertNotIn("cabin_radiation", snapshot.readings)
        self.assertEqual(len(snapshot.history["air"]), 25)
        self.assertEqual(snapshot.history["uv_index"][12], ("12:00", 51))
        self.assertEqual(snapshot.history["pressure"][-1], ("24:00", 506.5))
        self.assertEqual(len(snapshot.history["o2"]), 1)

    def test_day_endpoint_and_missing_values_are_not_fabricated(self):
        midnight = weather_snapshot(WEATHER_PATH.read_bytes(), "24:00")
        self.assertEqual(midnight.readings["uv_index"].value, 0)
        missing = weather_snapshot(b"Time,Temperature_C,Pressure_Pa,UV_Index\n12:00,,0,-1\n")
        for key in ("air", "pressure", "uv_index"):
            self.assertIsNone(missing.readings[key].value)
        with self.assertRaises(ValueError):
            weather_snapshot(b"Time,Temperature_C,Pressure_Pa,UV_Index\n11:00,-20,500,1\n")

    def test_dashboard_displays_uv_and_outside_units(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
        self.assertFalse(app.exception)
        markup = "\n".join(item.proto.body for item in app.get("html")) + "\n" + "\n".join(item.value for item in app.markdown)
        self.assertIn("Radiation · UV", markup)
        self.assertIn("Outside temperature", markup)
        self.assertIn("Outside pressure", markup)
        self.assertIn("504.8 <span>Pa</span>", markup)
        self.assertIn("-32.0 <span>°C</span>", markup)
        self.assertIn("51 <span>UV index</span>", markup)
        self.assertNotIn("µSv/h", markup)
        self.assertEqual(markup.count('class="env-gauge"'), 5)
        self.assertEqual(markup.count('role="meter"'), 5)
        self.assertNotIn('class="env-sparkline"', markup)
        self.assertNotIn('class="dash-icon"', markup)
        labels = ("Radiation · UV", "Outside temperature", "Outside pressure", "Cabin O₂", "Cabin CO₂")
        positions = [markup.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))
