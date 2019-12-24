import itertools
import math
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
        data = self.get_data()

        #SIZE = 1724 - 110
        SIZE = 1714 - 100
        SKIP_SIZE = 1
        hundreds_count = 0

        min_x = math.inf
        max_x = 0

        rows = {}

        beam = Beam(program=self.get_data())

        while True:
            SIZE += SKIP_SIZE
            input_ = []
            for x in range(SIZE):
                input_.append(x)
                input_.append(SIZE)
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
            min_x = min(s.find('#'), min_x)
            print(s[min_x:].rstrip(), end='')
            print((s.find('#'), SIZE), end='')
            if sum(output) >= 100:
                hundreds_count += 1
                start = (s.find('#'), SIZE)
                end = (s.rfind('#'), SIZE)
                #print(start, end, f'width: {sum(output)}', hundreds_count)
                rows[SIZE] = ((s.find('#'), SIZE), (s.rfind('#'), SIZE))
                i = SIZE
                while True:
                    i -= SKIP_SIZE
                    if i not in rows:
                        break
                    if rows[i][1][0] < start[0] + 100:
                        break
                print(SIZE - i)
                if SIZE - i > 100:
                    return
            else:
                hundreds_count == 0
                rows = {}
        return sum(output)

    def main(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
