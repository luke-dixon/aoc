from lib import puzzle


class Scanner:
    def __init__(self, depth, range):
        self.depth = depth
        self.range = range
        self._current = 0
        self.direction = 1

    @property
    def current(self):
        if self.direction > 0:
            return self._current
        elif self.direction < 0:
            return self.range - self._current - 1

    def update(self, steps=1):
        self._current = (self._current + steps) % self.range
        if self._current == 0:
            self.direction = -self.direction
            self._current += 1

    def __repr__(self):
        return f'Scanner(current={self.current}, range={self.range}, direction={self.direction}, _current={self._current})'


def run(scanners, player_initial=0):
    caught = 0
    player = player_initial
    while player <= max(scanners):
        if player in scanners and scanners[player].current == 0:
            caught += player * scanners[player].range
        for scanner in scanners:
            scanners[scanner].update()
        player += 1
    return caught


class Day13(puzzle.Puzzle):
    year = '2017'
    day = '13'

    def get_data(self):
        orig_data = self.input_data
#         orig_data = '''\
# 0: 3
# 1: 2
# 4: 4
# 6: 4'''
        return [[int(y) for y in x.strip().split(': ')] for x in orig_data.splitlines()]

    def part1(self):
        scanners = {}
        for d in self.get_data():
            scanners[d[0]] = Scanner(depth=d[0], range=d[1])

        result = run(scanners)
        return result

    def part2(self):
        scanners = {}
        for d in self.get_data():
            scanners[d[0]] = Scanner(depth=d[0], range=d[1])

        i = -1
        found = False
        while not found:
            i += 1
            found = True
            for scanner in scanners:
                if (i + scanner) % (2 * scanners[scanner].range - 2) == 0:
                    found = False
                    break

        return i

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
