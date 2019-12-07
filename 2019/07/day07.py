import itertools
import queue
import threading
from collections import defaultdict
from typing import List, Callable, Dict
from ctypes import c_long as c_int

from aocd.models import Puzzle


class Halt(Exception):
    pass


class Poison:
    pass


class Parameter:
    def __init__(self, data, position, mode):
        self.data = data
        self.position = position
        self.mode = mode

    def get(self):
        if self.mode:
            return self.data[self.position]
        else:
            return self.data[self.data[self.position]]

    def set(self, value):
        if self.mode:
            self.data[self.position] = value
        else:
            self.data[self.data[self.position]] = value


class Instruction:
    def __init__(self, data, position, operation, input_, output, parameter1, parameter2, parameter3, idx):
        self.idx = idx
        self.data = data
        self.position = position
        self.operation = operation
        self.input = input_
        self.output = output
        self.parameter1 = parameter1
        self.parameter2 = parameter2
        self.parameter3 = parameter3

    def __call__(self):
        return self.operation(self)


def add(self: Instruction) -> int:
    value = c_int(self.parameter1.get() + self.parameter2.get()).value
    self.parameter3.set(value)
    return self.position + 4


def multiply(self: Instruction) -> int:
    value = c_int(self.parameter1.get() * self.parameter2.get()).value
    self.parameter3.set(self.parameter1.get() * self.parameter2.get())
    return self.position + 4


def halt(self: Instruction) -> int:
    raise Halt


def store(self: Instruction) -> int:
    #print(f'store: {self.input}, {self.output}')
    value = self.input.pop(0)
    self.parameter1.set(value)
    return self.position + 2


def store_q(self: Instruction) -> int:
    #print(f'{self.idx} receiving')
    value = self.input.get(timeout=5)
    #print(f'{self.idx} received {value}')
    if type(value) == Poison:
        raise Halt
    self.parameter1.set(value)
    return self.position + 2


def retrieve(self: Instruction) -> int:
    #print(f'retrieve: {self.input}, {self.output}')
    #print(self.parameter1.get())
    self.output.append(self.parameter1.get())
    #print(self.parameter1.get())
    #print(f'retrieve end: {self.input}, {self.output}')
    return self.position + 2


def retrieve_q(self: Instruction) -> int:
    self.output.put(self.parameter1.get(), timeout=5)
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


operations: Dict[int, Callable[[Instruction], int]] = {
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

operations_q: Dict[int, Callable[[Instruction], int]] = {
    1: add,
    2: multiply,
    3: store_q,
    4: retrieve_q,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    99: halt,
}


def instruction_factory(data, position, input_, output, idx=None, operations=operations):
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
        idx,
    )


def run_intcode_computer(program, input_):
    output = []
    position = 0
    while True:
        instruction = instruction_factory(program, position, input_, output)
        try:
            position = instruction()
        except Halt:
            break
    return output


def run_intcode_computer2(program, input_, output, idx):
    position = 0
    while True:
        instruction = instruction_factory(program, position, input_, output, idx, operations=operations_q)
        try:
            position = instruction()
        except Halt:
            #print(f'amplifier {idx} halted')
            break
    return output


class Day7(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=7)
        self.data = [int(x) for x in self.input_data.splitlines()[0].split(',')]

    def part1(self):
        data = self.data
        #data = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
        #print(data)

        thruster_inputs = []

        l = [0, 0]
        for i in itertools.permutations(range(5)):
            l = [0, 0]
            #print(f'permutation: {i}')
            for phase in i:
                l[0] = phase
                #print(f'input: {l}')
                output = run_intcode_computer(data, l)
                #print(f'output {output}')
                l = [None, output.pop()]
            #print(f'thruster input: {l}')
            thruster_inputs.append(l[1])

        return max(thruster_inputs)

    def part2(self):
        data = self.data
        #data = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
        #data = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
        #print(data)

        thruster_inputs = []

        amplifier_indexes = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

        for i in itertools.permutations(range(5, 10)):
            #print(f'permutation: {i}')
            threads = []
            channels = []
            for _ in range(5):
                channels.append(queue.Queue())
            for channel_idx, phase in enumerate(i):
                channels[channel_idx].put(phase)
                #print(f'{amplifier_indexes.get(channel_idx)} -> {amplifier_indexes.get((channel_idx + 1) % len(channels))}')
                t = threading.Thread(target=run_intcode_computer2, args=(data, channels[channel_idx], channels[(channel_idx + 1) % len(channels)], amplifier_indexes[channel_idx]))
                threads.append(t)
                t.start()
            try:
                channels[0].put(0)
                amp_e = threads.pop()
                amp_e.join()
                amp_e_channel = channels.pop(0)
                #print([q.empty() for q in channels])
                thruster_input = amp_e_channel.get(timeout=1)
                #print(f'thruster input: {thruster_input}')
                thruster_inputs.append(thruster_input)
                for channel in channels:
                    channel.put(Poison())
            except KeyboardInterrupt:
                for channel in channels:
                    channel.put(Poison())
                for thread in threads:
                    thread.join()

        return max(thruster_inputs)


def main():
    puzzle = Day7()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')


if __name__ == '__main__':
    main()
