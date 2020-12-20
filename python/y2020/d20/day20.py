from collections import *
from functools import reduce
from itertools import *
from pprint import pprint

import networkx as nx
import re

from .. import puzzle


Tile = namedtuple('Tile', ['lines', 'top_edge', 'right_edge', 'bottom_edge', 'left_edge'])

TOP_EDGE = 'top_edge'
BOTTOM_EDGE = 'bottom_edge'
RIGHT_EDGE = 'right_edge'
LEFT_EDGE = 'left_edge'
EDGES = [TOP_EDGE, RIGHT_EDGE, BOTTOM_EDGE, LEFT_EDGE]
LINES = 'lines'


def rotate_grid(grid):
    new_grid = []
    for y, row in enumerate(grid):
        new_grid.append([grid[x][len(grid) - y - 1] for x, c in enumerate(row)])

    return new_grid


def assert_edges_consistent(tile):
    lines = tile[LINES]
    assert ''.join(lines[0]) == ''.join(tile[TOP_EDGE]), f"{''.join(lines[0])} != {''.join(tile[TOP_EDGE])}"
    assert ''.join(lines[-1]) == ''.join(tile[BOTTOM_EDGE]), f"{''.join(lines[-1])} != {''.join(tile[BOTTOM_EDGE])}"
    assert ''.join([lines[y][0] for y in range(len(tile[LINES]))]) == ''.join(tile[LEFT_EDGE]), f"{''.join([lines[y][0] for y in range(len(tile[LINES]))])} != {''.join(tile[LEFT_EDGE])}"
    assert ''.join([lines[y][-1] for y in range(len(tile[LINES]))]) == ''.join(tile[RIGHT_EDGE]), f"{''.join([c for c in lines[y][-1] for y in range(len(tile[LINES]))])} != {''.join(tile[RIGHT_EDGE])}"


def rotate_left(tile):
    lines = tile[LINES]
    assert_edges_consistent(tile)

    (
        tile[TOP_EDGE],
        tile[RIGHT_EDGE],
        tile[BOTTOM_EDGE],
        tile[LEFT_EDGE]
    ) = (
        tile[RIGHT_EDGE],
        tile[BOTTOM_EDGE][::-1],
        tile[LEFT_EDGE],
        tile[TOP_EDGE][::-1]
    )
    new_lines = []
    for y, row in enumerate(tile['lines']):
        new_lines.append([lines[x][len(lines) - y - 1] for x, c in enumerate(row)])

    tile['lines'] = new_lines
    print('rotate_left')

    assert_edges_consistent(tile)

def flip_tile(tile):
    assert_edges_consistent(tile)

    (
        tile[TOP_EDGE],
        tile[RIGHT_EDGE],
        tile[BOTTOM_EDGE],
        tile[LEFT_EDGE]
    ) = (
        tile[BOTTOM_EDGE],
        tile[RIGHT_EDGE][::-1],
        tile[TOP_EDGE],
        tile[LEFT_EDGE][::-1]
    )
    lines = tile[LINES]
    new_lines = list(reversed(lines))

    tile['lines'] = new_lines
    print('flip_tile')
    pprint(tile)

    assert_edges_consistent(tile)


