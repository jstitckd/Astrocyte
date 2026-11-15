"""Display bands must change colour at their configured boundaries."""
import unittest

from services.environment_colours import environment_colour, GREEN, AMBER, RED, BLUE, GREY


class EnvironmentalColourTests(unittest.TestCase):
    def test_uv_categories_and_missing_readings(self):
        for value, colour in ((0, GREEN), (2.9, GREEN), (3, AMBER), (5.9, AMBER), (6, RED), (8, RED), (11, RED), (51, RED)):
            self.assertEqual(environment_colour("uv_index", value)[0], colour)
        self.assertEqual(environment_colour("uv_index", 51)[1], "Extreme")
        for value in (None, float("nan"), float("inf")):
            self.assertEqual(environment_colour("uv_index", value)[0], GREY)

    def test_outside_and_cabin_channels_use_distinct_bands(self):
        self.assertEqual(environment_colour("air", -32)[0], GREEN)
        self.assertEqual(environment_colour("pressure", 504.8)[0], GREEN)
        for value, colour in ((-61, RED), (-60, GREEN), (-20, GREEN), (-19, RED)):
            self.assertEqual(environment_colour("air", value)[0], colour)
        for value, colour in ((499, RED), (500, GREEN), (600, GREEN), (601, RED)):
            self.assertEqual(environment_colour("pressure", value)[0], colour)
        for value in (19.5, 20.9, 23.5):
            self.assertEqual(environment_colour("o2", value)[0], GREEN)
        for value in (19.4, 23.6):
            self.assertEqual(environment_colour("o2", value)[0], RED)
        for value, colour in ((999, GREEN), (1000, AMBER), (2518, AMBER), (5000, RED)):
            self.assertEqual(environment_colour("co2", value)[0], colour)

    def test_gauge_clamps_pointer_but_keeps_actual_reading(self):
        from components.environment_gauge import gauge
        markup = gauge("uv_index", 51, "UV index", "Extreme")
        self.assertIn('aria-valuemax="12"', markup)
        self.assertIn('aria-valuenow="12"', markup)
        self.assertIn('aria-valuetext="51 UV index: Extreme.', markup)
        self.assertIn('left:100.0000%', markup)
        self.assertIn('>12+</span>', markup)

    def test_gradients_put_green_at_the_correct_preferred_values(self):
        from services.environment_colours import GAUGE_SCALES
        for key in ("air", "pressure", "o2"):
            scale = GAUGE_SCALES[key]
            stops = dict(scale.gradient_stops())
            self.assertEqual(stops[scale.minimum], RED)
            self.assertEqual(stops[scale.maximum], RED)
            self.assertEqual(stops[scale.low], GREEN)
            self.assertEqual(stops[scale.high], GREEN)
            self.assertIn(AMBER, stops.values())
        for key in ("uv_index", "co2"):
            scale = GAUGE_SCALES[key]
            stops = dict(scale.gradient_stops())
            self.assertEqual(stops[scale.minimum], GREEN)
            self.assertEqual(stops[scale.maximum], RED)

    def test_missing_gauge_does_not_imply_a_low_reading(self):
        from components.environment_gauge import gauge
        markup = gauge("o2", None, "%", "Not measured")
        self.assertNotIn('class="env-gauge-marker"', markup)
        self.assertNotIn('aria-valuenow=', markup)
        self.assertIn('aria-label="No measurement available"', markup)
