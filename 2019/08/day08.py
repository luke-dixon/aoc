from collections import Counter
from collections.abc import Sequence
from math import inf

from aocd.models import Puzzle


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


class Day8(Puzzle):
    def __init__(self):
        super().__init__(year=2019, day=8)
        self.data = str(self.input_data.splitlines()[0].strip())
        self.width = 25
        self.height = 6

    def part1(self):
        min_zeroes, min_zeroes_layer = inf, 0
        for i, layer in enumerate(layers(self.data, self.width, self.height)):
            c = Counter(layer)
            if c['0'] < min_zeroes:
                min_zeroes, min_zeroes_layer = c['0'], i

        c = Counter(layers(self.data, self.width, self.height)[min_zeroes_layer])
        return c['1'] * c['2']

    def part2(self):
        final_layer = [' '] * self.width * self.height

        for layer in reversed(layers(self.data, self.width, self.height)):
            for i, x in enumerate(layer):
                if x != '2':
                    final_layer[i] = x if x == '1' else ' '

        return '\n' + format_layer(final_layer, self.width, self.height)


def main():
    puzzle = Day8()

    print(f'Part 1 Answer: {puzzle.part1()}')
    print(f'Part 2 Answer: {puzzle.part2()}')
