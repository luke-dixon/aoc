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


class Day9(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=9)

    def get_data(self):
        orig_data = self.input_data
        #orig_data = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
        #orig_data = '1102,34915192,34915192,7,4,7,99,0'
        #orig_data = '104,1125899906842624,99'
        data = defaultdict(lambda: 0)
        for i, x in enumerate([int(x) for x in orig_data.split(',')]):
            data[i] = x
        return data

    def part1(self):
        input_ = [1]
        output = []
        run_intcode_computer(self.get_data(), ListInputDevice(input_), ListOutputDevice(output), label='part1')
        return output[0]

    def part2(self):
        input_ = [2]
        output = []
        run_intcode_computer(self.get_data(), ListInputDevice(input_), ListOutputDevice(output),label='part2')
        return output[0]


def main():
    puzzle = Day9()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')


if __name__ == '__main__':
    main()
