import queue
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Callable, List, Optional, Union

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


def run_intcode_computer(program: Union[List[int], Dict[int, int]], input_, output, label: str):
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


class GridInputDevice(InputDevice):
    def __init__(self, grid, next_value):
        self.grid = grid
        self.next_value = next_value

    def read(self):
        if not self.next_value:
            value = next(self.grid)
        else:
            value = self.next_value.pop(0)
        return value


class GridOutputDevice(OutputDevice):
    def __init__(self, grid, next_value):
        self.grid = grid
        self.value = []
        self.next_value = next_value

    def write(self, value: int) -> None:
        if len(self.value) == 1:
            self.value.append(value)
            self.next_value.append(self.grid.send(self.value))
            self.value = []
        else:
            self.value.append(value)


def grid_gen(data, initial_colour):
    x, y = 0, 0
    o_x, o_y = 0, 1

    painted_set = set()

    data[(0, 0)] = initial_colour

    yield 'started'
    while True:
        if (x, y) not in data:
            data[(x, y)] = 0

        value = yield data[(x, y)]

        if value == 'get result':
            value = yield painted_set


        colour, direction = value
        if direction == 0:
            if o_x == 0 and o_y == 1:
                o_x, o_y = -1, 0
            elif o_x == -1 and o_y == 0:
                o_x, o_y = 0, -1
            elif o_x == 0 and o_y == -1:
                o_x, o_y = 1, 0
            elif o_x == 1 and o_y == 0:
                o_x, o_y = 0, 1
        elif direction == 1:
            if o_x == 0 and o_y == 1:
                o_x, o_y = 1, 0
            elif o_x == -1 and o_y == 0:
                o_x, o_y = 0, 1
            elif o_x == 0 and o_y == -1:
                o_x, o_y = -1, 0
            elif o_x == 1 and o_y == 0:
                o_x, o_y = 0, -1

        data[(x, y)] = colour
        x, y = x + o_x, y + o_y
        painted_set.add((x, y))


def paint_grid(grid_data, x_range, y_range):
    output = ''
    for y in reversed(y_range):  # Ahh, it's reflected upside down
        for x in x_range:
            if (x, y) in grid_data:
                if grid_data[(x, y)]:
                    output += '#'
                else:
                    output += ' '
            else:
                output += '.'
        output += '\n'
    return output


class Day11(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=11)

    def get_data(self):
        orig_data = self.input_data
        data = defaultdict(lambda: 0)
        for i, x in enumerate([int(x) for x in orig_data.split(',')]):
            data[i] = x
        return data

    def part1(self):
        grid_data = {}
        grid = grid_gen(grid_data, initial_colour=0)

        next_value = []
        grid.send(None)
        run_intcode_computer(self.get_data(), GridInputDevice(grid, next_value), GridOutputDevice(grid, next_value), label='part1')

        return len(grid.send('get result'))

    def part2(self):
        grid_data = {}
        grid = grid_gen(grid_data, initial_colour=1)

        next_value = []
        grid.send(None)
        run_intcode_computer(self.get_data(), GridInputDevice(grid, next_value), GridOutputDevice(grid, next_value), label='part1')

        return '\n' + paint_grid(grid_data, range(-50, 50), range(-50, 50))


def main():
    puzzle = Day11()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')


if __name__ == '__main__':
    main()
