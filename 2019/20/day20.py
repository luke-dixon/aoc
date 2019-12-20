from collections import namedtuple
from collections.abc import Mapping
from functools import cached_property
from typing import Dict, Iterator, List, Tuple

from .. import bfs, math, puzzle


class Grid(Mapping):
    def __iter__(self) -> Iterator[Tuple[int, int]]:
        return iter(self.data.keys())

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, k: Tuple[int, int]) -> str:
        return self.data[k]

    def __init__(self, data):
        self.portal_squares: Dict[str, List[Tuple[int, int]]] = {}
        self.portals_by_pos: Dict[Tuple[int, int], str] = {}
        self.start_position = (0, 0)
        self.end_position = (0, 0)
        self.data: Dict[Tuple[int, int], str] = {}
        self.min_x, self.max_x = math.inf, 0
        self.min_y, self.max_y = math.inf, 0
        for y, row in enumerate(data.splitlines()):
            for x, c in enumerate(row):
                if c == ' ':
                    continue
                if c == '#':
                    continue
                elif c == '.':
                    self.data[(y, x)] = '.'
                    self.min_x = min(x, self.min_x)
                    self.max_x = max(x, self.max_x)
                    self.min_y = min(y, self.min_y)
                    self.max_y = max(y, self.max_y)
                    continue
                elif ord(c) in set(range(ord('A'), ord('Z') + 1)):
                    self.portals_by_pos[(y, x)] = c
                    if c not in self.portal_squares:
                        self.portal_squares[c] = []
                    self.portal_squares[c].append((y, x))
                    self.data[(y, x)] = c
                else:
                    print(y, x, c)
                    assert False

        self.movable = {'.', *list(self.portal_squares.keys())}
        self.portal_to_open_spaces = {}
        self.open_space_to_portal = {}
        for pos, c in self.portals_by_pos.items():
            if (pos[0] + 1, pos[1]) in self.portals_by_pos:
                c2 = self.portals_by_pos[pos[0] + 1, pos[1]]
                if (pos[0] - 1, pos[1]) in self.data and self.data[
                    (pos[0] - 1, pos[1])
                ] == '.':
                    open_space = (pos[0] - 1, pos[1])
                else:
                    open_space = (pos[0] + 2, pos[1])

                if (c, c2) == ('A', 'A'):
                    self.start_position = open_space
                if (c, c2) == ('Z', 'Z'):
                    self.end_position = open_space

                if f'{c}{c2}' not in self.portal_to_open_spaces:
                    self.portal_to_open_spaces[f'{c}{c2}'] = set()
                self.portal_to_open_spaces[f'{c}{c2}'].add(open_space)
                self.open_space_to_portal[open_space] = f'{c}{c2}'

            if (pos[0], pos[1] + 1) in self.portals_by_pos:
                c2 = self.portals_by_pos[pos[0], pos[1] + 1]
                if (pos[0], pos[1] - 1) in self.data and self.data[
                    (pos[0], pos[1] - 1)
                ] == '.':
                    open_space = (pos[0], pos[1] - 1)
                else:
                    open_space = (pos[0], pos[1] + 2)

                if (c, c2) == ('A', 'A'):
                    self.start_position = open_space
                if (c, c2) == ('Z', 'Z'):
                    self.end_position = open_space

                if f'{c}{c2}' not in self.portal_to_open_spaces:
                    self.portal_to_open_spaces[f'{c}{c2}'] = set()
                self.portal_to_open_spaces[f'{c}{c2}'].add(open_space)
                self.open_space_to_portal[open_space] = f'{c}{c2}'

        for portal, open_spaces in self.portal_to_open_spaces.items():
            if portal == 'AA':
                assert len(open_spaces) == 1
            elif portal == 'ZZ':
                assert len(open_spaces) == 1
            else:
                if len(open_spaces) != 2:
                    print(portal, open_spaces)
                assert len(open_spaces) == 2

        self.warp_to = {}
        for portal, open_spaces in self.portal_to_open_spaces.items():
            for open_space in open_spaces:
                if len(open_spaces.difference({open_space})) == 1:
                    (other,) = open_spaces.difference({open_space})
                    self.warp_to[open_space] = other

        self.neighbours = {}
        for position in self.data:
            self.neighbours[position] = set()
            for y in [-1, 1]:
                if (position[0] + y, position[1]) in self.data:
                    self.neighbours[position].add((position[0] + y, position[1]))
            for x in [-1, 1]:
                if (position[0], position[1] + x) in self.data:
                    self.neighbours[position].add((position[0], position[1] + x))

        self.inner_portals = set()
        for position in self.open_space_to_portal:
            if (self.min_y + 3 < position[0] < self.max_y - 3) and (
                self.min_x + 3 < position[1] < self.max_x - 3
            ):
                self.inner_portals.add(position)


State = namedtuple('State', ['position', 'path_length'])
State2 = namedtuple('State', ['position', 'path_length', 'level'])


class BFSp1(bfs.BFS):
    def __init__(self, grid: Grid):
        super().__init__()
        self.grid = grid
        self.visited = set()

    def initialise_queue(self):
        self.q.clear()
        self.q.append(State(self.grid.start_position, 0,))

    def break_condition(self, state):
        return state.position == self.grid.end_position

    def skip_state_condition(self, state):
        if (state.position,) in self.visited:
            return True

    def add_to_visited(self, state):
        self.visited.add(state.position)

    def get_neighbours(self, state):
        return self.grid.neighbours[state.position]

    def process_neighbour(self, state, neighbour):
        if neighbour in self.visited:
            return
        elif neighbour in self.grid.portals_by_pos:
            if state.position in self.grid.warp_to:
                self.q.append(
                    State(self.grid.warp_to[state.position], state.path_length + 1)
                )
        elif self.grid[neighbour] == '.':
            self.q.append(State(neighbour, state.path_length + 1))
        else:
            assert False, 'unhandled neighbour'


class BFSp2(BFSp1):
    def __init__(self, grid: Grid):
        super().__init__(grid)
        self.min_level = 0
        self.max_level = 200

    def initialise_queue(self):
        self.q.clear()
        self.q.append(State2(self.grid.start_position, 0, 0,))

    def break_condition(self, state):
        return state.position == self.grid.end_position and state.level == 0

    def skip_state_condition(self, state):
        if (state.position, state.level,) in self.visited:
            return True

    def add_to_visited(self, state):
        self.visited.add((state.position, state.level))

    def process_neighbour(self, state, neighbour):
        if neighbour in self.grid.portals_by_pos:
            if state.position in self.grid.warp_to:
                if state.position in self.grid.inner_portals:
                    if state.level < self.max_level:
                        self.q.append(
                            State2(
                                self.grid.warp_to[state.position],
                                state.path_length + 1,
                                state.level + 1,
                            )
                        )
                else:
                    if state.level > self.min_level:
                        self.q.append(
                            State2(
                                self.grid.warp_to[state.position],
                                state.path_length + 1,
                                state.level - 1,
                            )
                        )
        elif (neighbour, state.level) in self.visited:
            return
        elif self.grid[neighbour] == '.':
            self.q.append(State2(neighbour, state.path_length + 1, state.level))
        else:
            assert False, 'unhandled neighbour'


class Day20(puzzle.Puzzle):
    year = '2019'
    day = '20'

    @cached_property
    def data(self):
        data = self.input_data
        return Grid(data)

    def part1(self):
        return BFSp1(self.data).search().path_length

    def part2(self):
        return BFSp2(self.data).search().path_length

    def main(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
