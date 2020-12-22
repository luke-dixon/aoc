from collections import defaultdict

import networkx

from lib import puzzle


class Day06(puzzle.Puzzle):
    year = '2019'
    day = '6'

    universal_center = 'COM'

    def get_data(self):
        return self.input_data.splitlines()

    def part1(self):
        data = list(self.get_data())
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
        data = list(self.get_data())

        orbits = {}
        for orbit in data:
            key, value = orbit.split(')')
            orbits[value] = key

        orbits_graph = networkx.Graph()

        for orbit in data:
            center, obj = orbit.split(')')
            orbits_graph.add_edge(center, obj)

        return networkx.shortest_path_length(orbits_graph, orbits['YOU'], orbits['SAN'])

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
