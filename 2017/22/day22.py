import sys
from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


turn_left = {
    Direction.UP: Direction.LEFT,
    Direction.LEFT: Direction.DOWN,
    Direction.DOWN: Direction.RIGHT,
    Direction.RIGHT: Direction.UP,
}
turn_right = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}
turn_straight = {
    Direction.UP: Direction.UP,
    Direction.LEFT: Direction.LEFT,
    Direction.RIGHT: Direction.RIGHT,
    Direction.DOWN: Direction.DOWN,
}
turn_around = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


class Carrier:
    def __init__(self, y=0, x=0):
        self.y = y
        self.x = x
        self.direction = Direction.UP
        self.bursts = 0
        self.infected_bursts = 0
        self.cell_state = {
            '.': ('#', turn_left),
            '#': ('.', turn_right),
        }

    def __repr__(self):
        return f'Carrier({self.x}, {self.y}, {self.direction})'

    def move(self, grid):
        next_cell_state, turn = self.cell_state[chr(grid[self.y][self.x])]

        self.direction = turn[self.direction]
        grid[self.y][self.x] = ord(next_cell_state)
        self.bursts += 1
        if chr(grid[self.y][self.x]) == '#':
            self.infected_bursts += 1

        self.y += self.direction.value[0]
        self.x += self.direction.value[1]

        if self.y >= len(grid):
            grid.append(bytearray(('.' * len(grid[0])).encode('utf8')))
        assert self.y < len(grid)
        if self.y <= 0:
            grid.insert(0, bytearray(('.' * len(grid[0])).encode('utf8')))
            self.y += 1
        assert self.y >= 0
        if self.x >= len(grid[0]):
            for d in grid:
                d.append(ord('.'))
                assert len(d) > self.x
        assert self.x < len(grid[0])
        if self.x <= 0:
            for d in grid:
                d.insert(0, ord('.'))
            self.x += 1
        assert self.x >= 0


def print_grid(grid, carrier):
    for j, row in enumerate(grid):
        if j == carrier.y:
            if carrier.x != 0:
                print(' ', end='')
            print(' '.join(row.decode('utf8')[:carrier.x]), end='')
            print('[', end='')
            print(row.decode('utf8')[carrier.x], end='')
            print(']', end='')
            print(' '.join(row.decode('utf8')[carrier.x + 1:]))
        else:
            print(' ', end='')
            print(' '.join(row.decode('utf8')))


with open('input22.txt') as f:
    data = f.readlines()

grid = [bytearray(x.strip('\n'), 'utf8') for x in data]

carrier = Carrier(y=len(grid) // 2, x=len(grid[0]) // 2)
if sys.argv[-1] == '-p':
    print_grid(grid, carrier)
    print(carrier)

i = 0
while i < 10000:
    carrier.move(grid)
    i += 1

if sys.argv[-1] == '-p':
    print_grid(grid, carrier)
    print(carrier)

print(f'Day 19 Part 1 Answer: {carrier.infected_bursts} / {carrier.bursts}')


# Start over with fresh data
with open('input22.txt') as f:
    data = f.readlines()

grid2 = [bytearray(x.strip('\n'), 'utf8') for x in data]

carrier2 = Carrier(y=len(grid2) // 2, x=len(grid2[0]) // 2)
carrier2.cell_state = {
    '.': ('W', turn_left),
    'W': ('#', turn_straight),
    '#': ('F', turn_right),
    'F': ('.', turn_around),
}

i = 0
while i < 10000000:
    carrier2.move(grid2)
    i += 1

if sys.argv[-1] == '-p':
    print_grid(grid2, carrier2)
    print(carrier2)

print(f'Day 19 Part 2 Answer: {carrier2.infected_bursts} / {carrier2.bursts}')
