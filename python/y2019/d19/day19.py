import itertools
import shelve
from collections import Mapping, defaultdict
from typing import Iterator

from .. import intcode, puzzle


class Beam(Mapping):
    def __init__(self, program):
        self.program = program
        self.io_cache = shelve.open('.cache-2019-19')

    def __getitem__(self, k):
        try:
            return self.io_cache[str(k)]
        except KeyError:
            next_input = [k[0], k[1]]
            output = []
            memory = defaultdict(int)
            for i, d in enumerate(self.program):
                memory[i] = d
            intcode.run_intcode_computer(
                memory,
                intcode.ListInputDevice(next_input),
                intcode.ListOutputDevice(output),
                label='part1',
            )
            self.io_cache[str(k)] = output[0]
            return output[0]

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[int]:
        raise NotImplementedError


def get_likely_square_size(beam, row_index, required_square_size=100):
    LOWER_BOUND = 0
    UPPER_BOUND = 1
    rows = {}

    for j in [0, required_square_size - 1]:
        # TODO: Binary search for the upper and lower bounds
        i = 0
        while beam[(i, row_index + j)] == 0:
            i += 1
        lower_bound = i
        i = 0
        while beam[(lower_bound + i, row_index + j)] == 1:
            i += 1
        rows[row_index + j] = (lower_bound, lower_bound + i)
    if (rows[row_index][UPPER_BOUND] <
            rows[row_index + required_square_size - 1][LOWER_BOUND]):
        return 0
    return (rows[row_index][UPPER_BOUND] -
            rows[row_index + required_square_size - 1][LOWER_BOUND] + 1)


def get_square_size(beam, row_index, required_square_size=100):
    LOWER_BOUND = 0
    UPPER_BOUND = 1
    rows = {}

    # Get maximum bounds of square
    for j in [0, required_square_size - 1]:
        i = 0
        while beam[(i, row_index + j)] == 0:
            i += 1
        lower_bound = i
        i = 0
        while beam[(lower_bound + i, row_index + j)] == 1:
            i += 1
        rows[row_index + j] = (lower_bound, lower_bound + i)

    square_left, square_top = rows[row_index + j][LOWER_BOUND], row_index
    square_right = rows[row_index][UPPER_BOUND]

    # Check all other lines of the beam
    for j in range(0, required_square_size):
        while beam[(square_left, row_index + j)] == 0:
            square_left += 1
        while beam[(square_right, row_index + j)] == 0:
            square_right -= 1

    return (square_left, square_top), square_right - square_left + 1


class Day19(puzzle.Puzzle):
    year = '2019'
    day = '19'

    def add_additional_args(self, parser):
        parser.add_argument('-d', '--draw', action='store_true')

    def get_data(self):
        data = self.input_data
        return [int(x) for x in data.split(',')]

    def part1(self):
        SIZE = 50

        input_ = []
        for y, x in itertools.product(range(SIZE), range(SIZE)):
            input_.append(x)
            input_.append(y)

        beam = Beam(self.get_data())
        output = []
        while input_:
            next_input = [input_.pop(0), input_.pop(0)]
            output.append(beam[(next_input[0], next_input[1])])

        d = {
            0: ' ',
            1: '#',
        }
        s = ''
        pattern = []
        for i in range(SIZE):
            s += ''.join(d[x] for x in output[i * SIZE:i * SIZE + SIZE])
            s += '\n'
            pattern.append(sum(output[i * SIZE:i * SIZE + SIZE]))

        if self.args.draw:
            print(s)
        return sum(output)

    def part2(self):
        beam = Beam(program=self.get_data())

        likely_square_sizes = {}

        required_square_size = 100
        upper = 2000
        lower = 50

        for row_index in [upper, lower]:
            likely_square_sizes[row_index] = get_likely_square_size(
                beam, row_index)

        current = None
        while likely_square_sizes[lower] < required_square_size:
            last_current = current
            current = lower + ((upper - lower) // 2)
            if last_current == current:
                break
            likely_square_sizes[current] = get_likely_square_size(
                beam, current)
            if likely_square_sizes[current] > required_square_size:
                upper = current
            elif likely_square_sizes[current] < required_square_size:
                lower = current

        for i in range(lower + 1, upper + 1):
            print(f'checking {i}')
            coords, size = get_square_size(beam, i)
            print(f'{i} size: {size}')
            if size == required_square_size:
                return 10000 * coords[0] + coords[1]

    def main(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
