from unittest import TestCase

from . import day03


class Part1Test(TestCase):
    def test_example1(self):
        data = ('''R75,D30,R83,U83,L12,D49,R71,U7,L72\n'''
                '''U62,R66,U55,R34,D71,R55,D58,R83''').splitlines()
        self.assertEqual(day03.part1(day03.Grid.from_data(data)), 159)

    def test_example2(self):
        data = ('''R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n'''
                '''U98,R91,D20,R16,D67,R40,U7,R15,U6,R7''').splitlines()
        self.assertEqual(day03.part1(day03.Grid.from_data(data)), 135)


class Part2Test(TestCase):
    def test_example1(self):
        data = ('''R75,D30,R83,U83,L12,D49,R71,U7,L72\n'''
                '''U62,R66,U55,R34,D71,R55,D58,R83''').splitlines()
        self.assertEqual(day03.part2(day03.Grid.from_data(data)), 610)

    def test_example2(self):
        data = ('''R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n'''
                '''U98,R91,D20,R16,D67,R40,U7,R15,U6,R7''').splitlines()
        self.assertEqual(day03.part2(day03.Grid.from_data(data)), 410)
