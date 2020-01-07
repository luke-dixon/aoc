from collections import defaultdict

from .. import intcode, puzzle


class Day09(puzzle.Puzzle):
    year = '2019'
    day = '9'

    def get_data(self):
        data = defaultdict(lambda: 0)
        for i, x in enumerate([int(x) for x in self.input_data.split(',')]):
            data[i] = x
        return data

    def get_data2(self):
        data = [0] * 1100
        for i, x in enumerate([int(x) for x in self.input_data.split(',')]):
            data[i] = x
        return data

    def part1(self):
        input_ = [1]
        output = []
        intcode.run_intcode_computer(
            self.get_data2(),
            intcode.ListInputDevice(input_),
            intcode.ListOutputDevice(output),
            label='part1',
        )
        return output[0]

    def part2(self):
        input_ = [2]
        output = []
        intcode.run_intcode_computer(
            self.get_data2(),
            intcode.ListInputDevice(input_),
            intcode.ListOutputDevice(output),
            label='part2',
        )
        return output[0]

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
