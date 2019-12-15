from aocd.models import Puzzle

from .. import intcode


class Day5(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=5)

    def get_data(self):
        return tuple([int(x) for x in self.input_data.split(',')])

    def part1(self):
        output = []
        intcode.run_intcode_computer(
            list(self.get_data()),
            intcode.ListInputDevice([1]),
            intcode.ListOutputDevice(output),
            'part 1',
        )
        return output[-1]

    def part2(self):
        output = []
        intcode.run_intcode_computer(
            list(self.get_data()),
            intcode.ListInputDevice([5]),
            intcode.ListOutputDevice(output),
            'part 2',
        )
        return output[-1]


def main():
    puzzle = Day5()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')
