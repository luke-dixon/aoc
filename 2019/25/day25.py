import itertools
import queue
import threading
from collections import defaultdict

from .. import intcode, puzzle


class GridOutputDevice(intcode.OutputDevice):
    def __init__(self, grid, next_value):
        self.grid = grid
        self.value = []
        self.next_value = next_value

    def write(self, value: int) -> None:
        self.value.append(self.grid.send(value))


class AsciiInputDevice(intcode.InputDevice):
    def __init__(self, program):
        self.orig_program = program
        self.program = [ord(x) for x in '\n'.join(self.orig_program)]

    def read(self) -> int:
        if self.program:
            value = ord(self.program[0])
            self.program = self.program[1:]
            return value
        else:
            self.program = input('What to do: ')
            self.program += '\n'
            if self.program.startswith('try '):
                n = int(self.program[len('try ')])
                _, n, direction, *items = self.program.strip().split(' ')
                n = int(n)
                items = ' '.join(items).split(',')
                self.program = ''
                for item in items:
                    self.program += f'drop {item}\n'
                last = []
                for combination in itertools.combinations(items, n):
                    if len(last):
                        for item in last:
                            self.program += f'drop {item}\n'
                    last = []
                    for item in combination:
                        self.program += f'take {item}\n'
                        last.append(item)
                    self.program += f'{direction}\n'

            value = ord(self.program[0])
            self.program = self.program[1:]
            return value


def grid_gen2(draw=False):
    answer = None

    yield 'started'
    while True:
        s = ''
        l = []

        while True:
            d = yield
            if d is None:
                break
            if isinstance(d, int) and d > 127:
                answer = d
            if d == 'get part 2 result':
                yield {
                    'grid': s,
                    'answer': answer,
                }
                return
            s += chr(d)
            l.append(d)
            if s.endswith('\n\n'):
                break

        if draw:
            print(s, end='')


class Day25(puzzle.Puzzle):
    year = '2019'
    day = '25'

    def get_data(self):
        return [int(x) for x in self.input_data.splitlines()[0].split(',')]

    def part1(self):
        grid = grid_gen2(draw=True)

        data = defaultdict(int)
        for i, d in enumerate(self.get_data()):
            data[i] = d

        next_value = []
        grid.send(None)

        while True:
            intcode.run_intcode_computer(
                data,
                AsciiInputDevice([]),
                GridOutputDevice(grid, next_value),
                label='part1',
            )

    def part2(self):
        pass

    def main(self):
        print(f'Part 1 Answer: {self.part1()}')
