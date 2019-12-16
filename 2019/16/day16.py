from .. import puzzle


def get_mult_pattern(j):
    base_mult_pattern = [1, 0, -1, 0]

    if j > 1:
        for _ in range(j - 1):
            yield 0

    i = 0
    while True:
        for _ in range(j):
            yield base_mult_pattern[i % len(base_mult_pattern)]
        i += 1


class Day16(puzzle.Puzzle):
    year = '2019'
    day = '16'

    def get_data(self):
        return [int(x) for x in self.input_data]

    def part1(self):
        data = self.get_data()

        totals = list(data)

        for _ in range(100):
            signal = totals
            totals = []
            for i in range(1, len(signal) + 1):
                mult_pattern = get_mult_pattern(i)

                new_signal = []
                for x, y in zip(signal, mult_pattern):
                    if y == 0 or x == 0:
                        new_signal.append(0)
                    else:
                        new_signal.append(x * y)

                totals.append(abs(sum(new_signal)) % 10)
        return ''.join([str(x) for x in totals[:8]])

    def part2(self):
        '''
        What we do with the value at each position looks a bit like:
        1 3 5 7 9 1 3 5 7 9 1 3 5 7 9
         23  67  01  45  89  23  67
          345   901   567   123   789
           4567   1234    9012    7890
            56789     56789     56789
             678901      890123      0
              7890123       1234567
               89012345        4567890
                positive        negative

        The value we have for the offset is so large that we will only
        be adding all the values to the end of the list. We can work
        backwards to save calculating the same sums over and over.
        '''
        data = self.get_data()

        totals = list(data) * 10000
        offset = int(''.join(str(x) for x in totals[:7]))

        for _ in range(100):
            signal = totals
            totals = [0] * len(data) * 10000
            total = 0
            for i in reversed(range(offset, len(data) * 10000)):
                total += signal[i]
                totals[i] = abs(total) % 10

        return ''.join(str(x) for x in totals[offset : offset + 8])

    def main(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
