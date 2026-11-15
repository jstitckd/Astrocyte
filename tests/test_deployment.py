"""Release portability and the public demo-data contract."""
from contextlib import chdir
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd
import streamlit as st
from streamlit.testing.v1 import AppTest

from models.astronauts import Astronauts

ROOT = Path(__file__).resolve().parents[1]


class DeploymentTests(unittest.TestCase):
    def test_profiles_can_load_data_outside_the_repository_working_directory(self):
        with TemporaryDirectory() as folder, chdir(folder):
            for crew_id in Astronauts:
                with self.subTest(crew=crew_id):
                    st.cache_data.clear()
                    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
                    app.session_state.page = crew_id
                    app.run()
                    self.assertFalse(app.exception)
                    self.assertIn(f"health_summary_{crew_id}", app.session_state)

    def test_bundled_crew_records_are_labelled_synthetic(self):
        for crew_id in Astronauts:
            files = list((ROOT / "data").glob(f"{crew_id.lower()}*.csv"))
            self.assertGreaterEqual(len(files), 4)
            for path in files:
                with self.subTest(file=path.name):
                    frame = pd.read_csv(path)
                    self.assertFalse(frame.empty)
                    labels = frame["data_type"].astype(str).str.lower()
                    self.assertTrue(labels.isin({"synthetic", "synthetic_nasa_calibrated"}).all())
