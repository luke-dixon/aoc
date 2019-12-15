import itertools
from typing import Callable, Dict, List

from aocd.models import Puzzle


def print_data(data: List[int]) -> None:
    for i in range(0, (len(data) // 4 + 1)):
        print(data[i * 4 : i * 4 + 4])


def add(position: int, data: List[int]) -> None:
    data[data[position + 3]] = data[data[position + 1]] + data[data[position + 2]]


def multiply(position: int, data: List[int]) -> None:
    data[data[position + 3]] = data[data[position + 1]] * data[data[position + 2]]


class Halt(Exception):
    pass


def halt(_position: int, _data: List[int]) -> None:
    raise Halt()


operations: Dict[int, Callable[[int, List[int]], None]] = {
    1: add,
    2: multiply,
    99: halt,
}


class Day2(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=2)

    def get_data(self) -> List[int]:
        return [int(x) for x in self.input_data.strip().split(',')]

    def part1(self, noun: int, verb: int) -> int:
        data = self.get_data()
        data[1] = noun
        data[2] = verb

        position = 0
        while True:
            opcode = data[position]
            try:
                operations[opcode](position, data)
            except Halt:
                return data[0]
            position += 4

    def part2(self) -> int:
        for noun, verb in itertools.product(range(0, 100), range(0, 100)):
            if self.part1(noun, verb) == 19690720:
                return 100 * noun + verb


def main():
    puzzle = Day2()

    print(f'Answer part 1: {puzzle.part1(12, 2)}')
    print(f'Answer part 2: {puzzle.part2()}')
