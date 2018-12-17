import sys


sys.setrecursionlimit(10000)


with open('input17.txt') as f:
    data = [x.strip('\n') for x in f.readlines()]


max_x = 0
min_x = 500
max_y = 0
min_y = 500


veins = []


for d in data:
    l, r = d.split(', ')
    if l.startswith('y='):
        y, x = l, r
    else:
        x, y = l, r
    y = y.lstrip('y=')
    x = x.lstrip('x=')
    if '..' in x:
        x0, x1 = x.split('..')
        x = list(range(int(x0), int(x1) + 1))
    else:
        x = [int(x)]
    if '..' in y:
        y0, y1 = y.split('..')
        y = list(range(int(y0), int(y1) + 1))
    else:
        y = [int(y)]
    veins.append([y, x])
    assert (len(x) == 1 or len(y) == 1)
    if max(x) > max_x:
        max_x = max(x)
    if min(x) < min_x:
        min_x = min(x)
    if max(y) > max_y:
        max_y = max(y)
    if min(y) < min_y:
        min_y = min(y)
    assert min_y <= max_y
    assert min_x <= max_x

assert min_y < max_y
assert min_x < max_x

max_x += 2


grid = []
for y in range(max_y + 1):
    l = []
    for x in range(max_x + 1):
        l.append('.')
    grid.append(l)

def print_grid(grid):
    for row in grid:
        print(''.join(row))

for vein in veins:
    if len(vein[0]) == 1:
        y = vein[0][0]
        for x in vein[1]:
            grid[y][x] = '#'
    else:
        assert len(vein[1]) == 1
        x = vein[1][0]
        for y in vein[0]:
            grid[y][x] = '#'

grid[0][500] = '+'

water_falling = [[1, 500]]
water_expanding = []
water_overflowing = []

