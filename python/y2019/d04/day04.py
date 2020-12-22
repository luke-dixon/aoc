from lib import puzzle


def part1(data: str):
    lower = int(data.split('-')[0])
    upper = int(data.split('-')[1])

    results = []

    for i in range(lower, upper + 1):
        if i == int(''.join(sorted(str(i)))):
            prev = str(i)[0]
            valid = False
            for j in str(i)[1:]:
                if j == prev:
                    valid = True
                prev = j
            if valid:
                results.append(i)

    return len(results)


def part2(data: str):
    lower = int(data.split('-')[0])
    upper = int(data.split('-')[1])

    results = []

    for i in range(lower, upper + 1):
        if i == int(''.join(sorted(str(i)))):
            prev = str(i)[0]
            prev2 = str(i)[1]
            prev3 = str(i)[2]
            if prev == prev2 and prev2 != prev3:
                valid = True
            else:
                valid = False
            prev4 = str(i)[3]
            if prev2 == prev3 and prev != prev2 and prev3 != prev4:
                valid = True
            prev5 = str(i)[4]
            if prev3 == prev4 and prev2 != prev3 and prev4 != prev5:
                valid = True
            prev6 = str(i)[5]
            if prev4 == prev5 and prev3 != prev4 and prev5 != prev6:
                valid = True
            if prev5 == prev6 and prev5 != prev4:
                valid = True
            if valid:
                results.append(i)

    return len(results)


class Day04(puzzle.Puzzle):
    year = '2019'
    day = '4'

    def get_data(self) -> str:
        return self.input_data

    def run(self):
        print(f'Answer part 1: {part1(self.get_data())}')
        print(f'Answer part 2: {part2(self.get_data())}')
