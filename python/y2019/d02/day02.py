import itertools
from typing import List

from .. import intcode, puzzle


def run_intcode_computer(data):
    intcode.run_intcode_computer(
        data,
        intcode.ListInputDevice([]),
        intcode.ListOutputDevice([]),
        label='part1',
    )
    return data


def part1(data: List[int], noun: int, verb: int) -> int:
    data[1] = noun
    data[2] = verb

    data = run_intcode_computer(data)
    return data[0]


def part2(data: List[int]) -> int:
    for noun, verb in itertools.product(range(0, 100), range(0, 100)):
        if part1(list(data), noun, verb) == 19690720:
            return 100 * noun + verb


class Day02(puzzle.Puzzle):
    year = '2019'
    day = '2'

    def get_data(self) -> List[int]:
        return [int(x) for x in self.input_data.strip().split(',')]

    def run(self):
        print(f'Answer part 1: {part1(self.get_data(), 12, 2)}')
        print(f'Answer part 2: {part2(self.get_data())}')
