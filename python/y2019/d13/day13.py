import math
from collections import Counter, defaultdict

from .. import intcode
from lib import puzzle

flipper_location = (0, 0)
ball_location = (0, 0)


def draw_output(output, draw=True):
    global flipper_location
    global ball_location
    s = ''
    tiles = {
        0: ' ',
        1: '|',
        2: '#',
        3: '-',
        4: '*',
    }

    coords = {}

    max_x = 0
    min_x = math.inf
    max_y = 0
    min_y = math.inf

    score = 0

    for i in range(len(output) // 3):
        x, y, tile = output[i * 3], output[i * 3 + 1], output[i * 3 + 2]

        if x == -1:
            score = tile
            continue

        if tile == 3:
            flipper_location = (x, y)
        if tile == 4:
            ball_location = (x, y)

        max_x = max(max_x, x)
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        coords[(x, y)] = tile

    if draw:
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) in coords:
                    s += tiles.get(coords[(x, y)], 'e')
                else:
                    s += '.'
            s += '\n'

    s += f'score: {score}'

    return s


class AIJoystickInputDevice(intcode.InputDevice):
    def __init__(self, output, draw=False):
        self.output = output
        self.draw = draw

    def read(self):
        if self.draw:
            print(draw_output(self.output, draw=True))
        else:
            draw_output(self.output, draw=True)
        ai_controls = 0
        if ball_location[0] > flipper_location[0]:
            ai_controls = 1
        elif ball_location[0] < flipper_location[0]:
            ai_controls = -1
        return ai_controls


class UserJoystickInputDevice(intcode.InputDevice):
    def __init__(self, output):
        self.output = output

    def read(self):
        controls = {
            'a': -1,
            's': 0,
            'd': 1,
        }

        print(draw_output(self.output, draw=True))
        return controls.get(input('Enter a direction (a: left, d: right): '), 0)


class Day13(puzzle.Puzzle):
    year = '2019'
    day = '13'

    def add_additional_args(self, parser):
        parser.add_argument('-u', '--user', action='store_true')
        parser.add_argument('-d', '--draw', action='store_true')

    def get_data(self):
        orig_data = self.input_data
        data = defaultdict(lambda: 0)
        for i, x in enumerate([int(x) for x in orig_data.split(',')]):
            data[i] = x
        return data

    def part1(self):
        input_ = []
        output = []
        intcode.run_intcode_computer(
            self.get_data(),
            intcode.ListInputDevice(input_),
            intcode.ListOutputDevice(output),
            label='part2',
        )

        grid = draw_output(output)
        c = Counter(grid)

        return c['#']

    def part2(self):

        output = []
        data = self.get_data()
        data[0] = 2

        if self.args.user:
            input_device = UserJoystickInputDevice(output)
        else:
            input_device = AIJoystickInputDevice(output)
            if self.args.draw:
                input_device.draw = True

        intcode.run_intcode_computer(
            data, input_device, intcode.ListOutputDevice(output), label='part2'
        )

        return '\n' + draw_output(output)

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
