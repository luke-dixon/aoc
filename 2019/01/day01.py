from typing import List

from aocd.models import Puzzle


def calc_fuel(x: int, recursive: bool = False):
    fuel_required = x // 3
    fuel_required -= 2

    if recursive and fuel_required > 0:
        more_fuel = calc_fuel(fuel_required, recursive=recursive)
        if more_fuel > 0:
            fuel_required += more_fuel

    return fuel_required


class Day01(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=1)

    def get_data(self) -> List[int]:
        return [int(x) for x in self.input_data.splitlines()]

    def part1(self) -> int:
        return sum(calc_fuel(x) for x in self.get_data())

    def part2(self) -> int:
        return sum(calc_fuel(x, recursive=True) for x in self.get_data())


def main():
    puzzle = Day01()

    print(f'Answer part 1: {puzzle.part1()}')
    print(f'Answer part 2: {puzzle.part2()}')
