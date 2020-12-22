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


class AsciiInputDevice(intcode.InputDevice):
    def __init__(self, program):
        self.orig_program = program
        self.program = [ord(x) for x in '\n'.join(self.orig_program)]

    def read(self) -> int:
        if self.program:
            value = self.program.pop(0)
            return value
        else:
            return ord('\n')


def grid_gen1(draw=True):
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
            try:
                s += chr(d)
            except ValueError:
                # must be the answer!
                pass
            l.append(d)
            if s.endswith('\n'):
                break

        if draw:
            print(s, end='')


class Day21(puzzle.Puzzle):
    year = '2019'
    day = '21'

    def add_additional_args(self, parser):
        parser.add_argument('-d', '--draw', action='store_true')

    def get_data(self):
        data = self.input_data
        return [int(x) for x in data.split(',')]

    def part1(self):
        grid = grid_gen1(draw=self.args.draw)

        data = defaultdict(int)
        for i, d in enumerate(self.get_data()):
            data[i] = d

        # yapf: disable

        # Jump if A is empty or D is safe, but C or B are empty
        # J = not tt[A] or (tt[D] and (not tt[C] or not tt[B]))
        program = [
            'OR C J',
            'AND B J',
            'NOT J J',

            'OR D T',
            'AND T J',

            'NOT A T',
            'OR T J',

            'WALK',
        ]

        # yapf: enable

        next_value = []
        grid.send(None)
        intcode.run_intcode_computer(
            data,
            AsciiInputDevice(program),
            GridOutputDevice(grid, next_value),
            label='part1',
        )

        return grid.send('get part 2 result')['answer']

    def part2(self):
        grid = grid_gen1(draw=self.args.draw)

        data = defaultdict(int)
        for i, d in enumerate(self.get_data()):
            data[i] = d

        # yapf: disable

        # Jump if:
        #   A is empty or
        #   D and H are safe, but C or B are empty
        # J = not tt[A] or ((tt[D] and tt[H]) and (not tt[C] or not tt[B]))
        program = [
            'OR C J',
            'AND B J',
            'NOT J J',

            'OR D T',
            'AND H T',
            'AND T J',

            'NOT A T',
            'OR T J',

            'RUN',
        ]

        # yapf: enable

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
