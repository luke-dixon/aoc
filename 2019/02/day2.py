import itertools
from typing import List, Dict, Callable


def print_data(data: List[int]) -> None:
    for i in range(0, (len(data) // 4 + 1)):
        print(data[i*4:i*4 + 4])


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


def part1(data: List[int], noun: int, verb: int) -> int:
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


def part2(data: List[int]) -> int:
    for noun, verb in itertools.product(range(0, 100), range(0, 100)):
        if part1(list(data), noun, verb) == 19690720:
            return 100 * noun + verb


def main():
    with open('input2.txt') as f:
        data = [int(x) for x in f.read().strip().split(',')]

    print(f'Answer part 1: {part1(list(data), 12, 2)}')
    print(f'Answer part 2: {part2(data)}')


if __name__ == "__main__":
    main()
