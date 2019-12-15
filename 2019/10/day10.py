import math
import operator

from aocd.models import Puzzle

from .. import geometry


class Day10(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=10)

    def get_data(self):
        orig_data = self.input_data
        return orig_data.splitlines()

    def part1(self):
        asteroid_locations = set()
        for y, line in enumerate(self.get_data()):
            for x, c in enumerate(line):
                if c == '#':
                    asteroid_locations.add((x, y))

        asteroids_detected = {}
        for center in asteroid_locations:
            found_angles = set()
            for asteroid in asteroid_locations:
                angle = math.atan2((asteroid[1] - center[1]), asteroid[0] - center[0])
                if angle not in found_angles:
                    found_angles.add(angle)
            asteroids_detected[center] = len(found_angles)

        return max(asteroids_detected.values())

    def part2(self):
        asteroid_locations = set()
        for y, line in enumerate(self.get_data()):
            for x, c in enumerate(line):
                if c == '#':
                    asteroid_locations.add((x, y))

        asteroids_detected = {}
        for center in asteroid_locations:
            found_angles = set()
            for asteroid in asteroid_locations:
                angle = math.atan2((asteroid[1] - center[1]), asteroid[0] - center[0])
                if angle not in found_angles:
                    found_angles.add(angle)
            asteroids_detected[center] = len(found_angles)

        center = max(asteroids_detected.items(), key=operator.itemgetter(1))[0]

        asteroids_destroyed = []
        while True:
            asteroids_detected2 = {}
            for asteroid in asteroid_locations:
                angle = math.atan2(
                    (asteroid[1] - center[1]), asteroid[0] - center[0]
                ) - 3 * math.atan2(1, 0)
                if angle not in asteroids_detected2:
                    asteroids_detected2[angle] = (
                        asteroid[0] - center[0],
                        asteroid[1] - center[1],
                    )
                else:
                    current_location = asteroids_detected2[angle]
                    if geometry.taxicab_distance(
                        current_location, (0, 0)
                    ) > geometry.taxicab_distance(
                        (asteroid[0] - center[0], asteroid[1] - center[1]), (0, 0)
                    ):
                        asteroids_detected2[angle] = (
                            asteroid[0] - center[0],
                            asteroid[1] - center[1],
                        )

            asteroids_detected3 = {}
            for angle, location in asteroids_detected2.items():
                while angle < 0:
                    angle += 2 * math.pi
                asteroids_detected3[angle] = location

            for angle in sorted(asteroids_detected3.keys()):
                location = asteroids_detected3[angle]
                asteroid_locations.remove(
                    (location[0] + center[0], location[1] + center[1])
                )
                asteroids_destroyed.append(
                    (location[0] + center[0], location[1] + center[1])
                )

            if not asteroid_locations or not asteroids_detected2:
                break

        return asteroids_destroyed[199][0] * 100 + asteroids_destroyed[199][1]


def main():
    puzzle = Day10()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')
