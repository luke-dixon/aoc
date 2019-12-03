from collections import namedtuple


def taxicab_distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


Payload = namedtuple('Payload', ['origin', 'distance_by_wire'])


class Grid:
    _directions = {
        'U': (0, 1),
        'D': (0, -1),
        'L': (-1, 0),
        'R': (1, 0),
    }

    def __init__(self, origin=(0, 0)):
        self.origin = origin = (0, 0)
        self.__grid = {
            self.origin: Payload(origin=True, distance_by_wire={})
        }
        self.__wires = set()
        self.__intersections = set()

    def _add_direction(self, direction, position):
        return position[0] + self._directions[direction][0], position[1] + self._directions[direction][1]

    def get_intersections(self):
        for position in self.__intersections:
            yield *position, self.__grid[position]

    def add_wire(self, wire_idx, wire):
        self.__wires.add(wire_idx)
        position = self.origin
        distance = 0
        for path in wire.split(','):
            direction, length = path[0], int(path[1:])
            for _ in range(length):
                position = self._add_direction(direction, position)
                distance += 1
                if position not in self.__grid:
                    self.__grid[position] = Payload(
                        origin=False, distance_by_wire={wire_idx: distance})
                elif self.__grid[position].origin:
                    self.__grid[position].distance_by_wire[wire_idx] = 0
                else:
                    if all([
                        len(self.__grid[position].distance_by_wire.keys()) + 1 == len(self.__wires),
                        wire_idx not in self.__grid[position].distance_by_wire,
                    ]):
                        self.__intersections.add(position)
                    self.__grid[position].distance_by_wire[wire_idx] = distance

    @classmethod
    def from_data(cls, data):
        grid = cls()

        for wire_idx, wire in enumerate(data):
            grid.add_wire(wire_idx, wire)

        return grid


def part1(grid):
    distances = []
    for y, x, _ in grid.get_intersections():
        distances.append(taxicab_distance(grid.origin, (x, y)))
    return min(distances)


def part2(grid):
    distances = []
    for y, x, payload in grid.get_intersections():
        distances.append(sum(payload.distance_by_wire.values()))
    return min(distances)


def main():
    with open('input3.txt') as f:
        data = f.read().strip().splitlines()

    grid = Grid.from_data(data)

    print(f'Answer part 1: {part1(grid)}')
    print(f'Answer part 2: {part2(grid)}')


if __name__ == "__main__":
    main()
