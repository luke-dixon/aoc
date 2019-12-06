from collections import defaultdict
import networkx

from aocd.models import Puzzle


class Day6(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=6)
        self.data = self.input_data.splitlines()

        self.universal_center = 'COM'

    def part1(self):
        data = list(self.data)
        orbits = {}
        centers = defaultdict(list)
        for orbit in data:
            key, value = orbit.split(')')
            orbits[value] = key
            centers[key].append(value)

        total_orbits = defaultdict(list)
        for x in orbits:
            try:
                center, obj = orbits[x], x
                while True:
                    total_orbits[x].append(center)
                    center, obj = orbits[center], center
            except KeyError:
                pass

        total = 0
        for x in total_orbits:
            total += len(total_orbits[x])
        return total

    def part2(self):
        data = list(self.data)

        orbits = {}
        for orbit in data:
            key, value = orbit.split(')')
            orbits[value] = key

        orbits_graph = networkx.Graph()

        for orbit in data:
            center, obj = orbit.split(')')
            orbits_graph.add_edge(center, obj)

        return networkx.shortest_path_length(orbits_graph, orbits['YOU'], orbits['SAN'])


def main():
    puzzle = Day6()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')


if __name__ == '__main__':
    main()
