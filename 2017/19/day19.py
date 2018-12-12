from collections import namedtuple
from enum import Enum
import time
import sys


letters = [chr(x) for x in range(ord('A'), ord('Z') + 1)]


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


opposite_direction = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


class Packet:
    def __init__(self, y=0, x=0, direction=Direction.DOWN, letters=None):
        self.x = x
        self.y = y
        self.direction = direction
        self.letters = letters or []

    def __repr__(self):
        letters = ''.join(self.letters)
        return f'Packet({self.y}, {self.x}, {self.direction}, letters={letters})'


def print_location(grid, current):
    directions = {
        Direction.UP: '^',
        Direction.DOWN: 'v',
        Direction.LEFT: '<',
        Direction.RIGHT: '>',
    }
    for y in range(max(0, current.y - 10), min(len(grid), current.y + 10)):
        if y == current.y:
            print(grid[y][max(0, current.x - 10):current.x], end='')
            print(directions[current.direction], end='')
            print(grid[y][current.x + 1:min(len(grid), current.x + 10)])
        else:
            print(grid[y][max(0, current.x - 10):min(len(grid), current.x + 10)])
    print(current)


def find_start(grid):
    return (0, grid[0].index('|'))


def find_next(grid, current, previous, graph):
    options = set()
    current_square = grid[current.y][current.x]
    previous_square = ' '
    if previous:
        previous_square = grid[previous.y][previous.x]

    if current_square in '|-' and current.direction in (Direction.UP, Direction.DOWN):
        # our only options are up or down
        options.add(Direction.UP)
        options.add(Direction.DOWN)
    elif current_square in '|-' and current.direction in (Direction.LEFT, Direction.RIGHT):
        # our only options are left or right
        options.add(Direction.LEFT)
        options.add(Direction.RIGHT)
    elif current_square in letters:
        options.add(current.direction)

    # Remove any options that take us out of bounds
    for option in list(options):
        if -1 in (option.value[0] + current.y, option.value[1] + current.x):
            options.remove(option)

    # Remove any options that are off the track
    for option in list(options):
        if grid[option.value[0] + current.y][option.value[1] + current.x] == ' ':
            options.remove(option)

    # Only one choice
    if len(options) == 1:
        option = options.pop() 
        packet = Packet(option.value[0] + current.y, option.value[1] + current.x, option, current.letters)
        return packet

    # Remove the previous option
    for option in list(options):
        if current.y + option.value[0] == previous.y:
            if current.x + option.value[1] == previous.x:
                options.remove(option)

    # Only one choice
    if len(options) == 1:
        option = options.pop() 
        packet = Packet(option.value[0] + current.y, option.value[1] + current.x, option, current.letters)
        return packet

    assert len(options) == 0
    # Deal with choices
    if current_square == '+':
        options = {Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT}

        # Remove the previous, no point in going straight back
        options.remove(opposite_direction[previous.direction])

        # Check each direction to see if it is an option

        # Can we go left
        if Direction.UP in options and grid[current.y - 1][current.x] != '|':
            options.remove(Direction.UP)
        if Direction.DOWN in options and grid[current.y + 1][current.x] != '|':
            options.remove(Direction.DOWN)
        if Direction.LEFT in options and grid[current.y][current.x - 1] != '-':
            options.remove(Direction.LEFT)
        if Direction.RIGHT in options and grid[current.y][current.x + 1] != '-':
            options.remove(Direction.RIGHT)

    # Only one choice
    if len(options) == 1:
        option = options.pop() 
        packet = Packet(option.value[0] + current.y, option.value[1] + current.x, option, current.letters)
        return packet

    # Okay, there really are no other options
    return current


with open('input19.txt') as f:
    grid = [x.strip('\n') for x in f.readlines()]


# assume the grid is square
assert len(grid) == len(grid[0])


packet = Packet()
packet.y, packet.x = find_start(grid)

done = False
prev = None

decisions = {}
print_location(grid, packet)
steps = 1

draw = False
if sys.argv[-1] == '-d':
    draw = True
draw_delay = 0.08

while packet != prev:
    current = Packet(packet.y, packet.x, packet.direction, packet.letters)
    next_packet = find_next(grid, current, prev, decisions)
    prev = current
    packet = next_packet
    if grid[packet.y][packet.x] in letters and packet != prev:
        packet.letters.append(grid[packet.y][packet.x])
    if packet != prev:
        steps += 1
    if draw:
        print_location(grid, packet)
        if current.direction in [Direction.LEFT, Direction.RIGHT]:
            time.sleep(0.6 * draw_delay)
        else:
            time.sleep(draw_delay)

print_location(grid, packet)
print('Day 19 Part 1 Answer: ', ''.join(packet.letters))
print(f'Day 19 Part 1 Answer: {steps}')
