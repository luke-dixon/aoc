from typing import List

from lib import puzzle


def part1_update_strategy(instruction_value):
    return instruction_value + 1


def part2_update_strategy(instruction_value):
    return instruction_value - 1 if instruction_value >= 3 else instruction_value + 1


def run(data, update_strategy):
    next_instruction, steps = 0, 0
    try:
        while True:
            instruction_value = data[next_instruction]
            data[next_instruction] = update_strategy(instruction_value)
            next_instruction, steps = next_instruction + instruction_value, steps + 1
    except IndexError:
        return steps


class Day05(puzzle.Puzzle):
    year = '2017'
    day = '5'

    def get_data(self) -> List[int]:
        return [int(n) for n in self.input_data.splitlines()]

    def run(self):
        print(f'Part 1 Answer: {run(self.get_data(), part1_update_strategy)}')
        print(f'Part 2 Answer: {run(self.get_data(), part2_update_strategy)}')
