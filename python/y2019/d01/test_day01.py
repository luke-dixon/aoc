from unittest import TestCase

from . import day01


class CalcFuelTest(TestCase):
    def test_calc_fuel12(self):
        self.assertEqual(day01.calc_fuel(12), 2)

    def test_calc_fuel14(self):
        self.assertEqual(day01.calc_fuel(14), 2)

    def test_calc_fuel1969(self):
        self.assertEqual(day01.calc_fuel(1969), 654)

    def test_calc_fuel100756(self):
        self.assertEqual(day01.calc_fuel(100756), 33583)

    def test_calc_fuel12r(self):
        self.assertEqual(day01.calc_fuel(12, recursive=True), 2)

    def test_calc_fuel14r(self):
        self.assertEqual(day01.calc_fuel(14, recursive=True), 2)

    def test_calc_fuel1969r(self):
        self.assertEqual(day01.calc_fuel(1969, recursive=True), 966)

    def test_calc_fuel100756r(self):
        self.assertEqual(day01.calc_fuel(100756, recursive=True), 50346)


class Part1Test(TestCase):
    def test_small_list(self):
        self.assertEqual(day01.part1([132329, 98348, 99700]), 110118)


class Part2Test(TestCase):
    def test_small_list(self):
        self.assertEqual(day01.part2([132329, 98348, 99700]), 165088)
