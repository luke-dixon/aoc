from typing import List


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


def main():
    with open('input1.txt') as f:
        data = [int(x) for x in f.read().splitlines()]

    print(f'Answer part 1: {part1(data)}')
    print(f'Answer part 2: {part2(data)}')


if __name__ == "__main__":
    main()
