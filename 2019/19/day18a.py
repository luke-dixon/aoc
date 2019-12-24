import math
import random
from collections import defaultdict, deque
from functools import lru_cache

import networkx as nx

from .. import puzzle, intcode


def draw_grid(grid):
    min_y, max_y = 0, 0
    min_x, max_x = 0, 0

    for y, x in grid:
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x

    y_range = range(min_y, max_y + 2)
    x_range = range(min_x, max_x + 2)

    output = ''
    for y in y_range:
        for x in x_range:
            if (y, x) in grid:
                output += grid[(y, x)]
            else:
                output += '#'
        output += '\n'
    return output


def construct_graph(grid, position, keys):
    g = nx.Graph()

    l = deque([position])
    visited = set()

    movable = {'.', '@', *[chr(x) for x in range(ord('a'), ord('z') + 1)]}

    possible_keys = []

    while len(l) > 0:
        n = l.popleft()
        visited.add(n)
        if n in grid and grid[n] in keys:
            possible_keys.append(n)

        for y, x in [(n[0] + 1, n[1]), (n[0] - 1, n[1]), (n[0], n[1] + 1), (n[0], n[1] - 1)]:
            if (y, x) in grid and grid[(y, x)] in movable:
                g.add_edge(n, (y, x))
                if (y, x) not in visited:
                    l.append((y, x))

    return g, possible_keys


def new_state_path_length(t):
    return len(t[-1])


class Day18(puzzle.Puzzle):
    year = '2019'
    day = '18'

    def get_data(self):
        data = self.input_data
        return data

    def part1(self):
        data = self.get_data()

        g = nx.Graph()

        keys = {}
        pos_to_key = {}
        doors = {}
        position = (0, 0)
        grid = {}
        for y, row in enumerate(data.splitlines()):
            for x, c in enumerate(row):
                if c == '#':
                    continue
                if c == '.':
                    grid[(y, x)] = '.'
                    continue
                if c == '@':
                    position = (y, x)
                    grid[(y, x)] = c
                if ord(c) in set(range(ord('a'), ord('z') + 1)):
                    keys[c] = (y, x)
                    pos_to_key[(y, x)] = c
                    grid[(y, x)] = c
                if ord(c) in set(range(ord('A'), ord('Z') + 1)):
                    doors[c] = (y, x)
                    grid[(y, x)] = c

        paths = []

        state = deque([(dict(grid), position, set(), [position])])

        shortest_path = 5423
        b_next = True
        counted = 0
        discarded = 0
        discarded2 = 0
        reached_end = 0
        reached_end2 = 0

        count = 0
        while len(state) > 0:
            count += 1
            if count % 100 == 0:
                print(f'{count}, states: {len(state)}, shortest path: {shortest_path}, discarded: {discarded}, discarded2: {discarded2}, reached end: {reached_end}, reached end2: {reached_end2}')
                b_next = True
            if b_next == True:
                current_grid, position, keys_collected, path = state.popleft()
                #print(f'b_next, {len(paths)}')
            else:
                current_grid, position, keys_collected, path = state.pop()

            #print(f'At position {position}, keys collected {keys_collected}')
            #print(draw_grid(current_grid))

            #print(len(keys_collected), len(keys))

            if len(path) >= shortest_path:
                b_next = True
                discarded += 1
                continue

            if len(keys_collected) == len(keys):
                reached_end2 += 1
                if len(path) < shortest_path:
                    shortest_path = len(path)
                    print(f'new shortest path {shortest_path}, paths: {len(paths)}, discarded: {discarded}')
                    #b_next = True
                continue

            graph, possible_keys = construct_graph(current_grid, position, keys)

            #print(f'possible keys: {possible_keys}, collected: {keys_collected}')

            b_next = False

            new_states = []
            for key_pos in possible_keys:
                #print(f'Adding path to {key_pos}')
                path_to_key = nx.shortest_path(graph, position, key_pos)[1:]
                new_path = path + path_to_key

                if len(new_path) >= shortest_path:
                    #b_next = True
                    discarded += 1
                    continue

                if (len(new_path) / (len(keys_collected) + 1)) >= (shortest_path / len(pos_to_key)):
                    #b_next = True
                    discarded2 += 1
                    continue

                new_position = key_pos

                new_keys_collected = set(keys_collected)
                new_keys_collected.add(current_grid[key_pos])
                #print(f'new keys collected {new_keys_collected}')

                key = current_grid[key_pos]
                new_grid = dict(current_grid)
                new_grid[position] = '.'
                if key.upper() in doors:
                    new_grid[doors[pos_to_key[key_pos].upper()]] = '.'
                new_grid[key_pos] = '@'

                new_states.append((
                    new_grid,
                    new_position,
                    new_keys_collected,
                    new_path,
                ))

            #for new_state in sorted(new_states, key=new_state_path_length):
            for new_state in random.sample(new_states, len(new_states)):
                state.append(new_state)

            if len(new_states) == 0:
                reached_end += 1
                b_next = True

        print(draw_grid(grid))

        print(paths)
        print(len(paths))
        lengths = []
        for path in paths:
            print(len(path) - 1)
            lengths.append(len(path) - 1)

        return min(lengths)

    def part2(self):
        return None

    def main(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
