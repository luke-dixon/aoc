from functools import lru_cache

from lib import puzzle


def calc_biodiversity(grid):
    total = 0
    for i, cell in enumerate(grid):
        if cell == '#':
            total += 2**i
    return total


adjacent = ((0, 1), (0, -1), (-1, 0), (1, 0))


def mutate(grid):
    new_data = []
    for y, row in enumerate(grid):
        s = ''
        for x, cell in enumerate(row):
            adjacent_bugs = 0
            for ay, ax in adjacent:
                if y + ay < 0 or x + ax < 0:
                    continue
                try:
                    if grid[y + ay][x + ax] == '#':
                        adjacent_bugs += 1
                except IndexError:
                    pass
            #print((y, x), adjacent_bugs)
            if cell == '#':
                if adjacent_bugs != 1:
                    s += '.'
                else:
                    s += '#'
            elif cell == '.':
                if adjacent_bugs in {1, 2}:
                    s += '#'
                else:
                    s += '.'

        new_data.append(s)
    return new_data


@lru_cache
def get_adjacent2(y, x):
    assert not (y == 2) or not (x == 2)
    adjacent = []
    for ay, ax in ((0, 1), (0, -1), (-1, 0), (1, 0)):
        if (y + ay, x + ax) == (2, 2):
            if y == 2:
                for i in range(5):
                    adjacent.append((1, i, 0 if x == 1 else 4))
            elif x == 2:
                for i in range(5):
                    adjacent.append((1, 0 if y == 1 else 4, i))
        elif y + ay < 0:
            adjacent.append((-1, 1, 2))
        elif y + ay > 4:
            adjacent.append((-1, 3, 2))
        elif x + ax < 0:
            adjacent.append((-1, 2, 1))
        elif x + ax > 4:
            adjacent.append((-1, 2, 3))
        else:
            adjacent.append((0, y + ay, x + ax))

    return tuple(adjacent)


def mutate2(grids):
    new_grids = []

    for row in grids[0]:
        if '#' in row:
            grids.insert(0, ['.....'] * 5)
            break
    for row in grids[-1]:
        if '#' in row:
            grids.append(['.....'] * 5)

    for n, grid in enumerate(grids):
        new_grid = []
        for y, row in enumerate(grid):
            s = ''
            for x, cell in enumerate(row):
                if (y, x) == (2, 2):
                    # skip middle tile
                    s += '?'
                    continue
                adjacent_bugs = 0
                for level, ay, ax in get_adjacent2(y, x):
                    if n + level < 0:
                        continue
                    if n + level > len(grids) - 1:
                        continue
                    if grids[n + level][ay][ax] == '#':
                        adjacent_bugs += 1
                # print((y, x), adjacent_bugs)
                if cell == '#':
                    if adjacent_bugs != 1:
                        s += '.'
                    else:
                        s += '#'
                elif cell == '.':
                    if adjacent_bugs in {1, 2}:
                        s += '#'
                    else:
                        s += '.'

            new_grid.append(s)
        new_grids.append(new_grid)

    return new_grids


def paint_grid(grid):
    return '\n'.join(grid)


class Day24(puzzle.Puzzle):
    year = '2019'
    day = '24'

    def add_additional_args(self, parser):
        parser.add_argument('-d', '--draw', action='store_true')

    def get_data(self):
        data = self.input_data
        return data.splitlines()

    def part1(self):
        data = self.get_data()
        seen = set()
        biodiversity = calc_biodiversity(''.join(data))
        while biodiversity not in seen:
            if self.args.draw:
                print(paint_grid(data))
                print(biodiversity)
                print()
            seen.add(biodiversity)
            data = mutate(data)
            biodiversity = calc_biodiversity(''.join(data))

        return biodiversity

    def part2(self):
        grids = [self.get_data()]

        for grid in grids:
            print(paint_grid(grid))
            print()

        for _ in range(200):
            grids = mutate2(grids)

        for grid in grids:
            print(paint_grid(grid))
            print()

        print(get_adjacent2(1, 2))

        total_bugs = 0
        for grid in grids:
            for row in grid:
                for cell in row:
                    if cell == '#':
                        total_bugs += 1

        return total_bugs

    def main(self):
        #print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
