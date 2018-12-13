from enum import Enum


class CrashDetected(Exception):
    def __init__(self, y, x, carts):
        super().__init__()
        self.y, self.x = y, x
        self.carts = carts


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


cart_directions = {
    '^': Direction.UP,
    '<': Direction.LEFT,
    'v': Direction.DOWN,
    '>': Direction.RIGHT,
}


static_choices = {
    '/': {
        Direction.UP: Direction.RIGHT,
        Direction.LEFT: Direction.DOWN,
        Direction.DOWN: Direction.LEFT,
        Direction.RIGHT: Direction.UP,
    },
    '\\': {
        Direction.UP: Direction.LEFT,
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.RIGHT,
        Direction.LEFT: Direction.UP,
    },
}

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

turn_plus = {
    0: turn_left,
    1: turn_straight,
    2: turn_right,
}


class Cart:
    def __init__(self, y, x, direction, carts_locations):
        self.direction = direction
        self.points_choice = 0
        self.y, self.x = y, x
        self.carts_locations = carts_locations
        self.set_pos(y, x)

        self.update_choice_table = {
            '<^v>-|': self.update_straight,
            ''.join(static_choices.keys()): self.update_turn,
            '+': self.update_plus,
        }

    def set_pos(self, y, x):
        if (self.y, self.x) in self.carts_locations:
            del self.carts_locations[(self.y, self.x)]
        self.y, self.x = y, x
        if (y, x) in self.carts_locations:
            raise CrashDetected(y, x, [self.carts_locations[(self.y, self.x)], self])
        self.carts_locations[(y, x)] = self

    def update_straight(self, current_square):
        y = self.y + self.direction.value[0]
        x = self.x + self.direction.value[1]
        self.set_pos(y, x)

    def update_turn(self, current_square):
        self.direction = static_choices[current_square][self.direction]
        y = self.y + self.direction.value[0]
        x = self.x + self.direction.value[1]
        self.set_pos(y, x)

    def update_plus(self, current_square):
        self.direction = turn_plus[self.points_choice % 3][self.direction]
        y = self.y + self.direction.value[0]
        x = self.x + self.direction.value[1]
        self.set_pos(y, x)
        self.points_choice = (self.points_choice + 1) % 3

    def update(self, grid):
        current_square = grid[self.y][self.x]
        for update_choice in self.update_choice_table:
            if current_square in update_choice:
                self.update_choice_table[update_choice](current_square)
                return

    def __repr__(self):
        return f'Cart({self.x}, {self.y}, {self.direction}, {self.points_choice})'



with open('input13.txt') as f:
    data = [x.strip('\n') for x in f.readlines()]


carts = []
carts_locations = {}
for y, row in enumerate(data):
    for x, c in enumerate(row):
        if c in cart_directions:
            carts.append(Cart(y, x, cart_directions[c], carts_locations))

tick = 1

try:
    while True:
        for carts_location in list(sorted(carts_locations)):
            carts_locations[carts_location].update(data)
        tick += 1

except CrashDetected as e:
    print(f'Day 13 Part 1 Answer: {e.x},{e.y}')

tick = 1


carts = []
carts_locations = {}
for y, row in enumerate(data):
    for x, c in enumerate(row):
        if c in cart_directions:
            carts.append(Cart(y, x, cart_directions[c], carts_locations))



while len(carts_locations) > 1:
    for carts_location in list(sorted(carts_locations)):
        if carts_location not in carts_locations:
            continue
        try:
            carts_locations[carts_location].update(data)
        except CrashDetected as e:
            print(f'Crash detected ({e.x}, {e.y}), carts: {e.carts}')
            del carts_locations[(e.y, e.x)]

    tick += 1

print('Remaining carts:')
for carts_location in carts_locations:
    print(f'Day 13 Part 2 Answer: {carts_locations[carts_location].x},{carts_locations[carts_location].y}')
