from collections import defaultdict, deque

from lib import puzzle


class Day15(puzzle.Puzzle):
    year = '2020'
    day = '15'

    def get_data(self):
        return [int(x) for x in self.input_data.splitlines()[0].split(',')]
        return [0, 3, 6]

    def part1(self):
        data = self.get_data()

        print(data)

        d = defaultdict(list)

        for i, n in enumerate(data):
            d[n].append(i)

        numbers = data
        while i <= 2020:
            i += 1
            last_spoken = numbers[-1]
            first_time = len(d[last_spoken]) <= 1
            if first_time:
                numbers.append(0)
                d[0].append(i)
            else:
                number = d[last_spoken][-1] - d[last_spoken][-2]
                numbers.append(number)
                if len(d[number]) > 1:
                    d[number] = [d[number][-1], i]
                else:
                    d[number].append(i)

        return numbers[2020 - 1]

    def part2(self):
        data = self.get_data()

        print(data)

        d = defaultdict(deque)
        last_occurence = {}
        prev_occurence = {}

        for i, n in enumerate(data):
            last_occurence[n] = i

        prev_number = None
        last_number = data[-1]
        while i < 30000000 - 1:
            i += 1
            last_spoken = last_number
            first_time = last_spoken not in last_occurence
            if first_time:
                last_number = 0
                last_occurence[0] = i
            else:
                prev_number = last_number
                last_number = last_occurence[last_spoken] - prev_occurence.get(last_spoken, 0)
                prev_occurence[last_number] = last_occurence.get(last_number, 0)
                last_occurence[last_number] = i

        print(len(d))
        #pprint(numbers)
        print(prev_number, last_number)

        return last_number

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')


# [14, 3, 1, 0, 9, 5]
# [x, x, x, x, x, x, x, x, x, x, x, x, z, x, x, 9, x, x, x, v, x, x, x, w, 0, x, z, 14, v, 9, 14, 3, 1, 0, 9, 5
# 1 seems invalid