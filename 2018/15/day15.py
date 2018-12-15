import sys

import networkx as nx


with open('input15.txt') as f:
    data = [x.strip('\n') for x in f.readlines()]


class GameEnded(Exception):
    pass


class Unit:
    attackpower = 3

    def __init__(self, y, x, grid, graph1, graph2, units, goblins, elfs):
        self.y, self.x = y, x
        self.hitpoints = 200
        self.dead = False
        self.units = units
        self.units[(y, x)] = self
        self.grid = grid
        self.graph1 = graph1
        self.graph = graph2
        self.goblins = goblins
        self.elfs = elfs

    def take_turn(self):
        if len(self.targets) == 0:
            raise GameEnded
        targets = self.move()
        self.attack(targets)

    def move(self):
        # Check for any adjacent targets
        adjacent_targets = []
        for ty, tx in self.targets:
            if ty == self.y:
                if tx in (self.x - 1, self.x + 1):
                    adjacent_targets.append((ty, tx))
            if tx == self.x:
                if ty in (self.y - 1, self.y + 1):
                    adjacent_targets.append((ty, tx))
        if adjacent_targets:
            return adjacent_targets

        self.graph = create_graph(self.grid)
        current = self.grid[self.y][self.x]
        for sq in [self.grid[self.y - 1][self.x], self.grid[self.y][self.x - 1], self.grid[self.y][self.x + 1], self.grid[self.y + 1][self.x]]:
            if type(sq) == Wall:
                continue
            if sq.occupied:
                continue
            self.graph.add_edge(current, sq)

        # Find in range squares of targets
        targets_in_range_coords = []
        for ty, tx in sorted(self.targets.keys()):
            sq = self.grid[ty][tx]
            assert type(sq) != Wall

            node = self.graph1[sq]
            targets_in_range_coords.extend([(p.y, p.x) for p in node])
        if not targets_in_range_coords:
            return

        paths = []
        for ty, tx in targets_in_range_coords:
            target_sq = self.grid[ty][tx]
            if target_sq.occupied:
                continue
            try:
                paths.append(nx.shortest_path(self.graph, self.grid[self.y][self.x], target_sq))
            except nx.exception.NetworkXNoPath:
                pass
            except nx.exception.NodeNotFound:
                pass

        # No paths available
        if not paths:
            return

        # Find shortest path
        min_length_path = paths[0]
        min_length_paths = []
        for path in paths:
            if len(path) == len(min_length_path):
                min_length_paths.append(path)
            if len(path) < len(min_length_path):
                min_length_paths = [path]
                min_length_path = path

        min_length_path = min_length_paths[0]
        if len(min_length_paths) > 1:
            for path in min_length_paths:
                if path[1] < min_length_path[1]:
                    min_length_path = path

        # Begin travelling along path
        new_y, new_x = min_length_path[1].y, min_length_path[1].x
        old_y, old_x = self.y, self.x

        # Update the grid
        self.grid[old_y][old_x].occupied = None
        self.grid[new_y][new_x].occupied = self.c

        # Update units
        self.units[(new_y, new_x)] = self.units[(old_y, old_x)]
        del self.units[(old_y, old_x)]
        self.allies[(new_y, new_x)] = self.allies[(old_y, old_x)]
        del self.allies[(old_y, old_x)]

        # Update unit
        self.y = new_y
        self.x = new_x

        # Check for any adjacent targets
        adjacent_targets = []
        for ty, tx in self.targets:
            if ty == self.y:
                if tx in (self.x - 1, self.x + 1):
                    adjacent_targets.append((ty, tx))
            if tx == self.x:
                if ty in (self.y - 1, self.y + 1):
                    adjacent_targets.append((ty, tx))
        return adjacent_targets

    @property
    def targets(self):
        return self.units

    @property
    def allies(self):
        return self.units

    def attack(self, targets):
        if targets:
            loop_targets = list(sorted(targets))
            min_hp_target = loop_targets[0]
            display_targets = [self.targets[x] for x in loop_targets]
            for target in loop_targets:
                if self.targets[target].hitpoints < self.targets[min_hp_target].hitpoints:
                    min_hp_target = target

            target = self.targets[min_hp_target]
            target.hitpoints -= self.attackpower
            if target.hitpoints <= 0:
                target.dead = True
                self.grid[min_hp_target[0]][min_hp_target[1]].occupied = None
                del self.targets[min_hp_target]
                del self.units[min_hp_target]

    def __repr__(self):
        return f'Unit({self.y}, {self.x})'


class Goblin(Unit):
    c = 'G'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.goblins[(self.y, self.x)] = self

    @property
    def targets(self):
        return self.elfs

    @property
    def allies(self):
        return self.goblins

    def __repr__(self):
        return f'Goblin({self.hitpoints}, {self.y}, {self.x})'


class Elf(Unit):
    c = 'E'
    attackpower = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elfs[(self.y, self.x)] = self

    @property
    def targets(self):
        return self.goblins

    @property
    def allies(self):
        return self.elfs

    def __repr__(self):
        return f'Elf({self.hitpoints}, {self.y}, {self.x})'


class Square:
    _char = ' '

    def __init__(self, y, x):
        self.y, self.x = y, x

    def draw(self):
        print(self._char, end='')

    def __repr__(self):
        return f'Square({self.x}, {self.y})'

    def __lt__(self, other):
        if self.y < other.y:
            return True
        if self.y == other.y and self.x < other.x:
            return True
        return False


class Wall(Square):
    _char = '#'

    def __repr__(self):
        return f'Wall({self.x}, {self.y})'