class FallingWater:
    def __init__(self, y, x, grid, water_list, stopped_list, parent=None):
        self.y, self.x = y, x
        self.grid = grid
        self.stopped = False
        self.stopped_list = stopped_list
        self.water_list = water_list
        self.water_list.append(self)
        self.grid[self.y][self.x] = '|'
        self.parent = parent
        self.children = []
        if self.parent:
            self.parent.children.append(self)

    def stop(self, parents=False):
        self.stopped = True
        if self not in self.stopped_list:
            self.stopped_list.append(self)
        if parents and self.parent:
                self.parent.stop(parents=True)

    def unstop(self):
        self.stopped = False
        if self in self.stopped_list:
            self.stopped_list.remove(self)

    def update(self):
        try:
            below = self.grid[self.y + 1][self.x]
            left = self.grid[self.y][self.x - 1]
            right = self.grid[self.y][self.x + 1]
        except IndexError:
            self.grid[self.y][self.x] = '|'
            if self.parent:
                self.stop(parents=True)
            raise IndexError

        if self.stopped:
            if self not in self.stopped_list:
                self.stopped_list.append(self)
            if below == '~':
                if left == '#' and right == '|':
                    self.stop()
                    return
                if left == '|' and right == '#':
                    self.stop()
                    return
                if left == '#' and right == '#':
                    self.grid[self.y][self.x] = '~'
                    self.stop()
                    return
                self.unstop()

        if below == '|':
            return
        if below == '.':
            FallingWater(self.y + 1, self.x, grid, self.water_list, self.stopped_list, self)
            return
        if below == '#':
            # Look right until we find a wall or an edge
            if left == '|' and right == '|':
                return

            right_edge = False
            right_wall = False
            ey, ex = self.y, self.x
            while not right_wall and not right_edge:
                if self.grid[ey][ex + 1] == '#':
                    right_wall = True
                    break
                if self.grid[ey + 1][ex + 1] == '.' or self.grid[ey + 1][ex + 1] == '|':
                    right_edge = True
                    break
                ex += 1

            # Look left until we find a wall or an edge
            left_edge = False
            left_wall = False
            ey, ex = self.y, self.x
            while not left_wall and not left_edge:
                if self.grid[ey][ex - 1] == '#':
                    left_wall = True
                    break
                if self.grid[ey + 1][ex - 1] == '.' or self.grid[ey + 1][ex - 1] == '|':
                    left_edge = True
                    break
                ex -= 1

            if left_edge:
                FallingWater(self.y, self.x - 1, self.grid, self.water_list, self.stopped_list, self)
                assert right_edge == True

            if right_edge:
                FallingWater(self.y, self.x + 1, self.grid, self.water_list, self.stopped_list, self)
                assert left_edge == True

            if left_edge and right_edge:
                return

            # okay, need to start expanding

            # expand right
            if right != '|':
                ey, ex = self.y, self.x
                while self.grid[ey][ex] != '#':
                    self.grid[ey][ex] = '~'
                    ex += 1

            # expand left
            if left != '|':
                ey, ex = self.y, self.x
                while self.grid[ey][ex] != '#':
                    self.grid[ey][ex] = '~'
                    ex -= 1
            self.stop()
            return
        if below == '~':
            if left == '|' and right == '|':
                return

            # okay, need to start expanding, but check for overflow
            overflowing_right = False

            # expand right
            ey, ex = self.y, self.x + 1
            while self.grid[ey][ex] == '.' or self.grid[ey][ex] == '|' or self.grid[ey][ex] == '~':
                if self.grid[ey + 1][ex] == '.':
                    overflowing_right = True
                    break
                ex += 1

            # expand left
            overflowing_left = False
            ey, ex = self.y, self.x - 1
            while self.grid[ey][ex] == '.' or self.grid[ey][ex] == '|' or self.grid[ey][ex] == '~':
                if self.grid[ey + 1][ex] == '.':
                    overflowing_left = True
                    break
                ex -= 1

            self.grid[self.y][self.x] = '~'

            if overflowing_left:
                ey, ex = self.y, self.x - 1
                # expand left
                #while self.grid[ey][ex] == '~':
                while self.grid[ey + 1][ex] != '.':
                    self.grid[ey][ex] = '|'
                    if self.grid[ey + 1][ex] == '.':
                        FallingWater(ey, ex, self.grid, self.water_list, self.stopped_list, self)
                        break
                    if self.grid[ey + 1][ex] == '|':
                        break
                    ex -= 1
                FallingWater(ey, ex, self.grid, self.water_list, self.stopped_list, self)

                self.grid[self.y][self.x] = '|'
                if not overflowing_right:
                    ey, ex = self.y, self.x + 1
                    while self.grid[ey][ex] != '#':
                        self.grid[ey][ex] = '|'
                        ex += 1
                self.stop()
            if overflowing_right:
                ey, ex = self.y, self.x + 1
                # expand right
                # while self.grid[ey][ex] == '~':
                while self.grid[ey + 1][ex] != '.':
                    self.grid[ey][ex] = '|'
                    if self.grid[ey + 1][ex] == '.':
                        FallingWater(ey, ex, self.grid, self.water_list, self.stopped_list, self)
                        break
                    if self.grid[ey + 1][ex] == '|':
                        break
                    ex += 1
                FallingWater(ey, ex, self.grid, self.water_list, self.stopped_list, self)

                self.grid[self.y][self.x] = '|'
                if not overflowing_left:
                    ey, ex = self.y, self.x - 1
                    while self.grid[ey][ex] != '#':
                        self.grid[ey][ex] = '|'
                        ex -= 1
                self.stop()
            if not overflowing_right and not overflowing_left:
                # expand right
                ey, ex = self.y, self.x + 1
                while self.grid[ey][ex] != '#':
                    self.grid[ey][ex] = '~'
                    ex += 1

                # expand left
                ey, ex = self.y, self.x - 1
                while self.grid[ey][ex] != '#':
                    self.grid[ey][ex] = '~'
                    ex -= 1

                self.grid[self.y][self.x] = '~'

    def __repr__(self):
        return f'FallingWater({self.y}, {self.x}, stopped={self.stopped})'


def run_water2(grid):
    water_list = []
    stopped_list = []
    water = FallingWater(1, 500, grid, water_list, stopped_list)
    error_count = 0
    while len(stopped_list) != len(water_list):
        for water in water_list:
            try:
                water.update()
            except IndexError:
                error_count += 1
                if error_count > 20:
                    print(error_count)
                    raise


def count_water(grid, chars=('~', '|', '+')):
    count = 0
    for i, row in enumerate(grid):
        if i < min_y:
            continue
        for c in row:
            if c in chars:
                count += 1
    return count

def count_resting_water(grid):
    return count_water(grid, chars=('~',))

try:
    run_water2(grid)
except IndexError:
    pass
except KeyboardInterrupt:
    pass
#print_grid(grid)
print(f'Day 17 Part 1 Answer: {count_water(grid)}')
print(f'Day 17 Part 2 Answer: {count_resting_water(grid)}')
