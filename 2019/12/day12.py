import functools
import itertools
import math
import re
from collections import deque

from aocd.models import Puzzle


class Point:
    __slots__ = ('data')

    def __init__(self, x, y, z):
        self.data = [x, y, z]

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, z={self.z})'

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    @property
    def z(self):
        return self.data[2]

    @x.setter
    def x(self, value):
        self.data[0] = value

    @y.setter
    def y(self, value):
        self.data[1] = value

    @z.setter
    def z(self, value):
        self.data[2] = value

    @classmethod
    def from_point(cls, other):
        return cls(other.x, other.y, other.z)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.data[0], self.data[1], self.data[2] = self.x + other.x, self.y + other.y, self.z + other.z
        return self

    def __eq__(self, other):
        return all([
            self.x == other.x,
            self.y == other.y,
            self.z == other.z,
        ])


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def lcmv(l):
    return functools.reduce(lcm, l)


class Moon:
    def __init__(self, point, velocity, last_point=None, last_velocity=None):
        self.point = point
        self.velocity = velocity
        self.path = []
        self._is_repeating = False

    def add_velocity(self, other_moon):
        for i in range(3):
            self.velocity[i] += self.point[i] < other_moon.point[i]
            self.velocity[i] -= self.point[i] > other_moon.point[i]

    def apply_velocity(self):
        self.point += self.velocity

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
        cleaned_data = []
        for d in self.input_data.splitlines():
            m = re.search(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', d)
            cleaned_data.append(Point(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        return cleaned_data

    def part1(self):
        moons = set()
        for point in self.get_data():
            moons.add(Moon(point=point, velocity=Point(0, 0, 0)))

        for _ in range(1000):

            for moon, other_moon in itertools.permutations(moons, 2):
                moon.add_velocity(other_moon)

            for moon in moons:
                moon.apply_velocity()

        return sum(moon.total_energy() for moon in moons)

    def part2(self):
        lcms = []
        PATTERN_SIZE = 8
        for axis in reversed(range(3)):
            moons = []
            for point in self.get_data():
                moons.append(Moon(point=point, velocity=Point(0, 0, 0)))

            for moon in moons:
                moon.point = {0: moon.point.x, 1: moon.point.y, 2: moon.point.z}[axis]
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

                for moon, other_moon in itertools.permutations(moons, 2):
                    moon.velocity += moon.point < other_moon.point
                    moon.velocity -= moon.point > other_moon.point

                for i, moon in enumerate(moons):
                    moon.point += moon.velocity

                steps += 1

            lcms.append(lcmv(stabilised))

        return lcmv(lcms)


def main():
    puzzle = Day11()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')


if __name__ == '__main__':
    main()
