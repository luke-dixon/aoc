import itertools
import re
import time
from collections import deque

from .. import geometry, math
from lib import puzzle


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


def draw_moons(moons, dimensions):
    min_x = min([moon.position[dimensions[0]] for moon in moons])
    min_y = min([moon.position[dimensions[1]] for moon in moons])
    max_x = max([moon.position[dimensions[0]] for moon in moons])
    max_y = max([moon.position[dimensions[1]] for moon in moons])

    s = ''

    for y in range(min(min_y, -30), max(max_y + 1, 30)):
        for x in range(min(min_x, -30), max(max_x + 1, 30)):
            if (x, y) == (
                moons[0].position[dimensions[0]],
                moons[0].position[dimensions[1]],
            ):
                s += 'O'
            elif (x, y) == (
                moons[1].position[dimensions[0]],
                moons[1].position[dimensions[1]],
            ):
                s += '@'
            elif (x, y) == (
                moons[2].position[dimensions[0]],
                moons[2].position[dimensions[1]],
            ):
                s += '#'
            elif (x, y) == (
                moons[3].position[dimensions[0]],
                moons[3].position[dimensions[1]],
            ):
                s += '+'
            else:
                s += ' '
        s += '\n'
    s += f'x: {(min_x, max_x)}, y: {(min_y, max_y)}'
    s += '\n'
    return s


class MoonDimension:
    PATTERN_SIZE = 8

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


class Day12(puzzle.Puzzle):
    year = '2019'
    day = '12'

    def add_additional_args(self, parser):
        parser.add_argument('-d', '--draw', action='store_true')

    def get_data(self):
        cleaned_data = []
        data = self.input_data
        data = '''<x=-9, y=-1, z=-1>\n<x=2, y=9, z=5>\n<x=10, y=18, z=-12>\n<x=-6, y=15, z=-7>'''
        for d in data.splitlines():
            m = re.search(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', d)
            cleaned_data.append(
                geometry.Point3D(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            )
        return cleaned_data

    def get_moons(self):
        moons = []
        for moon_position in self.get_data():
            moons.append(
                Moon(position=moon_position, velocity=geometry.Point3D(0, 0, 0))
            )
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

            if self.args.draw:
                print(draw_moons(moons, [0, 1]))
                time.sleep(0.2)

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

            lcms.append(math.lcmv([moon.steps for moon in moons]))

        return math.lcmv(lcms)

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
