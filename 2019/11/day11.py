import queue
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Union

from aocd.models import Puzzle

from .. import intcode


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
        intcode.run_intcode_computer(
            self.get_data(),
            GridInputDevice(grid, next_value),
            GridOutputDevice(grid, next_value),
            label='part1',
        )

        return len(grid.send('get result'))

    def part2(self):
        grid_data = {}
        grid = grid_gen(grid_data, initial_colour=1)

        next_value = []
        grid.send(None)
        intcode.run_intcode_computer(
            self.get_data(),
            GridInputDevice(grid, next_value),
            GridOutputDevice(grid, next_value),
            label='part1',
        )

        return '\n' + paint_grid(grid_data, range(-2, 50), range(-10, 3))


def main():
    puzzle = Day11()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')
