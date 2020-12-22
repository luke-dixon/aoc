from collections import deque, namedtuple
from collections.abc import Mapping
from typing import Deque, Dict, Iterator, Tuple

from lib import puzzle


class Grid(Mapping):
    def __iter__(self) -> Iterator[Tuple[int, int]]:
        return self.data.keys()

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, k: Tuple[int, int]) -> str:
        return self.data[k]

    def __init__(self, data):
        self.keys: Dict[str, Tuple[int, int]] = {}
        self.pos_to_key: Dict[Tuple[int, int], str] = {}
        self.doors: Dict[str, Tuple[int, int]] = {}
        self.pos_to_door: Dict[Tuple[int, int], str] = {}
        self.start_position = (0, 0)
        self.data: Dict[Tuple[int, int], str] = {}
        for y, row in enumerate(data.splitlines()):
            for x, c in enumerate(row):
                if c == '#':
                    continue
                elif c == '.':
                    self.data[(y, x)] = '.'
                    continue
                elif c == '@':
                    self.start_position = (y, x)
                    self.data[(y, x)] = c
                elif ord(c) in set(range(ord('a'), ord('z') + 1)):
                    self.keys[c] = (y, x)
                    self.pos_to_key[(y, x)] = c
                    self.data[(y, x)] = c
                elif ord(c) in set(range(ord('A'), ord('Z') + 1)):
                    self.doors[c] = (y, x)
                    self.pos_to_door[(y, x)] = c
                    self.data[(y, x)] = c
                else:
                    assert False
        self.key_pos_to_door_pos = {}
        for key, key_pos in self.keys.items():
            try:
                door_pos = self.doors[key.upper()]
                self.key_pos_to_door_pos[key_pos] = door_pos
            except KeyError:
                pass

        self.movable = {'.', '@', *list(self.keys.keys())}


class Grid2(Grid):
    def __init__(self, data):
        super().__init__(data)

        self.data[self.start_position] = '#'
        self.start_positions = []
        for y in [1, -1]:
            for x in [1, -1]:
                pos = (self.start_position[1] + y, self.start_position[0] + x)
                self.data[pos] = '@'
                self.start_positions.append(pos)

        for y in [-1, 1]:
            self.data[(self.start_position[1] + y, self.start_position[0])] = '#'
        for x in [-1, 1]:
            self.data[(self.start_position[1], self.start_position[0] + x)] = '#'


State = namedtuple(
    'State',
    [
        'position',
        'path_length',
        'collected',
        'opened',
        'visited',
        'searching_from_position',
    ],
)


class BFS:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.q: Deque[State] = deque([])
        self.searching_from = {}
        self.max_collected = 0
        self.max_visited = 0

    def initialise_queue(self):
        self.q.clear()
        self.q.append(
            State(
                self.grid.start_position,
                0,
                set(),
                set(),
                set(),
                self.grid.start_position,
            )
        )

    def break_condition(self, state):
        return len(state.collected) == len(self.grid.keys)

    def skip_state_condition(self, state):
        if len(state.visited) == 0:
            if (
                state.searching_from_position,
                tuple(sorted(state.collected)),
            ) not in self.searching_from:
                self.searching_from[
                    (state.searching_from_position, tuple(sorted(state.collected)))
                ] = state.visited
            else:
                # Abandon paths that reached somewhere we've already been, but in more steps
                return True

        if len(state.collected) + 3 < self.max_collected:
            return True
        if (
            len(state.collected) == self.max_collected
            and len(state.visited) + 50 < self.max_visited
        ):
            return True
        if len(state.collected) > self.max_collected:
            self.max_collected = max(len(state.collected), self.max_collected)
            self.max_visited = 0

    def add_to_visited(self, state):
        state.visited.add(state.position)

    def get_neighbours(self, state):
        n = state.position
        return [(n[0] + 1, n[1]), (n[0] - 1, n[1]), (n[0], n[1] + 1), (n[0], n[1] - 1)]

    def process_neighbour(self, state, neighbour):
        y, x = neighbour
        new_collected = state.collected
        new_opened = state.opened
        new_visited = state.visited
        new_searching_from_position = state.searching_from_position
        if (y, x) in new_visited:
            return
        if ((y, x) in self.grid and self.grid[(y, x)]) in self.grid.movable or (
            y,
            x,
        ) in state.opened:
            if (y, x) in self.grid.pos_to_key and (y, x) not in new_collected:
                new_collected = set(state.collected)
                new_opened = set(state.opened)
                new_collected.add((y, x))
                if (y, x) in self.grid.key_pos_to_door_pos:
                    new_opened.add(self.grid.key_pos_to_door_pos[(y, x)])
                new_visited = set()
                new_searching_from_position = (y, x)
            self.q.append(
                State(
                    (y, x),
                    state.path_length + 1,
                    new_collected,
                    new_opened,
                    new_visited,
                    new_searching_from_position,
                )
            )

    def search(self):
        self.initialise_queue()
        while len(self.q) > 0:
            state = self.q.popleft()

            if self.skip_state_condition(state):
                continue

            self.add_to_visited(state)

            if self.break_condition(state):
                # Done, exit successfully
                break

            for neighbour in self.get_neighbours(state):
                self.process_neighbour(state, neighbour)
        else:
            # Finished without finding all the keys
            print('Not found')
            return None

        return state.path_length


