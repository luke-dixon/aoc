from unittest import TestCase

from . import day02


class Test(TestCase):
    def test_example1(self):
        program = [int(x) for x in '1,9,10,3,2,3,11,0,99,30,40,50'.split(',')]
        self.assertEqual(
            day02.run_intcode_computer(program),
            [3500,9,10,70,2,3,11,0,99,30,40,50]
        )

    def test_small_example1(self):
        program = [1,0,0,0,99]
        self.assertEqual(
            day02.run_intcode_computer(program),
            [2,0,0,0,99]
        )

    def test_small_example2(self):
        program = [2,3,0,3,99]
        self.assertEqual(
            day02.run_intcode_computer(program),
            [2,3,0,6,99]
        )

    def test_small_example3(self):
        program = [2,4,4,5,99,0]
        self.assertEqual(
            day02.run_intcode_computer(program),
            [2,4,4,5,99,9801]
        )

    def test_small_example4(self):
        program = [1,1,1,4,99,5,6,0,99]
        self.assertEqual(
            day02.run_intcode_computer(program),
            [30,1,1,4,2,5,6,0,99]
        )
