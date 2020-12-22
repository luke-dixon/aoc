
from collections import *
from itertools import *

from lib import puzzle

Rule = namedtuple('Rule', ['field', 'ranges'])


def draw_grid(grid):
    min_x, min_y, min_z = 0, 0, 0
    max_x, max_y, max_z = 0, 0, 0
    for (x, y, z) in grid:
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)
        min_z, max_z = min(min_z, z), max(max_z, z)

    for z in range(min_z, max_z + 1):
        print(f'z = {z}')
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                print(grid[(x, y, z)], end='')
            print()


class Day17(puzzle.Puzzle):
    year = '2020'
    day = '17'

    def get_data(self):
        orig_data = self.input_data.splitlines()
        data = orig_data

#         data = '''.#.
# ..#
# ###'''.splitlines()

        return data

    def part1(self):
        data = self.get_data()

        grid = defaultdict(lambda: '.')
        for y, line in enumerate(data):
            for x, c in enumerate(line):
                if c == '#':
                    grid[(x, y, 0)] = c

        draw_grid(grid)

        total = len(grid)
        print(f'total: {total}')
        print()

        cycle = 1
        while True:
            new_grid = defaultdict(lambda: '.')

            queue = deque()
            for key in grid:
                queue.append(key)

            visited = set()

            while queue:
                x, y, z = queue.popleft()
                if (x, y, z) in visited:
                    continue
                visited.add((x, y, z))
                if grid[x, y, z] == '.':
                    active_neighbours = 0
                    for ax, ay, az in product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
                        if (0, 0, 0) == (ax, ay, az):
                            continue

                        if grid[(x + ax, y + ay, z + az)] == '#':
                            active_neighbours += 1

                        if active_neighbours > 3:
                            break

                    if active_neighbours > 0:
                        for ax, ay, az in product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
                            if (0, 0, 0) == (ax, ay, az):
                                continue
                            if (x + ax, y + ay, z + az) not in visited:
                                queue.append((x + ax, y + ay, z + az))

                    if active_neighbours == 3:
                        new_grid[(x, y, z)] = '#'

                elif grid[x, y, z] == '#':
                    active_neighbours = 0
                    for ax, ay, az in product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
                        if (0, 0, 0) == (ax, ay, az):
                            continue

                        if grid[(x + ax, y + ay, z + az)] == '#':
                            active_neighbours += 1

                    if active_neighbours > 0:
                        for ax, ay, az in product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
                            if (0, 0, 0) == (ax, ay, az):
                                continue

                            if (x + ax, y + ay, z + az) not in visited:
                                queue.append((x + ax, y + ay, z + az))

                            if active_neighbours > 3:
                                break

                    if active_neighbours == 3 or active_neighbours == 2:
                        new_grid[(x, y, z)] = '#'
                else:
                    assert False

            print(f'after cycle {cycle}:')
            total = len(new_grid)

            print(f'total: {total}')
            print()

            if cycle == 6:
                break
            cycle += 1
            grid = new_grid

            draw_grid(grid)

        return total

    def part2(self):
        data = self.get_data()

        grid = defaultdict(lambda: '.')
        for y, line in enumerate(data):
            for x, c in enumerate(line):
                if c == '#':
                    grid[(x, y, 0, 0)] = c

        total = len(grid)

        print(f'total: {total}')
        print()

        cycle = 1
        while True:
            new_grid = defaultdict(lambda: '.')

            queue = deque()
            for key in grid:
                queue.append(key)

            visited = set()

            while queue:
                x, y, z, w = queue.popleft()
                if (x, y, z, w) in visited:
                    continue
                visited.add((x, y, z, w))
                if grid[(x, y, z, w)] == '.':
                    active_neighbours = 0
                    for ax, ay, az, aw in product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
                        if (0, 0, 0, 0) == (ax, ay, az, aw):
                            continue

                        if grid[(x + ax, y + ay, z + az, w + aw)] == '#':
                            active_neighbours += 1

                        if active_neighbours > 3:
                            break

                    if active_neighbours == 3:
                        new_grid[(x, y, z, w)] = '#'

                elif grid[x, y, z, w] == '#':
                    active_neighbours = 0
                    for ax, ay, az, aw in product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
                        if (0, 0, 0, 0) == (ax, ay, az, aw):
                            continue

                        if grid[(x + ax, y + ay, z + az, w + aw)] == '#':
                            active_neighbours += 1

                        if active_neighbours > 3:
                            break

                    if active_neighbours > 0:
                        for ax, ay, az, aw in product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
                            if (0, 0, 0, 0) == (ax, ay, az, aw):
                                continue

                            if (x + ax, y + ay, z + az, w + aw) not in visited:
                                queue.append((x + ax, y + ay, z + az, w + aw))
                                pass

                    if active_neighbours == 3 or active_neighbours == 2:
                        new_grid[(x, y, z, w)] = '#'
                else:
                    assert False

            print(f'after cycle {cycle}:')
            total = len(new_grid)
            print(f'total: {total}')
            print()

            if cycle == 6:
                break
            cycle += 1
            grid = new_grid

        return total

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
