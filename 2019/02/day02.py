import itertools
from typing import List

from .. import intcode, puzzle


class Day02(puzzle.Puzzle):
    year = '2019'
    day = '2'

    def get_data(self) -> List[int]:
        return [int(x) for x in self.input_data.strip().split(',')]

    def part1(self, noun: int, verb: int) -> int:
        data = self.get_data()
        data[1] = noun
        data[2] = verb

        intcode.run_intcode_computer(
            data,
            intcode.ListInputDevice([]),
            intcode.ListOutputDevice([]),
            label='part1',
        )
        return data[0]

    def part2(self) -> int:
        for noun, verb in itertools.product(range(0, 100), range(0, 100)):
            if self.part1(noun, verb) == 19690720:
                return 100 * noun + verb

    def run(self):
        print(f'Answer part 1: {self.part1(12, 2)}')
        print(f'Answer part 2: {self.part2()}')
