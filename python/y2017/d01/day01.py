from lib import puzzle


def part1(data: str) -> int:
    numbers = []

    if data[-1] == data[0]:
        numbers.append(int(data[0]))

    for i in range(len(data) - 1):
        if data[i] == data[i + 1]:
            numbers.append(int(data[i]))

    return sum(numbers)


def part2(data: str) -> int:
    numbers = []

    for i in range(len(data)):
        if data[i] == data[((len(data) // 2) + i) % len(data)]:
            numbers.append(int(data[i]))
    return sum(numbers)


class Day01(puzzle.Puzzle):
    year = '2017'
    day = '1'

    def get_data(self) -> str:
        return self.input_data.strip()

    def run(self):
        print(f'Answer part 1: {part1(self.get_data())}')
        print(f'Answer part 2: {part2(self.get_data())}')
