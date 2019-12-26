from typing import List

from .. import puzzle


def calc_fuel(x: int, recursive: bool = False):
    fuel_required = x // 3
    fuel_required -= 2

    if recursive and fuel_required > 0:
        more_fuel = calc_fuel(fuel_required, recursive=recursive)
        if more_fuel > 0:
            fuel_required += more_fuel

    return fuel_required


def part1(data: List[int]) -> int:
    return sum(calc_fuel(x) for x in data)


def part2(data: List[int]) -> int:
    return sum(calc_fuel(x, recursive=True) for x in data)


class Day01(puzzle.Puzzle):
    year = '2019'
    day = '1'

    def get_data(self) -> List[int]:
        return [int(x) for x in self.input_data.splitlines()]

    def run(self):
        print(f'Answer part 1: {part1(self.get_data())}')
        print(f'Answer part 2: {part2(self.get_data())}')
