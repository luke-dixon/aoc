from unittest import TestCase

from . import day04


class Part1Test(TestCase):
    def test_example1(self):
        self.assertEqual(day04.part1('11111-11111'), 1)

    def test_example2(self):
        self.assertEqual(day04.part1('223450-223450'), 0)

    def test_example3(self):
        self.assertEqual(day04.part1('123789-123789'), 0)


class Part2Test(TestCase):
    def test_example1(self):
        self.assertEqual(day04.part2('112233-112233'), 1)

    def test_example2(self):
        self.assertEqual(day04.part2('123444-123444'), 0)

    def test_example3(self):
        self.assertEqual(day04.part2('111122-111122'), 1)