class Day20(puzzle.Puzzle):
    year = '2020'
    day = '20'

    def get_data(self):
        orig_data = self.input_data.splitlines()
        data = orig_data

        data = '''Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...'''.splitlines()

        data = orig_data

        tiles = {}
        current_tile = None
        current_tile_value = {}
        for line in data:
            if line.startswith('Tile '):
                current_tile = int(line.split(' ')[1].rstrip(':'))
                tiles[current_tile] = {'lines': []}
            elif line == '':
                current_tile = None
            else:
                print(current_tile)
                tiles[current_tile]['lines'].append([c for c in line])

        for tile, value in tiles.items():
            lines = value['lines']

            right_edge = left_edge = [lines[y][-1] for y in range(len(lines))]

            left_edge = [lines[y][0] for y in range(len(lines))]

            # Top
            value[TOP_EDGE] = lines[0]
            # Right
            value[RIGHT_EDGE] = right_edge
            # Bottom
            value[BOTTOM_EDGE] = lines[-1]
            # Left
            value[LEFT_EDGE] = left_edge

        return tiles

    def part1(self):
        tiles = self.get_data()

        pprint(tiles)

        edge_counter = Counter()
        for tile_id, tile in tiles.items():
            edge_counter.update([
                ''.join(tile[TOP_EDGE]),
                ''.join(tile[RIGHT_EDGE]),
                ''.join(tile[BOTTOM_EDGE]),
                ''.join(tile[LEFT_EDGE]),
                ''.join(tile[TOP_EDGE][::-1]),
                ''.join(tile[RIGHT_EDGE][::-1]),
                ''.join(tile[BOTTOM_EDGE][::-1]),
                ''.join(tile[LEFT_EDGE][::-1]),
            ])

        pprint(edge_counter)

        edge_pieces = []
        corner_pieces = []
        other_pieces = []
        for tile_id, tile in tiles.items():
            edges = 0
            for edge in [TOP_EDGE, RIGHT_EDGE, BOTTOM_EDGE, LEFT_EDGE]:
                if edge_counter[''.join(tile[edge])] == 1:
                    edges += 1
            if edges == 0:
                other_pieces.append(tile_id)
            elif edges == 1:
                edge_pieces.append(tile_id)
            elif edges  == 2:
                corner_pieces.append(tile_id)
            else:
                assert False, f"This piece has too many edges: {tile_id}"

        assert len(corner_pieces) == 4, f"Too many corner pieces found: {corner_pieces}"

        return reduce(lambda x, y: x * y, corner_pieces)

    def part2(self):

        tiles = self.get_data()

        pprint(tiles)

        edge_counter = Counter()
        for tile_id, tile in tiles.items():
            edge_counter.update([
                ''.join(tile[TOP_EDGE]),
                ''.join(tile[RIGHT_EDGE]),
                ''.join(tile[BOTTOM_EDGE]),
                ''.join(tile[LEFT_EDGE]),
                ''.join(tile[TOP_EDGE][::-1]),
                ''.join(tile[RIGHT_EDGE][::-1]),
                ''.join(tile[BOTTOM_EDGE][::-1]),
                ''.join(tile[LEFT_EDGE][::-1]),
            ])

        pprint(edge_counter)

        tile_by_edge = defaultdict(set)
        for tile_id, tile in tiles.items():
            for edge in [TOP_EDGE, RIGHT_EDGE, BOTTOM_EDGE, LEFT_EDGE]:
                tile_by_edge[''.join(tile[edge])].add(tile_id)
                tile_by_edge[''.join(tile[edge][::-1])].add(tile_id)

        edge_pieces = []
        corner_pieces = []
        other_pieces = []
        for tile_id, tile in tiles.items():
            edges = 0
            for edge in [TOP_EDGE, RIGHT_EDGE, BOTTOM_EDGE, LEFT_EDGE]:
                if edge_counter[''.join(tile[edge])] == 1:
                    edges += 1
            if edges == 0:
                other_pieces.append(tile_id)
            elif edges == 1:
                edge_pieces.append(tile_id)
            elif edges == 2:
                corner_pieces.append(tile_id)
            else:
                assert False, f"This piece has too many edges: {tile_id}"

        assert len(corner_pieces) == 4, f"Too many corner pieces found: {corner_pieces}"

        print(corner_pieces)
        print(len(edge_pieces) / 4)

        edge_pieces = set(edge_pieces)
        #corner_pieces = set(corner_pieces)
        other_pieces = set(other_pieces)

        edges = []
        current_edge = None
        graph = nx.Graph()
        for corner_piece in corner_pieces:
            corner_piece_edges = []
            for edge in [TOP_EDGE, RIGHT_EDGE, BOTTOM_EDGE, LEFT_EDGE]:
                tile = tiles[corner_piece]
                if edge_counter[''.join(tile[edge])] != 2:
                    corner_piece_edges.append(''.join(tile[edge]))
            assert len(corner_piece_edges) == 2

        queue = deque()
        queue.append(list(corner_pieces)[0])
        visited = set()
        while queue:
            current_tile_id = queue.popleft()
            current_tile = tiles[current_tile_id]
            if current_tile_id in visited:
                continue
            visited.add(current_tile_id)

            for edge in EDGES:
                if ''.join(current_tile[edge]) in tile_by_edge:
                    next_edges = list(tile_by_edge[''.join(current_tile[edge])] - {current_tile_id})
                    if next_edges:
                        assert len(next_edges) == 1, f'next_edges length not 1, {next_edges}'
                        queue.append(next_edges[0])
                        graph.add_edge(current_tile_id, next_edges[0])

        pprint(graph[list(corner_pieces)[0]])
        pprint(list(graph[list(corner_pieces)[0]]))

        corners = list(corner_pieces)[0], list(corner_pieces)[2]
        side1 = nx.shortest_path(graph, *corners)
        corners = list(corner_pieces)[0], list(corner_pieces)[3]
        side2 = nx.shortest_path(graph, *corners)
        corners = list(corner_pieces)[2], list(corner_pieces)[1]
        side3 = nx.shortest_path(graph, *corners)
        corners = list(corner_pieces)[3], list(corner_pieces)[1]
        side4 = nx.shortest_path(graph, *corners)
        assert len(side1) == len(side2) == len(side3) == len(side4)

        grid = []
        for x in range(len(side2)):
            grid.append([None] * len(side1))

        grid[0] = side1
        for i, tile_id in enumerate(side2):
            grid[i][0] = tile_id
        grid[-1] = side4
        for i, tile_id in enumerate(side3):
            grid[i][-1] = tile_id

        for row in range(1, 12):
            for col in range(1, 12):
                grid[row][col] = list((set(graph[grid[row - 1][col]]) & set(graph[grid[row][col - 1]])) - {grid[row - 1][col - 1]})[0]

        pprint(grid)
        flip_tile(tiles[grid[0][0]])
        rotate_left(tiles[grid[0][0]])
        rotate_left(tiles[grid[0][0]])

        print(tile_by_edge[''.join(tiles[grid[0][0]][TOP_EDGE])], tile_by_edge[''.join(tiles[grid[0][0]][LEFT_EDGE])], tile_by_edge[''.join(tiles[grid[0][0]][RIGHT_EDGE])], tile_by_edge[''.join(tiles[grid[0][0]][BOTTOM_EDGE])])
        pprint(tiles[grid[0][0]])

        assert len(tile_by_edge[''.join(tiles[grid[0][0]][TOP_EDGE])]) == 1
        assert len(tile_by_edge[''.join(tiles[grid[0][0]][LEFT_EDGE])]) == 1

        for i in range(4):
            rotate_left(tiles[grid[0][1]])
        pprint(tiles[grid[0][1]])
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                print(y, x)
                rotates = 0
                flips = 0
                while True:
                    above_y = y - 1
                    left_x = x - 1
                    matched_y, matched_x = None, None
                    if above_y >= 0:
                        matched_y = tiles[grid[above_y][x]][BOTTOM_EDGE] == tiles[grid[y][x]][TOP_EDGE]
                    if left_x >= 0:
                        matched_x = tiles[grid[y][left_x]][RIGHT_EDGE] == tiles[grid[y][x]][LEFT_EDGE]

                    if matched_y and matched_x:
                        break
                    elif matched_y is None and matched_x:
                        break
                    elif matched_x is None and matched_y:
                        break
                    elif matched_x is None and matched_y is None:
                        assert (y, x) == (0, 0)
                        break
                    elif flips >= 1 and rotates >= 4:
                        assert False, "Not found"
                    elif rotates >= 4:
                        flip_tile(tiles[grid[y][x]])
                        rotates = 0
                        flips += 1
                    else:
                        print(rotates)
                        assert rotates <= 4
                        rotate_left(tiles[grid[y][x]])
                        rotates += 1

        grid2 = []

        for y, row in enumerate(grid):
            tile_size = len(tiles[row[0]][LINES]) - 2
            for _ in range(tile_size):
                grid2.append([])
            for x, tile_id in enumerate(row):
                for i, tile_row in enumerate(tiles[tile_id][LINES][1:-1]):
                    grid2[y * tile_size + i].extend(tile_row[1:-1])
        for row in grid2:
            print(''.join(row))

        sea_monster = '''\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''.splitlines()
        sea_monster_coords = []
        for y, line in enumerate(sea_monster):
            for x, c in enumerate(line):
                if c == '#':
                    sea_monster_coords.append((y, x))
        print(sea_monster_coords)

        rotations = 0
        sea_monsters = []
        while rotations < 4:
            sea_monsters_found = False
            for y, row in enumerate(grid2):
                for x, c in enumerate(row):
                    found = True
                    for my, mx in sea_monster_coords:
                        try:
                            if grid2[y + my][x + mx] != '#':
                                found = False
                                break
                        except IndexError:
                            found = False
                            break
                    if found:
                        print(f"Sea monster found at {y, x}")
                        sea_monsters.append((y, x))
                        sea_monsters_found = True
            if sea_monsters_found:
                break
            print('rotating grid')
            grid2 = rotate_grid(grid2)
            rotations += 1

        pprint(sea_monsters)

        smc = Counter()
        for row in sea_monster:
            for x in row:
                smc.update(x)

        c = Counter()
        for row in grid2:
            for x in row:
                c.update(x)
        print(c, smc)

        print(c['#'] - smc['#'] * len(sea_monsters))

        return c['#'] - smc['#'] * len(sea_monsters)

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
