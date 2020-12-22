import random
import time
from collections import defaultdict, deque

import networkx as nx

from .. import intcode
from lib import puzzle


class GridInputDevice(intcode.InputDevice):
    def __init__(self, grid, next_value):
        self.grid = grid
        self.next_value = next_value

    def read(self):
        if not self.next_value:
            value = next(self.grid)
        else:
            value = self.next_value.pop(0)
        return value


class GridOutputDevice(intcode.OutputDevice):
    def __init__(self, grid, next_value):
        self.grid = grid
        self.value = []
        self.next_value = next_value

    def write(self, value: int) -> None:
        self.next_value.append(self.grid.send(value))


class FullyExplored(Exception):
    def __init__(self, payload):
        self.payload = payload
        super().__init__()


def grid_gen(grid, draw=False):
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    x, y = 0, 0
    o_x, o_y = 0, 1

    direction_to_code = {
        (0, 1): 1,
        (0, -1): 2,
        (-1, 0): 3,
        (1, 0): 4,
    }
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    grid[(x, y)] = 'D'

    g = nx.Graph()

    to_explore_set = {(0, 0)}
    to_explore = deque([(0, 0)])

    exploring = to_explore.pop()
    to_explore_set.remove(exploring)
    explored_current = set()
    explored = set()

    oxygen_location = None

    yield 'started'
    while True:
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)

        if draw:
            print(paint_grid(grid, range(min(-22, min_x - 2), max(20, max_x + 3)), range(min(-18, min_y - 2), max(22, max_y + 3))))
            time.sleep(0.015)

        status = yield direction_to_code[(o_x, o_y)]

        origin = (0, 0)

        if status == 0:
            # hit wall
            grid[(x + o_x, y + o_y)] = '#'
            explored.add((x + o_x, y + o_y))
        elif status == 1:
            # empty space
            grid[(x, y)] = 'O' if (x, y) == oxygen_location else ' '
            if (x + o_x, y + o_y) not in explored and (
                x + o_x,
                y + o_y,
            ) not in to_explore_set:
                to_explore_set.add((x + o_x, y + o_y))
                to_explore.append((x + o_x, y + o_y))
            g.add_edge((x, y), (x + o_x, y + o_y))
            x, y = x + o_x, y + o_y
            grid[(x, y)] = 'D'
        elif status == 2:
            # found oxygen
            if (x + o_x, y + o_y) not in explored and (
                x + o_x,
                y + o_y,
            ) not in to_explore_set:
                to_explore_set.add((x + o_x, y + o_y))
                to_explore.append((x + o_x, y + o_y))
            g.add_edge((x, y), (x + o_x, y + o_y))
            x, y = x + o_x, y + o_y
            grid[(x, y)] = 'O'
            if not oxygen_location:
                oxygen_location = (x, y)

        if (x, y) == exploring and len(explored_current) < 4:
            # Pick a square around the one we are currently exploring
            for dx, dy in random.sample(directions, k=len(directions)):
                if (x + dx, y + dy) not in explored_current:
                    o_x, o_y = dx, dy
                    break
            explored_current.add((x + o_x, y + o_y))
            continue
        elif (x, y) != exploring and len(explored_current) < 4:
            # Get back to the square we are exploring from
            path = nx.shortest_path(g, (x, y), exploring)
            if x > path[1][0]:
                o_x = -1
            elif x < path[1][0]:
                o_x = 1
            else:
                o_x = 0

            if y > path[1][1]:
                o_y = -1
            elif y < path[1][1]:
                o_y = 1
            else:
                o_y = 0
        elif len(explored_current) == 4:
            # We've fully explored the directly surrounding tiles
            explored.add((x, y))

            if len(to_explore) == 0:
                # We're done
                raise FullyExplored(
                    {
                        'min_x': min_x,
                        'max_x': max_x,
                        'min_y': min_y,
                        'max_y': max_y,
                        'graph': g,
                        'origin': origin,
                        'oxygen_location': oxygen_location,
                        'grid': grid,
                    }
                )

            # Pick a new square to explore
            exploring = to_explore.pop()  # DFS as BFS would cause too much backtracking
            to_explore_set.remove(exploring)
            explored_current = set()

            # Add already explored squares, so we don't keep checking them
            for dx, dy in directions:
                if (exploring[0] + dx, exploring[1] + dy) in explored:
                    explored_current.add((exploring[0] + dx, exploring[1] + dy))


def paint_grid(grid_data, x_range, y_range):
    output = ''
    for y in reversed(y_range):  # Ahh, it's reflected upside down
        for x in x_range:
            if (x, y) in grid_data:
                if grid_data[(x, y)]:
                    output += grid_data[(x, y)]
                else:
                    output += '.'
            else:
                output += '.'
        output += '\n'
    return output


class Day15(puzzle.Puzzle):
    year = '2019'
    day = '15'

    def add_additional_args(self, parser):
        parser.add_argument('-d', '--draw', action='store_true')

    def get_data(self):
        orig_data = self.input_data
        data = defaultdict(lambda: 0)
        for i, x in enumerate([int(x) for x in orig_data.split(',')]):
            data[i] = x
        return data

    def run(self):
        grid_data = {}
        grid = grid_gen(grid_data, draw=self.args.draw)

        next_value = []
        grid.send(None)
        intcode.run_intcode_computer(
            self.get_data(),
            GridInputDevice(grid, next_value),
            GridOutputDevice(grid, next_value),
            label='part1',
        )

        return len(grid.send('get result'))

    def main(self):
        try:
            self.run()
        except FullyExplored as e:
            grid = e.payload['grid']
            min_x, max_x = e.payload['min_x'], e.payload['max_x']
            min_y, max_y = e.payload['min_y'], e.payload['max_y']
            graph = e.payload['graph']
            origin = e.payload['origin']
            oxygen_location = e.payload['oxygen_location']
            print(
                paint_grid(
                    grid, range(min_x - 2, max_x + 3), range(min_y - 2, max_y + 3)
                )
            )
            print(
                f'Part 1 Answer: {len(nx.shortest_path(graph, origin, oxygen_location)) - 1}'
            )
            r = nx.single_source_dijkstra_path_length(graph, oxygen_location)
            print(f'Part 2 Answer: {max(r.values())}')
