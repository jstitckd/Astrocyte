"""Display bands must change colour at their configured boundaries."""
import unittest

from services.environment_colours import environment_colour, GREEN, AMBER, RED, BLUE, GREY


class EnvironmentalColourTests(unittest.TestCase):
    def test_uv_categories_and_missing_readings(self):
        for value, colour in ((0, GREEN), (2.9, GREEN), (3, AMBER), (5.9, AMBER), (6, RED), (8, RED), (11, RED), (51, RED)):
            self.assertEqual(environment_colour("uv_index", value)[0], colour)
        self.assertEqual(environment_colour("uv_index", 51)[1], "Extreme UV")
        for value in (None, float("nan"), float("inf")):
            self.assertEqual(environment_colour("uv_index", value)[0], GREY)

    def test_outside_and_cabin_channels_use_distinct_bands(self):
        self.assertEqual(environment_colour("air", -32)[0], BLUE)
        self.assertEqual(environment_colour("pressure", 504.8)[0], AMBER)
        for value in (19.5, 20.9, 23.5):
            self.assertEqual(environment_colour("o2", value)[0], GREEN)
        for value in (19.4, 23.6):
            self.assertEqual(environment_colour("o2", value)[0], RED)
        for value, colour in ((999, GREEN), (1000, AMBER), (2518, AMBER), (5000, RED)):
            self.assertEqual(environment_colour("co2", value)[0], colour)
