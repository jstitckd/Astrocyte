"""Measured/demo provenance, snapshot gaps, units and homepage integration."""
from pathlib import Path
import unittest

import pandas as pd
from streamlit.testing.v1 import AppTest

from components.environment_charts import history_figure
from services.environment import DEFAULT_DATA_PATH, Reading, clock, converted, load_csv, take_snapshot

ROOT = Path(__file__).resolve().parents[1]


class EnvironmentDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frame, cls.schema = load_csv(DEFAULT_DATA_PATH.read_bytes())

    def test_actual_weather_and_unmeasured_channels(self):
        snapshot = take_snapshot(self.frame, self.schema, 1740, "12:00")
        self.assertAlmostEqual(snapshot.readings["air"].value, -19.43264)
        self.assertAlmostEqual(snapshot.readings["pressure"].value, 663.94107)
        self.assertEqual(snapshot.readings["air"].source, "csv")
        self.assertEqual(snapshot.end_time, "12:20")
        for key in ("surface_radiation", "dose_total", "cabin_pm25", "dust", "perchlorate"):
            with self.subTest(key=key):
                self.assertIsNone(snapshot.readings[key].value)
                self.assertEqual(snapshot.readings[key].source, "missing")
        # Spectral/infrared irradiance columns in the same CSV are not dosimetry.
        self.assertIsNone(self.schema["surface_radiation"])

    def test_cabin_demo_is_explicit_and_can_be_disabled(self):
        demo = take_snapshot(self.frame, self.schema, 1740, "12:00", show_demo=True)
        recorded_only = take_snapshot(self.frame, self.schema, 1740, "12:00", show_demo=False)
        for key in ("o2", "co2", "cabin_temp", "cabin_pressure", "cabin_radiation"):
            self.assertEqual(demo.readings[key].source, "demo")
            self.assertIsNotNone(demo.readings[key].value)
            self.assertIsNone(recorded_only.readings[key].value)
        self.assertEqual(demo.readings["air"], recorded_only.readings["air"])

    def test_observation_dropouts_are_not_filled_or_replaced_by_last_reading(self):
        snapshot = take_snapshot(self.frame, self.schema, 1740, "09:20", show_demo=False)
        self.assertIsNone(snapshot.readings["air"].value)
        self.assertIsNone(snapshot.readings["pressure"].value)
        self.assertIn("observation", snapshot.readings["air"].note)
        self.assertIsNotNone(snapshot.air_range)

    def test_optional_recorded_channels_override_demo_and_preserve_their_gaps(self):
        content = b"Sol,LMST_Start,Cabin_O2_pct,Cabin_Radiation_uSv_h,Surface_Dust_mg_m3,Regolith_Perchlorate_wt_pct\n1740,12:00,21.2,3.5,0.04,0.6\n1740,12:20,,,,\n"
        frame, schema = load_csv(content)
        snapshot = take_snapshot(frame, schema, 1740, "12:00")
        self.assertEqual(snapshot.readings["o2"], Reading(21.2, "%", "csv"))
        self.assertEqual(snapshot.readings["cabin_radiation"].value, 3.5)
        self.assertEqual(snapshot.readings["dust"].source, "csv")
        self.assertEqual(snapshot.readings["perchlorate"].value, .6)
        gap = take_snapshot(frame, schema, 1740, "12:20")
        self.assertIsNone(gap.readings["o2"].value)
        self.assertEqual(gap.readings["o2"].source, "missing")

    def test_physical_invalid_values_stay_missing_without_health_classification(self):
        frame, schema = load_csv(b"Sol,LMST_Start,Air_Temp_ATS_C,Pressure_Pa,Cabin_O2_pct\n1740,12:00,-72,-1,101\n")
        snapshot = take_snapshot(frame, schema, 1740, "12:00")
        self.assertEqual(snapshot.readings["air"].value, -72)
        self.assertIsNone(snapshot.readings["pressure"].value)
        self.assertIsNone(snapshot.readings["o2"].value)

    def test_units_and_mars_clock(self):
        self.assertEqual(converted(Reading(-40, "°C", "csv"), "°F").value, -40)
        self.assertEqual(converted(Reading(1000, "Pa", "csv"), pressure_unit="mbar").value, 10)
        self.assertEqual(converted(Reading(None, "°C", "missing"), "°F").unit, "°F")
        self.assertIsNone(converted(Reading(None, "Pa", "missing"), pressure_unit="mbar").value)
        self.assertEqual(clock("12:20"), 12 + 20 / 60)
        self.assertTrue(pd.isna(clock("24:00")))

    def test_bad_files_and_ambiguous_snapshots_are_rejected(self):
        cases = (
            b"", b"bad,headers\n1,2\n", b"\xff", b"x" * (5 * 1024 * 1024 + 1),
            b"Sol,Sol,LMST_Start,Pressure_Pa\n1740,1740,12:00,600\n",
            b"Sol,LMST_Start,Pressure_Pa\n1740,12:00,600\n1740,12:00,700\n",
            b"Sol,LMST_Start,Pressure_Pa\n1740,29:00,600\n",
            b"Sol,LMST_Start,Pressure_Pa\n-1,12:00,600\n",
        )
        for content in cases:
            with self.subTest(size=len(content)), self.assertRaises(ValueError):
                load_csv(content)

    def test_recorded_chart_has_actual_gaps_and_no_forecast(self):
        snapshot = take_snapshot(self.frame, self.schema, 1740, "12:00")
        figure = history_figure(self.frame, self.schema, snapshot, "temperature")
        self.assertEqual(len(figure.data), 2)
        self.assertFalse(figure.data[0].connectgaps)
        self.assertEqual(sum(pd.isna(value) for value in figure.data[0].y), 4)
        self.assertEqual(len(figure.data[0].y), 72)
        self.assertEqual(figure.layout.shapes[0].x0, 12)


class EnvironmentHomepageTests(unittest.TestCase):
    def test_homepage_excludes_environment_and_keeps_map_navigation(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
        self.assertFalse(app.exception)
        body = "\n".join(element.proto.body for element in app.get("html"))
        self.assertNotIn("Environmental overview", body)
        self.assertNotIn('class="env-cards"', body)
        self.assertEqual(len(app.radio), 0)
        app.session_state["mars_base_map"] = {"area": "living", "event_id": "map-only-home"}
        app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.page, "living")


if __name__ == "__main__":
    unittest.main()
