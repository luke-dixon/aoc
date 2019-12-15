from collections import defaultdict, deque

import networkx as nx
from aocd.models import Puzzle

from . import intcode


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


def grid_gen(grid):
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    x, y = 0, 0
    o_x, o_y = 0, 1

    direction_to_code = {
        (0, 1): 1,
        (0, -1): 2,
        (-1, 0): 3,
        (1, 0): 4,
    }
    grid[(x, y)] = 'D'

    g = nx.Graph()

    to_explore_set = {(0, 0)}
    to_explore = deque([(0, 0)])

    exploring = to_explore.pop()
    to_explore_set.remove(exploring)
    explored_current = {}
    explored = {}

    oxygen_location = None

    yield 'started'
    while True:
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)

        status = yield direction_to_code[(o_x, o_y)]

        origin = (0, 0)

        if status == 0:
            # hit wall
            grid[(x + o_x, y + o_y)] = '#'
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
            if (x + 1, y + 0) not in explored_current:
                o_x, o_y = 1, 0
            elif (x - 1, y + 0) not in explored_current:
                o_x, o_y = -1, 0
            elif (x + 0, y + 1) not in explored_current:
                o_x, o_y = 0, 1
            elif (x + 0, y - 1) not in explored_current:
                o_x, o_y = 0, -1
            explored_current[(x + o_x, y + o_y)] = True
            continue
        elif (x, y) != exploring:
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
            explored[(x, y)] = True

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
            explored_current = {}


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


class Day15(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=15)

    def get_data(self):
        orig_data = self.input_data
        # orig_data = '3,8,1005,8,339,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,29,2,1108,11,10,1,1,20,10,2,107,6,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,62,1006,0,29,1006,0,12,1,1101,5,10,1,2,20,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,99,1006,0,30,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,124,1006,0,60,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,149,2,1007,2,10,1,1105,10,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,178,1,1108,15,10,1,1101,5,10,1,109,8,10,1006,0,20,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,215,1006,0,61,1006,0,16,2,1105,15,10,1006,0,50,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,250,1,1003,10,10,1,9,19,10,2,1004,6,10,2,1106,2,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,289,1,1103,13,10,2,105,17,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,318,101,1,9,9,1007,9,1086,10,1005,10,15,99,109,661,104,0,104,1,21101,0,825599304340,1,21101,356,0,0,1106,0,460,21101,0,937108545948,1,21102,1,367,0,1106,0,460,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,21628980315,1,21101,0,414,0,1105,1,460,21101,0,3316673539,1,21101,425,0,0,1106,0,460,3,10,104,0,104,0,3,10,104,0,104,0,21102,988753428840,1,1,21102,1,448,0,1106,0,460,21102,825544569700,1,1,21102,459,1,0,1106,0,460,99,109,2,21202,-1,1,1,21102,1,40,2,21102,491,1,3,21102,481,1,0,1105,1,524,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,486,487,502,4,0,1001,486,1,486,108,4,486,10,1006,10,518,1101,0,0,486,109,-2,2105,1,0,0,109,4,2102,1,-1,523,1207,-3,0,10,1006,10,541,21102,0,1,-3,21201,-3,0,1,22102,1,-2,2,21102,1,1,3,21102,560,1,0,1106,0,565,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,588,2207,-4,-2,10,1006,10,588,22101,0,-4,-4,1105,1,656,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21102,1,607,0,1106,0,565,22102,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,626,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,648,21202,-1,1,1,21101,0,648,0,105,1,523,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0'
        data = defaultdict(lambda: 0)
        for i, x in enumerate([int(x) for x in orig_data.split(',')]):
            data[i] = x
        return data

    def run(self):
        grid_data = {}
        grid = grid_gen(grid_data)

        next_value = []
        grid.send(None)
        intcode.run_intcode_computer(
            self.get_data(),
            GridInputDevice(grid, next_value),
            GridOutputDevice(grid, next_value),
            label='part1',
        )

        return len(grid.send('get result'))


def main():
    try:
        Day15().run()
    except FullyExplored as e:
        grid = e.payload['grid']
        min_x, max_x = e.payload['min_x'], e.payload['max_x']
        min_y, max_y = e.payload['min_y'], e.payload['max_y']
        graph = e.payload['graph']
        origin = e.payload['origin']
        oxygen_location = e.payload['oxygen_location']
        print(
            paint_grid(grid, range(min_x - 2, max_x + 3), range(min_y - 2, max_y + 3))
        )
        print(
            f'Part 1 Answer: {len(nx.shortest_path(graph, origin, oxygen_location)) - 1}'
        )
        r = nx.single_source_dijkstra_path_length(graph, oxygen_location)
        print(f'Part 2 Answer: {max(r.values())}')


if __name__ == '__main__':
    main()
