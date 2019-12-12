import math
import re
from collections import deque

from aocd.models import Puzzle


class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return f'Point({self.x}, {self.y}, {self.z})'

    @classmethod
    def from_point(cls, other):
        return cls(other.x, other.y, other.z)

    def __getitem__(self, i):
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        if i == 2:
            return self.z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other):
        return all([
            self.x == other.x,
            self.y == other.y,
            self.z == other.z,
        ])


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def lcm3(a, b, c):
    return lcm(a, lcm(b, c))


def lcm4(a, b, c, d):
    return lcm(a, lcm(b, lcm(c, d)))


class Moon:
    def __init__(self, point, velocity, last_point=None, last_velocity=None):
        self.point = point
        self.velocity = velocity
        self.path = []
        self._is_repeating = False

    def is_repeating(self):
        if self._is_repeating:
            return True
        path = self.path
        if len(self.path) % 2 != 0:
            return False
        if len(path) < 4:
            return False
        self._is_repeating = path[:len(path) // 2] == path[len(path) // 2:]
        return self._is_repeating

    def potential_energy(self):
        return sum([abs(e) for e in [self.point.x, self.point.y, self.point.z]])

    def kinetic_energy(self):
        return sum([abs(e) for e in [self.velocity.x, self.velocity.y, self.velocity.z]])

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def __repr__(self):
        return f'Moon(point={repr(self.point)}, velocity={repr(self.velocity)}, path={len(self.path) // 2})'


class Day11(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=12)

    def get_data(self):
        orig_data = '''<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>'''
        orig_data = '''<x=-8, y=-10, z=0>\n<x=5, y=5, z=10>\n<x=2, y=-7, z=3>\n<x=9, y=-8, z=-3>'''

        orig_data = self.input_data
        data = orig_data.splitlines()
        cleaned_data = []
        for d in data:
            m = re.search(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', d)
            cleaned_data.append(Point(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        return cleaned_data

    def part1(self):
        data = self.get_data()
        moons = []
        for d in data:
            moons.append(Moon(d, Point(0, 0, 0)))

        steps = 0

        while True:

            for moon in moons:
                for other_moon in moons:
                    if moon.point.x < other_moon.point.x:
                        moon.velocity.x += 1
                    if moon.point.x > other_moon.point.x:
                        moon.velocity.x -= 1
                    if moon.point.y < other_moon.point.y:
                        moon.velocity.y += 1
                    if moon.point.y > other_moon.point.y:
                        moon.velocity.y -= 1
                    if moon.point.z < other_moon.point.z:
                        moon.velocity.z += 1
                    if moon.point.z > other_moon.point.z:
                        moon.velocity.z -= 1

            for moon in moons:
                moon.point.x += moon.velocity.x
                moon.point.y += moon.velocity.y
                moon.point.z += moon.velocity.z

            steps += 1
            total_energy = sum(moon.total_energy() for moon in moons)
            if steps >= 1000:
                break

        return sum(moon.total_energy() for moon in moons)

    def part2(self):


        lcms = []
        PATTERN_SIZE = 8
        for j in reversed(range(3)):
            moons = []
            for d in self.get_data():
                moons.append(Moon(d, Point(0, 0, 0), Point(0, 0, 0), Point(0, 0, 0)))

            for moon in moons:
                moon.point = {0: moon.point.x, 1: moon.point.y, 2: moon.point.z}[j]
                moon.velocity = 0

            steps = 0
            patterns = [[], [], [], []]
            last = [deque(), deque(), deque(), deque()]
            stabilised = [False, False, False, False]
            while True:
                is_repeating = [moon.is_repeating() for moon in moons]
                for i, moon in enumerate(moons):
                    last[i].append(moon.point)
                    if len(last[i]) > PATTERN_SIZE:
                        last[i].popleft()
                    if steps < PATTERN_SIZE:
                        patterns[i].append(moon.point)
                    if not stabilised[i] and steps > PATTERN_SIZE and list(last[i]) == patterns[i]:
                        stabilised[i] = steps - PATTERN_SIZE + 1

                if all(stabilised):
                    break

                if all([
                    *is_repeating,
                    steps > 2,
                ]):
                    break

                for i, moon in enumerate(moons):
                    for other_moon in moons:
                        if moon == other_moon:
                            continue
                        if moon.point < other_moon.point:
                            moon.velocity += 1
                        if moon.point > other_moon.point:
                            moon.velocity -= 1

                for i, moon in enumerate(moons):
                    moon.point += moon.velocity

                steps += 1

            lcms.append(lcm4(*stabilised))

        return lcm3(*lcms)


def main():
    puzzle = Day11()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')


if __name__ == '__main__':
    main()
