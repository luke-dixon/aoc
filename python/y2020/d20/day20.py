import random
from collections import Counter, defaultdict, deque
from collections.abc import Sequence
from functools import cached_property, reduce

import networkx as nx

from lib import chargrid, puzzle

SEA_MONSTER = '''\
                  #
#    ##    ##    ###
 #  #  #  #  #  #\
'''

EDGES = ['top_edge', 'right_edge', 'bottom_edge', 'left_edge']


class Tile:
    def __init__(self, grid: chargrid.Grid):
        self.grid = grid
        self.top_edge = ''.join(grid[0])
        self.bottom_edge = ''.join(grid[-1])
        self.right_edge = ''.join([grid[y][-1] for y in range(len(grid))])
        self.left_edge = ''.join([grid[y][0] for y in range(len(grid))])

    def get_possible_edges(self) -> Sequence[str]:
        return [
            self.top_edge,
            self.right_edge,
            self.bottom_edge,
            self.left_edge,
            self.top_edge[::-1],
            self.right_edge[::-1],
            self.bottom_edge[::-1],
            self.left_edge[::-1],
        ]


class Tiles(dict):
    def __init__(self):
        super().__init__()
        self._edge_pieces = []
        self._corner_pieces = []
        self._other_pieces = []

    @classmethod
    def from_data(cls, data):
        tiles = cls()

        grid_by_id = {}
        current_tile_id = None
        for line in data.splitlines():
            if line.startswith('Tile '):
                current_tile_id = int(line.split(' ')[1].rstrip(':'))
                grid_by_id[current_tile_id] = []
            elif line == '':
                current_tile_id = None
            else:
                grid_by_id[current_tile_id].append([c for c in line])

        for tile_id, grid in grid_by_id.items():
            tiles[tile_id] = Tile(grid)

        return tiles

    def _set_piece_types(self):
        edge_counter = Counter()
        for tile_id, tile in self.items():
            edge_counter.update(tile.get_possible_edges())

        self._edge_pieces = []
        self._corner_pieces = []
        self._other_pieces = []
        for tile_id, tile in self.items():
            edges = 0
            for edge in EDGES:
                if edge_counter[getattr(tile, edge)] == 1:
                    edges += 1
            if edges == 0:
                self._other_pieces.append(tile_id)
            elif edges == 1:
                self._edge_pieces.append(tile_id)
            elif edges == 2:
                self._corner_pieces.append(tile_id)
            else:
                assert False, f"This piece has too many edges: {tile_id}"

        assert (
            len(self._corner_pieces) == 4
        ), f"Wrong number of corner pieces found: {self._corner_pieces}"

    @property
    def edge_pieces(self):
        if not self._edge_pieces:
            self._set_piece_types()
        return self._edge_pieces

    @property
    def corner_pieces(self):
        if not self._corner_pieces:
            self._set_piece_types()
        return self._corner_pieces

    @property
    def other_pieces(self):
        if not self._other_pieces:
            self._set_piece_types()
        return self._other_pieces

    @cached_property
    def by_edge(self):
        tile_by_edge = defaultdict(set)
        for tile_id, tile in self.items():
            for edge in EDGES:
                tile_by_edge[getattr(tile, edge)].add(tile_id)
                tile_by_edge[getattr(tile, edge)[::-1]].add(tile_id)
        return dict(tile_by_edge)


