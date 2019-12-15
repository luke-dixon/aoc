import itertools
import queue
import threading
from abc import ABC
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from .. import puzzle


class Halt(Exception):
    pass


@dataclass
class Parameter:
    data: List[int]
    position: int
    mode: int

    def get(self):
        if self.mode:
            return self.data[self.position]
        else:
            return self.data[self.data[self.position]]

    def set(self, value: int):
        if self.mode:
            self.data[self.position] = value
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

    def __call__(self):
        return self.operation(self)


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
    self.output.write(self.parameter1.get())
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


default_operations: Dict[int, Callable[[Instruction], int]] = {
    1: add,
    2: multiply,
    3: store,
    4: retrieve,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    99: halt,
}


def instruction_factory(
    data: List[int],
    position: int,
    input_,
    output,
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
        Parameter(data, position + 1, int(opcode[2])),
        Parameter(data, position + 2, int(opcode[1])),
        Parameter(data, position + 3, int(opcode[0])),
        label,
    )


def run_intcode_computer(program: List[int], input_):
    output = []
    position = 0
    program = list(program)
    while True:
        instruction = instruction_factory(
            program, position, input_, ListOutputDevice(output)
        )
        try:
            position = instruction()
        except Halt:
            break
    return output


def run_intcode_computer2(program: List[int], input_, output, label: str):
    position = 0
    program = list(program)

    while True:
        instruction = instruction_factory(program, position, input_, output, label,)
        try:
            position = instruction()
        except Halt:
            break
    return output


class Day07(puzzle.Puzzle):
    year = '2019'
    day = '7'

    def get_data(self):
        return [int(x) for x in self.input_data.splitlines()[0].split(',')]

    def part1(self):
        data = self.get_data()

        thruster_inputs = []

        for i in itertools.permutations(range(5)):
            input_ = [0, 0]
            for phase in i:
                input_[0] = phase
                output = run_intcode_computer(data, ListInputDevice(input_))
                input_ = [None, output.pop()]
            thruster_inputs.append(input_[1])

        return max(thruster_inputs)

    def part2(self):
        data = self.get_data()
        thruster_inputs = []
        amplifier_indexes = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

        for i in itertools.permutations(range(5, 10)):
            threads = []
            channels = []
            for _ in range(5):
                channels.append(queue.Queue())
            for channel_index, phase in enumerate(i):
                channels[channel_index].put(phase)
                t = threading.Thread(
                    target=run_intcode_computer2,
                    args=(
                        data,
                        QueueInputDevice(channels[channel_index]),
                        QueueOutputDevice(
                            channels[(channel_index + 1) % len(channels)]
                        ),
                        amplifier_indexes[channel_index],
                    ),
                )
                threads.append(t)
                t.start()
            try:
                channels[0].put(0)
                amp_e = threads.pop()
                amp_e.join()
            finally:
                for channel in channels:
                    channel.put(Halt())
                for thread in threads:
                    thread.join()
            amp_e_output_channel = channels.pop(0)  # Or amplifier a input channel
            thruster_input = amp_e_output_channel.get()
            thruster_inputs.append(thruster_input)

        return max(thruster_inputs)

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
