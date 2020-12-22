from collections import defaultdict

from .. import intcode
from lib import puzzle


class GridInputDevice(intcode.InputDevice):
    def __init__(self, grid, next_value):
        self.grid = grid
        self.next_value = next_value

    def read(self):
        if not self.next_value:
            value = next(self.grid)
        else:
            value = self.next_value.pop(0)
        return value


class GridOutputDevice(intcode.OutputDevice):
    def __init__(self, grid, next_value):
        self.grid = grid
        self.value = []
        self.next_value = next_value

    def write(self, value: int) -> None:
        self.value.append(self.grid.send(value))


class FullyExplored(Exception):
    def __init__(self, payload):
        self.payload = payload
        super().__init__()


def grid_gen1():
    yield 'started'
    while True:
        s = '.'

        while True:
            d = yield
            if d == 'get part 1 result':
                yield {
                    'grid': s,
                }
                return
            s += chr(d)


class AsciiInputDevice(intcode.InputDevice):
    def __init__(self, program):
        self.orig_program = program
        self.program = [ord(x) for x in '\n'.join(self.orig_program)]

    def read(self) -> int:
        if self.program:
            value = self.program.pop(0)
            return value
        else:
            self.program = [ord(x) for x in '\n'.join(self.orig_program)]
            return '\n'


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


class Day17(puzzle.Puzzle):
    year = '2019'
    day = '17'

    def add_additional_args(self, parser):
        parser.add_argument('-d', '--draw', action='store_true')

    def get_data(self):
        data = self.input_data
        return [int(x) for x in data.split(',')]

    def part1(self):
        grid = grid_gen1()

        data = defaultdict(int)
        for i, d in enumerate(self.get_data()):
            data[i] = d

        next_value = []
        grid.send(None)
        intcode.run_intcode_computer(
            data,
            GridInputDevice(grid, next_value),
            GridOutputDevice(grid, next_value),
            label='part1',
        )

        data = grid.send('get part 1 result')

        intersections = []

        rows = data['grid'].splitlines()
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == '#':
                    try:
                        if all([
                            rows[y + 1][x] == '#',
                            rows[y - 1][x] == '#',
                            rows[y][x + 1] == '#',
                            rows[y][x - 1] == '#',
                        ]):
                            intersections.append((y, x))
                    except IndexError:
                        pass

        total = 0
        for y, x in intersections:
            total += y * x

        return total


    def part2(self):
        grid = grid_gen2(draw=self.args.draw)

        data = defaultdict(int)
        for i, d in enumerate(self.get_data()):
            data[i] = d

        data[0] = 2

        program = [
            'A,B,A,B,C,B,A,C,B,C',
            'L,12,L,8,R,10,R,10',
            'L,6,L,4,L,12',
            'R,10,L,8,L,4,R,10',
            'y' if self.args.draw else 'n',
        ]

        next_value = []
        grid.send(None)
        intcode.run_intcode_computer(
            data,
            AsciiInputDevice(program),
            GridOutputDevice(grid, next_value),
            label='part1',
        )

        return grid.send('get part 2 result')['answer']

    def main(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
