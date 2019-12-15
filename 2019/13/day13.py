import math
import queue
import sys
from abc import ABC
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Union

from aocd.models import Puzzle


class Halt(Exception):
    pass


@dataclass
class Parameter:
    data: List[int]
    position: int
    mode: int
    relative_base: int

    def get(self):
        if self.mode == 1:
            return self.data[self.position]
        elif self.mode == 2:
            return self.data[self.data[self.position] + self.relative_base]
        else:
            return self.data[self.data[self.position]]

    def set(self, value: int):
        if self.mode == 1:
            self.data[self.position] = value
        elif self.mode == 2:
            self.data[self.data[self.position] + self.relative_base] = value
        else:
            self.data[self.data[self.position]] = value


@dataclass
class Instruction:
    data: List[int]
    position: int
    operation: Callable[['Instruction'], int]
    input: 'InputDevice'
    output: 'OutputDevice'
    parameter1: Parameter
    parameter2: Parameter
    parameter3: Parameter
    label: str
    relative_base: int

    def __call__(self):
        global I
        # print(f'{I}: operation: {self.operation.__name__}, pointer: {self.position}')
        return self.operation(self), self.relative_base


class InputDevice(ABC):
    def read(self) -> int:
        pass


class OutputDevice(ABC):
    def write(self, value: int) -> None:
        pass


@dataclass
class ListInputDevice(InputDevice):
    list: List[int]

    def read(self) -> int:
        return self.list.pop(0)


class ListOutputDevice(OutputDevice):
    def __init__(self, output_list: List[int]):
        self.list = output_list

    def write(self, value: int) -> None:
        self.list.append(value)


class QueueInputDevice(InputDevice):
    def __init__(self, input_queue: queue.Queue):
        self.queue = input_queue

    def read(self) -> int:
        return self.queue.get()


class QueueOutputDevice(OutputDevice):
    def __init__(self, output_queue: queue.Queue):
        self.queue = output_queue

    def write(self, value: int) -> None:
        self.queue.put(value)


def add(self: Instruction) -> int:
    self.parameter3.set(self.parameter1.get() + self.parameter2.get())
    return self.position + 4


def multiply(self: Instruction) -> int:
    self.parameter3.set(self.parameter1.get() * self.parameter2.get())
    return self.position + 4


def halt(self: Instruction) -> int:
    raise Halt


def store(self: Instruction) -> int:
    value = self.input.read()
    if isinstance(value, Exception):
        raise value
    self.parameter1.set(value)
    return self.position + 2


def retrieve(self: Instruction) -> int:
    value = self.parameter1.get()
    self.output.write(value)
    return self.position + 2


def jump_if_true(self: Instruction) -> int:
    if self.parameter1.get() != 0:
        return self.parameter2.get()
    else:
        return self.position + 3


def jump_if_false(self: Instruction) -> int:
    if self.parameter1.get() == 0:
        return self.parameter2.get()
    else:
        return self.position + 3


def less_than(self: Instruction) -> int:
    if self.parameter1.get() < self.parameter2.get():
        self.parameter3.set(1)
    else:
        self.parameter3.set(0)
    return self.position + 4


def equals(self: Instruction) -> int:
    if self.parameter1.get() == self.parameter2.get():
        self.parameter3.set(1)
    else:
        self.parameter3.set(0)
    return self.position + 4


def set_relative_base(self: Instruction) -> int:
    self.relative_base += self.parameter1.get()
    return self.position + 2


default_operations: Dict[int, Callable[[Instruction], int]] = {
    1: add,
    2: multiply,
    3: store,
    4: retrieve,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    9: set_relative_base,
    99: halt,
}


def instruction_factory(
    data: List[int],
    position: int,
    input_,
    output,
    relative_base,
    label: Optional[str] = None,
    operations: Optional[Dict[int, Callable[[Instruction], int]]] = None,
):
    if operations is None:
        operations = default_operations
    opcode = str(data[position]).rjust(5, '0')
    return Instruction(
        data,
        position,
        operations[int(opcode[3:])],
        input_,
        output,
        Parameter(data, position + 1, int(opcode[2]), relative_base),
        Parameter(data, position + 2, int(opcode[1]), relative_base),
        Parameter(data, position + 3, int(opcode[0]), relative_base),
        label,
        relative_base,
    )


def run_intcode_computer(
    program: Union[List[int], Dict[int, int]], input_, output, label: str
):
    position = 0
    relative_base = 0

    while True:
        instruction = instruction_factory(
            program, position, input_, output, relative_base, label
        )
        try:
            position, relative_base = instruction()
        except Halt:
            break
    return output


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


class AIJoystickInputDevice(InputDevice):
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


class UserJoystickInputDevice(InputDevice):
    def __init__(self, output):
        self.output = output

    def read(self):
        controls = {
            'a': -1,
            's': 0,
            'd': 1,
        }

        return controls.get(input('Enter a direction: '), 0)


class Day13(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=13)

    def get_data(self):
        orig_data = self.input_data
        data = defaultdict(lambda: 0)
        for i, x in enumerate([int(x) for x in orig_data.split(',')]):
            data[i] = x
        return data

    def part1(self):
        input_ = []
        output = []
        run_intcode_computer(
            self.get_data(),
            ListInputDevice(input_),
            ListOutputDevice(output),
            label='part2',
        )

        grid = draw_output(output)
        c = Counter(grid)

        return c['#']

    def part2(self):

        output = []
        data = self.get_data()
        data[0] = 2

        if '-u' in sys.argv:
            input_device = UserJoystickInputDevice(output)
        else:
            input_device = AIJoystickInputDevice(output)
            if '-d' in sys.argv:
                input_device.draw = True

        run_intcode_computer(
            data, input_device, ListOutputDevice(output), label='part2'
        )

        return '\n' + draw_output(output)


def main():
    puzzle = Day13()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')