class Space(Square):
    _char = '.'

    def __init__(self, y, x, occupied=None):
        super().__init__(y, x)
        self.occupied = occupied

    def draw(self):
        if self.occupied:
            print(self.occupied, end='')
        else:
            super().draw()

    def __repr__(self):
        if self.occupied:
            return f'Space({self.x}, {self.y}, {self.occupied})'
        return f'Space({self.x}, {self.y})'



def create_grid(data):
    grid = []
    for y, row in enumerate(data):
        grid.append([])
        for x, c in enumerate(row):
            if c == '#':
                grid[y].append(Wall(y, x))
            elif c == '.':
                grid[y].append(Space(y, x))
            else:
                grid[y].append(Space(y, x, c))
    return grid


def create_graph1(grid):
    grid_graph = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if type(grid[y][x]) == Wall:
                continue
            adjacent_coords = [
                (y - 1, x),
                (y, x - 1),
                (y, x + 1),
                (y + 1, x),
            ]
            grid_graph[c] = []
            for y1, x1 in adjacent_coords:
                if y1 < 0 or x1 < 0:
                    continue
                if y1 >= len(grid) or x1 >= len(grid[y1]):
                    continue
                if type(grid[y1][x1]) == Wall:
                    continue
                grid_graph[c].append(grid[y1][x1])
    return grid_graph


def create_graph(grid):
    grid_graph2 = nx.Graph()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if type(grid[y][x]) == Wall:
                continue
            adjacent_coords = [
                (y - 1, x),
                (y, x - 1),
                (y, x + 1),
                (y + 1, x),
            ]
            for y1, x1 in adjacent_coords:
                if y1 < 0 or x1 < 0:
                    continue
                if y1 >= len(grid) or x1 >= len(grid[y1]):
                    continue
                if type(grid[y1][x1]) == Wall:
                    continue
                if grid[y1][x1].occupied or grid[y][x].occupied:
                    continue
                grid_graph2.add_edge(grid[y][x], grid[y1][x1])
    return grid_graph2


def draw_grid(grid):
    for row in grid:
        for c in row:
            c.draw()
        print()


def create_units(grid, graph1, graph2):
    units = {}
    goblins = {}
    elfs = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if type(c) == Wall:
                continue
            if c.occupied == 'G':
                Goblin(y, x, grid, graph1, graph2, units, goblins, elfs)
            if c.occupied == 'E':
                Elf(y, x, grid, graph1, graph2, units, goblins, elfs)
    return units, goblins, elfs


def run_game(grid, units, goblins, elfs):
    rounds = 0
    while True:
        rounds += 1
        try:
            for unit_coord in list(sorted(list((units.keys())))):
                if unit_coord in units:  # Might have died
                    unit = units[unit_coord]
                    unit.take_turn()
            if sys.argv[-1] == '-d':
                print([units[x] for x in sorted(list(units.keys()))])
                draw_grid(grid)
            if len(goblins) <= 0:
                return rounds, 'elfs'
            if len(elfs) <= 0:
                return rounds, 'goblins'
        except GameEnded:
            rounds -= 1
            if len(elfs) == 0:
                return rounds, 'goblins'
            if len(goblins) == 0:
                return rounds, 'elfs'
            break
    return rounds


grid = create_grid(data)
grid_graph = create_graph1(grid)
grid_graph2 = create_graph(grid)

units, goblins, elfs = create_units(grid, grid_graph, grid_graph2)

if sys.argv[-1] == '-d':
    draw_grid(grid)

starting_elfs = len(elfs)

rounds, winner = run_game(grid, units, goblins, elfs)
if winner == 'elfs':
    winner = elfs
elif winner == 'goblins':
    winner = goblins
else:
    assert False
print(f'rounds: {rounds}')
hitpoints_left = 0
for unit_idx in winner:
    unit = winner[unit_idx]
    hitpoints_left += unit.hitpoints

print(f'Elfs left: {len(elfs)} / {starting_elfs}')
print(f'hitpoints left: {hitpoints_left}')
print(f'Day 15 Part 1 Answer: {rounds * hitpoints_left}')

# Guess that it is under 50
winner = None
guess_max = 50
guess_min = 4
guess = guess_min
while True:
    old_guess = guess
    print(guess_min, guess_max)
    guess = guess_min + ((guess_max - guess_min) // 2)
    if guess == old_guess:
        print('guess not changing')
        break

    Elf.attackpower = guess
    print(f'Guess {guess}')

    with open('input15.txt') as f:
        data = [x.strip('\n') for x in f.readlines()]

    grid = create_grid(data)
    grid_graph = create_graph1(grid)
    grid_graph2 = create_graph(grid)

    units, goblins, elfs = create_units(grid, grid_graph, grid_graph2)
    for elf_idx in elfs:
        assert elfs[elf_idx].attackpower == guess
    for goblin_idx in goblins:
        assert goblins[goblin_idx].attackpower == 3

    rounds, winner = run_game(grid, units, goblins, elfs)
    if winner == 'goblins':
        winner = goblins
        print('goblins win')
        guess_min = guess
    elif winner == 'elfs':
        winner = elfs
        print('elfs win')
        if starting_elfs == len(elfs):
            guess_max = guess + 1
        else:
            guess_min = guess
    else:
        print('Looks like it\'s a tie')
        assert False
    if guess_max == guess_min:
        break

if not winner:
    print('No winner')
else:
    hitpoints_left = 0
    for unit_idx in winner:
        unit = winner[unit_idx]
        hitpoints_left += unit.hitpoints

    print(f'Elfs left: {len(elfs)} / {starting_elfs}')
    print(f'Elf attack power level: {Elf.attackpower}')
    print(f'Day 15 Part 2 Answer: {rounds} x {hitpoints_left} = {rounds * hitpoints_left}')
