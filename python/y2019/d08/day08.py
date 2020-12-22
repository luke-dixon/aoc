from collections import Counter
from collections.abc import Sequence
from math import inf

from lib import puzzle


def format_layer(layer, width=25, height=6):
    s = ''
    for i in range(height):
        for j in range(width):
            s += layer[i * width + j]
        s += '\n'
    return s


class layers(Sequence):
    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height
        self.layer_length = width * height

    def __len__(self):
        return len(self.data) // self.layer_length

    def __getitem__(self, item):
        if isinstance(item, int):
            if item >= len(self):
                raise IndexError
            return self.data[
                item * self.layer_length : (item * self.layer_length)
                + self.layer_length
            ]
        else:
            raise NotImplementedError(
                f'Indexing by {type(item)} has not been implemented'
            )


class Day08(puzzle.Puzzle):
    year = '2019'
    day = '8'

    width = 25
    height = 6

    def get_data(self):
        return str(self.input_data.splitlines()[0].strip())

    def part1(self):
        min_zeroes, min_zeroes_layer = inf, 0
        for i, layer in enumerate(layers(self.get_data(), self.width, self.height)):
            c = Counter(layer)
            if c['0'] < min_zeroes:
                min_zeroes, min_zeroes_layer = c['0'], i

        c = Counter(layers(self.get_data(), self.width, self.height)[min_zeroes_layer])
        return c['1'] * c['2']

    def part2(self):
        final_layer = [' '] * self.width * self.height

        for layer in reversed(layers(self.get_data(), self.width, self.height)):
            for i, x in enumerate(layer):
                if x != '2':
                    final_layer[i] = x if x == '1' else ' '

        return '\n' + format_layer(final_layer, self.width, self.height)

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
