import functools
import itertools
import math
import re
import sys
import time
from collections import deque

from aocd.models import Puzzle


class Point:
    __slots__ = 'data'

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
        self.data[0], self.data[1], self.data[2] = (
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )
        return self

    def __eq__(self, other):
        return all([self.x == other.x, self.y == other.y, self.z == other.z,])


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def lcmv(l):
    return functools.reduce(lcm, l)


class Moon:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def add_velocity(self, other_moon):
        for i in range(3):
            self.velocity[i] += self.position[i] < other_moon.position[i]
            self.velocity[i] -= self.position[i] > other_moon.position[i]

    def apply_velocity(self):
        self.position += self.velocity

    def potential_energy(self):
        return sum(
            [abs(e) for e in [self.position.x, self.position.y, self.position.z]]
        )

    def kinetic_energy(self):
        return sum(
            [abs(e) for e in [self.velocity.x, self.velocity.y, self.velocity.z]]
        )

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def __repr__(self):
        return f'Moon(position={repr(self.position)}, velocity={repr(self.velocity)}, path={len(self.path) // 2})'


def print_moons(moons, dimensions):
    min_x = min([moon.position[dimensions[0]] for moon in moons])
    min_y = min([moon.position[dimensions[1]] for moon in moons])
    max_x = max([moon.position[dimensions[0]] for moon in moons])
    max_y = max([moon.position[dimensions[1]] for moon in moons])

    for y in range(min(min_y, -30), max(max_y + 1, 30)):
        for x in range(min(min_x, -30), max(max_x + 1, 30)):
            if (x, y) == (
                moons[0].position[dimensions[0]],
                moons[0].position[dimensions[1]],
            ):
                print('O', end='')
            elif (x, y) == (
                moons[1].position[dimensions[0]],
                moons[1].position[dimensions[1]],
            ):
                print('@', end='')
            elif (x, y) == (
                moons[2].position[dimensions[0]],
                moons[2].position[dimensions[1]],
            ):
                print('#', end='')
            elif (x, y) == (
                moons[3].position[dimensions[0]],
                moons[3].position[dimensions[1]],
            ):
                print('+', end='')
            else:
                print(' ', end='')
        print()
    print(f'x: {(min_x, max_x)}, y: {(min_y, max_y)}')
    print()
    time.sleep(2)


class MoonDimension:
    PATTERN_SIZE = 9

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.pattern = [self.position]
        self.last = deque([self.position])
        self.stabilised = False
        self.steps = 1 - self.PATTERN_SIZE

    def add_velocity(self, other_moon_dimension):
        self.velocity += self.position < other_moon_dimension.position
        self.velocity -= self.position > other_moon_dimension.position

    def apply_velocity(self):
        self.position += self.velocity

        if not self.stabilised:
            self.steps += 1

            self.last.append(self.position)

            if len(self.last) > self.PATTERN_SIZE:
                self.last.popleft()

            if len(self.pattern) < self.PATTERN_SIZE:
                self.pattern.append(self.position)

            if (
                len(self.pattern) >= self.PATTERN_SIZE
                and len(self.last) >= self.PATTERN_SIZE
                and self.steps > self.PATTERN_SIZE
            ):
                self.stabilised = list(self.last) == self.pattern

    def __repr__(self):
        return f'MoonDimension(position={repr(self.position)}, velocity={repr(self.velocity)})'


class Day11(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=12)

    def get_data(self):
        cleaned_data = []
        for d in self.input_data.splitlines():
            m = re.search(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', d)
            cleaned_data.append(
                Point(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            )
        return cleaned_data

    def get_moons(self):
        moons = []
        for moon_position in self.get_data():
            moons.append(Moon(position=moon_position, velocity=Point(0, 0, 0)))
        return moons

    def get_moons2(self, axis):
        moons = []
        for moon_position in self.get_data():
            moons.append(
                MoonDimension(
                    position={
                        0: moon_position.x,
                        1: moon_position.y,
                        2: moon_position.z,
                    }[axis],
                    velocity=0,
                )
            )
        return moons

    def part1(self):
        moons = self.get_moons()
        for _ in range(1000):

            for moon, other_moon in itertools.permutations(moons, 2):
                moon.add_velocity(other_moon)

            for moon in moons:
                moon.apply_velocity()

            if '-p' in sys.argv:
                print_moons(moons, [0, 1])

        return sum(moon.total_energy() for moon in moons)

    def part2(self):
        lcms = []
        for axis in reversed(range(3)):
            moons = self.get_moons2(axis)

            while not all([moon.stabilised for moon in moons]):

                for moon, other_moon in itertools.permutations(moons, 2):
                    moon.add_velocity(other_moon)

                for moon in moons:
                    moon.apply_velocity()

            lcms.append(lcmv([moon.steps for moon in moons]))

        return lcmv(lcms)


def main():
    puzzle = Day11()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')


if __name__ == '__main__':
    main()
