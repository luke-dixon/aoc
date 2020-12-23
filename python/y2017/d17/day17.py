from collections import deque

from lib import puzzle


class Day17(puzzle.Puzzle):
    year = '2017'
    day = '17'

    def get_data(self):
        return int(self.input_data.strip())

    def part1(self):
        ring = deque([])

        for i in range(0, 2017 + 1):
            ring.rotate(-self.get_data())
            ring.append(i)

        ring.rotate(-1)
        answer = ring.pop()

        return answer


    def part2(self):
        ring = deque([])

        for i in range(0, 2017 + 1):
            ring.rotate(-self.get_data())
            ring.append(i)

        ring.rotate(-1)

        # Start over
        current = 0
        after_zero = 0

        i = 0
        for i in range(1, 50000000):
            # Each time we go forward x times where x is our input.
            # Afterwards we go forward by 1.
            # The first time through it doesn't matter what we do as there is
            # only one element so it's fine to move what happens afterwards here.
            current = (current + self.get_data() + 1) % (i)
            if current == 0:
                after_zero = i

        return after_zero

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
