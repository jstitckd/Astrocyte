from datetime import date
from pathlib import Path
import unittest

import pandas as pd

from models.metrics import READING_COLUMNS
from services.adapters import read_adapter
from services.demo import demo_readings
from services.ingestion import DataValidationError, filter_readings, load_csv, readings_csv, validate_readings


class IngestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.demo = demo_readings()

    def test_sample_is_reproducible_and_round_trips(self):
        sample = Path(__file__).resolve().parents[1] / "data" / "sample_readings.csv"
        frame = load_csv(sample.read_bytes())
        pd.testing.assert_frame_equal(frame, self.demo)
        pd.testing.assert_frame_equal(load_csv(readings_csv(frame)), frame)
        self.assertEqual(len(frame), 462)
        self.assertEqual(list(frame), READING_COLUMNS)

    def test_utc_offsets_naive_dates_and_inclusive_window(self):
        rows = [
            {"timestamp": "2026-11-14T00:30:00+02:00", "crew_id": "crew-01", "metric": "heart_rate", "value": 60, "unit": "bpm", "data_source": "test"},
            {"timestamp": "2026-11-14T23:59:59", "crew_id": "crew-01", "metric": "heart_rate", "value": 61, "unit": "bpm", "data_source": "test"},
            {"timestamp": "2026-11-15T00:00:00Z", "crew_id": "crew-01", "metric": "heart_rate", "value": 62, "unit": "bpm", "data_source": "test"},
        ]
        frame = validate_readings(rows)
        self.assertEqual(frame.iloc[0].timestamp.day, 13)
        selected = filter_readings(frame, "crew-01", date(2026, 11, 14), date(2026, 11, 14))
        self.assertEqual(selected.value.tolist(), [61])
        self.assertTrue(filter_readings(frame, "another-crew", "2026-11-14", "2026-11-14").empty)
        with self.assertRaises(ValueError):
            filter_readings(frame, "crew-01", "2026-11-15", "2026-11-14")

    def test_validation_rejects_ambiguous_or_corrupt_input(self):
        baseline = self.demo[self.demo.metric.eq("heart_rate")].head(3).copy()
        cases = {}
        cases["missing column"] = baseline.drop(columns="data_source")
        cases["empty"] = baseline.iloc[:0]
        for name, col, value in [
            ("unknown metric", "metric", "health_score"), ("wrong unit", "unit", "beats"),
            ("non-numeric", "value", "bad"), ("infinite", "value", float("inf")),
            ("nan", "value", float("nan")), ("boolean", "value", True),
            ("invalid date", "timestamp", "2026-02-30T10:00:00Z"),
            ("ambiguous date", "timestamp", "11/14/2026"), ("numeric timestamp", "timestamp", 123),
            ("blank crew", "crew_id", " "), ("bad crew ID", "crew_id", "<script>"),
            ("missing source", "data_source", None), ("negative", "value", -1),
        ]:
            frame = baseline.astype(object).copy()
            frame.loc[0, col] = value
            cases[name] = frame
        cases["duplicate"] = baseline.iloc[[0, 0]]
        for name, frame in cases.items():
            with self.subTest(name=name), self.assertRaises(DataValidationError):
                validate_readings(frame)

    def test_rejects_duplicate_daily_total_at_different_times(self):
        row = self.demo[self.demo.metric.eq("fluid_ml")].iloc[[0]].copy()
        duplicate = row.copy()
        duplicate["timestamp"] = duplicate.timestamp - pd.Timedelta(hours=1)
        with self.assertRaisesRegex(DataValidationError, "Daily-total"):
            validate_readings(pd.concat([row, duplicate]))

    def test_csv_parse_errors_and_upload_limit(self):
        for content in [b"", b"wrong,headers\n1,2\n", b"\xff", b"a" * (5 * 1024 * 1024 + 1)]:
            with self.subTest(size=len(content)), self.assertRaises(DataValidationError):
                load_csv(content)

    def test_adapter_uses_the_same_boundary(self):
        demo = self.demo

        class DemoAdapter:
            def fetch(self):
                return demo

        pd.testing.assert_frame_equal(read_adapter(DemoAdapter()), demo)


if __name__ == "__main__":
    unittest.main()
