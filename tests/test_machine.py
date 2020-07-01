import unittest
from coffee_machine import utils, models


class TestMachine(unittest.TestCase):
    def setUp(self) -> None:
        data = utils.get_last_saved_state("tests")
        self.machine = models.Machine(**data)

    def test_drink_serve(self):
        self.machine.serve_drink('hot_tea')
        self.assertFalse(self.machine.taps[0])
        self.assertEqual(self.machine.free_tap, 1)
        self.assertEqual(self.machine.available_ingredients['hot_water'], 300)
        self.assertEqual(self.machine.available_ingredients['hot_milk'], 400)
        self.assertEqual(self.machine.available_ingredients['ginger_syrup'], 90)
        self.assertEqual(self.machine.available_ingredients['sugar_syrup'], 90)
        self.assertEqual(self.machine.available_ingredients['tea_leaves_syrup'], 70)

    def test_add_ingredient(self):
        self.machine.add_ingredients(dict(green_mixture=1000))
        self.machine.add_ingredients(dict(random_ingredient=1000))
        self.machine.add_ingredients(dict(hot_water=10000))
        self.assertEqual(self.machine.available_ingredients['green_mixture'], 1000)
        self.assertEqual(self.machine.available_ingredients['random_ingredient'], 1000)
        self.assertGreaterEqual(self.machine.available_ingredients['hot_water'], 1000)