State2 = namedtuple(
    'State2',
    [
        'positions',
        'robot',
        'path_length',
        'collected',
        'opened',
        'visited',
        'searching_from_positions',
    ],
)


class BFS2(BFS):
    def __init__(self, grid: Grid2):
        self.grid = grid
        self.q: Deque[State2] = deque([])
        self.searching_from = {}
        self.max_collected = 0

    def initialise_queue(self):
        self.q.clear()
        self.q.append(
            State2(
                list(self.grid.start_positions),
                0,
                0,
                set(),
                set(),
                set(),
                list(self.grid.start_positions),
            )
        )

    def skip_state_condition(self, state):
        if len(state.visited) == 0:
            if (
                tuple(state.searching_from_positions),
                state.robot,
                tuple(sorted(state.collected)),
            ) not in self.searching_from:
                self.searching_from[
                    (
                        tuple(state.searching_from_positions),
                        state.robot,
                        tuple(sorted(state.collected)),
                    )
                ] = state.visited
            else:
                # Abandon paths that reached somewhere we've already been, but in more steps
                return True

        if len(state.collected) + 2 < self.max_collected:
            # Abandon paths that have fallen too far behind. Needs tweaking for different inputs.
            return True

        if len(state.collected) > self.max_collected:
            self.max_collected = max(len(state.collected), self.max_collected)

    def add_to_visited(self, state):
        state.visited.add(state.positions[state.robot])

    def get_neighbours(self, state):
        n = state.positions[state.robot]
        return [(n[0] + 1, n[1]), (n[0] - 1, n[1]), (n[0], n[1] + 1), (n[0], n[1] - 1)]

    def process_neighbour(self, state, neighbour):
        y, x = neighbour
        new_positions = list(state.positions)
        new_positions[state.robot] = (y, x)
        new_collected = state.collected
        new_opened = state.opened
        new_visited = state.visited
        new_searching_from_positions = list(state.searching_from_positions)
        if (y, x) in new_visited:
            return
        if ((y, x) in self.grid and self.grid[(y, x)]) in self.grid.movable or (
            y,
            x,
        ) in state.opened:
            if (y, x) in self.grid.pos_to_key and (y, x) not in new_collected:
                new_collected = set(state.collected)
                new_opened = set(state.opened)
                new_collected.add((y, x))
                if (y, x) in self.grid.key_pos_to_door_pos:
                    new_opened.add(self.grid.key_pos_to_door_pos[(y, x)])
                new_visited = set()
                new_searching_from_positions[state.robot] = (y, x)
                new_robot = state.robot
                for _ in range(3):
                    new_robot = (new_robot + 1) % 4
                    self.q.append(
                        State2(
                            list(new_positions),
                            new_robot,
                            state.path_length + 1,
                            set(new_collected),
                            set(new_opened),
                            set(new_visited),
                            list(new_searching_from_positions),
                        )
                    )
            self.q.append(
                State2(
                    new_positions,
                    state.robot,
                    state.path_length + 1,
                    new_collected,
                    new_opened,
                    new_visited,
                    new_searching_from_positions,
                )
            )
        elif (y, x) in self.grid.pos_to_door:
            # Switch robots, but stay next to the door
            new_robot = state.robot
            for _ in range(3):
                new_robot = (new_robot + 1) % 4
                self.q.append(
                    State2(
                        list(state.positions),
                        new_robot,
                        state.path_length,
                        set(state.collected),
                        set(state.opened),
                        set(),
                        state.searching_from_positions,
                    )
                )


class Day18(puzzle.Puzzle):
    year = '2019'
    day = '18'

    def get_data(self):
        data = self.input_data
        return data

    def part1(self):
        result = BFS(Grid(self.get_data())).search()
        if result is None:
            print('Not found')
            return
        return result

    def part2(self):
        result = BFS2(Grid2(self.get_data())).search()
        if result is None:
            print('Not found')
            return
        return result

    def main(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