def get_sea_monster_coords():
    sea_monster_coords = []
    for y, line in enumerate(SEA_MONSTER.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                sea_monster_coords.append((y, x))
    return sea_monster_coords


def search_for_sea_monsters(grid2, sea_monster_coords):
    sea_monsters = []
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
                sea_monsters.append((y, x))
    return sea_monsters


class Day20(puzzle.Puzzle):
    year = '2020'
    day = '20'

    @cached_property
    def tiles(self):
        tiles = Tiles.from_data(self.input_data)

        return tiles

    def part1(self):
        return reduce(lambda x, y: x * y, self.tiles.corner_pieces)

    def part2(self):

        tiles = self.tiles

        edge_counter = Counter()
        for tile_id, tile in tiles.items():
            edge_counter.update(tile.get_possible_edges())

        for corner_tile in tiles.corner_pieces:
            corner_piece_edges = []
            for edge in EDGES:
                tile = tiles[corner_tile]
                if edge_counter[getattr(tile, edge)] != 2:
                    corner_piece_edges.append(getattr(tile, edge))
            assert len(corner_piece_edges) == 2

        # Build graph of which tiles join with which other tiles
        queue = deque()
        queue.append(tiles.corner_pieces[0])
        visited = set()
        graph = nx.Graph()
        while queue:
            current_tile_id = queue.popleft()
            current_tile = tiles[current_tile_id]
            if current_tile_id in visited:
                continue
            visited.add(current_tile_id)

            for edge in EDGES:
                if ''.join(getattr(current_tile, edge)) in tiles.by_edge:
                    next_edges = list(
                        tiles.by_edge[getattr(current_tile, edge)] - {current_tile_id}
                    )
                    if next_edges:
                        assert (
                            len(next_edges) == 1
                        ), f'next_edges length not 1, {next_edges}'
                        queue.append(next_edges[0])
                        graph.add_edge(current_tile_id, next_edges[0])

        # Figure out which corners go where

        # Choose an arbitrary corner tile to be the top left tile
        top_left_corner_tile = random.choice(tiles.corner_pieces)

        # Find the shortest paths to each of the other corners
        shortest_paths = {}
        for corner_tile in tiles.corner_pieces:
            if corner_tile != top_left_corner_tile:
                shortest_paths[corner_tile] = nx.shortest_path(
                    graph, top_left_corner_tile, corner_tile
                )

        # The furthest away is the bottom left
        bottom_right_corner_tile = None
        for corner in shortest_paths:
            if bottom_right_corner_tile not in shortest_paths:
                bottom_right_corner_tile = corner
            else:
                if len(shortest_paths[corner]) > len(
                    shortest_paths[bottom_right_corner_tile]
                ):
                    bottom_right_corner_tile = corner

        # It doesn't matter which the other two are
        top_right_corner_tile, bottom_left_corner_tile = random.sample(
            set(shortest_paths.keys()) - {bottom_right_corner_tile}, 2
        )

        top_edge_tiles = shortest_paths[top_right_corner_tile]
        left_edge_tiles = shortest_paths[bottom_left_corner_tile]
        right_edge_tiles = nx.shortest_path(
            graph, top_right_corner_tile, bottom_right_corner_tile
        )
        bottom_edge_tiles = nx.shortest_path(
            graph, bottom_left_corner_tile, bottom_right_corner_tile
        )
        assert (
            len(top_edge_tiles)
            == len(left_edge_tiles)
            == len(right_edge_tiles)
            == len(bottom_edge_tiles)
        )

        # Next we want to figure out where each tile goes
        # First, create a grid with empty slots
        tile_grid = []
        for x in range(len(left_edge_tiles)):
            tile_grid.append([None] * len(top_edge_tiles))

        # Now place the top corners and edge pieces on the grid
        tile_grid[0] = top_edge_tiles

        # Place the left corners and edge pieces on the grid
        for i, tile_id in enumerate(left_edge_tiles):
            tile_grid[i][0] = tile_id

        # Place the bottom corners and edge pieces on the grid
        tile_grid[-1] = bottom_edge_tiles

        # Place the right corners and edge pieces on the grid
        for i, tile_id in enumerate(right_edge_tiles):
            tile_grid[i][-1] = tile_id

        # Add the rest of the pieces to the grid by checking against the left and top tiles
        for row in range(1, 12):
            for col in range(1, 12):
                tile_grid[row][col] = list(
                    (
                        set(graph[tile_grid[row - 1][col]])
                        & set(graph[tile_grid[row][col - 1]])
                    )
                    - {tile_grid[row - 1][col - 1]}
                )[0]

        # Get top left tile in correct orientation
        for tile_lines in chargrid.symmetries(tiles[tile_grid[0][0]].grid):
            tiles[tile_grid[0][0]] = Tile(tile_lines)
            if all(
                [
                    len(tiles.by_edge[tiles[tile_grid[0][0]].top_edge]) == 1,
                    len(tiles.by_edge[tiles[tile_grid[0][0]].left_edge]) == 1,
                    tiles[tile_grid[0][0]].right_edge
                    in tiles[tile_grid[0][1]].get_possible_edges(),
                ]
            ):
                break
        else:
            assert False, "Couldn't find correct orientation for top left grid"

        # Get rest of tiles in correct orientation
        for y, row in enumerate(tile_grid):
            for x, col in enumerate(row):
                current_tile = tiles[tile_grid[y][x]]
                above_y = y - 1
                left_x = x - 1
                for tiles_grid in chargrid.symmetries(current_tile.grid):
                    tiles[tile_grid[y][x]] = current_tile = Tile(tiles_grid)
                    matched_y, matched_x = None, None
                    if above_y >= 0:
                        matched_y = (
                            tiles[tile_grid[above_y][x]].bottom_edge
                            == current_tile.top_edge
                        )
                    if left_x >= 0:
                        matched_x = (
                            tiles[tile_grid[y][left_x]].right_edge
                            == current_tile.left_edge
                        )

                    if any(
                        [
                            matched_y and matched_x,
                            matched_y is None and matched_x,
                            matched_x is None and matched_y,
                            matched_x is None and matched_y is None,
                        ]
                    ):
                        break

        # Place tiles on grid, stripping edges
        habitat_grid = []
        for y, row in enumerate(tile_grid):
            tile_size = len(tiles[row[0]].grid) - 2
            for _ in range(tile_size):
                habitat_grid.append([])
            for x, tile_id in enumerate(row):
                for i, tile_row in enumerate(tiles[tile_id].grid[1:-1]):
                    habitat_grid[y * tile_size + i].extend(tile_row[1:-1])

        # Search for sea monsters
        sea_monster_coords = get_sea_monster_coords()
        sea_monsters = []
        for tile_grid in chargrid.symmetries(habitat_grid):
            sea_monsters = search_for_sea_monsters(tile_grid, sea_monster_coords)
            if sea_monsters:
                break

        # Determine how rough the waters are
        c = Counter()
        for row in habitat_grid:
            for x in row:
                c.update(x)
        return c['#'] - len(sea_monster_coords) * len(sea_monsters)

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
