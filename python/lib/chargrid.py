from typing import Iterator, List

Grid = List[List[str]]


def print_grid(grid: Grid) -> None:
    for line in grid:
        print(''.join(line))


def rotate_left(grid: Grid) -> Grid:
    new_grid = []
    for y, row in enumerate(grid):
        new_grid.append([grid[x][len(grid) - y - 1] for x, c in enumerate(row)])

    return new_grid


def rotate_right(grid: Grid) -> Grid:
    new_grid = []
    for y, row in enumerate(grid):
        new_grid.append([grid[len(grid[0]) - x - 1][y] for x, c in enumerate(row)])

    return new_grid


def flip_vertical(grid: Grid) -> Grid:
    return list(reversed(grid))


def flip_horizontal(grid: Grid) -> Grid:
    return [list(reversed(line)) for line in grid]


def symmetries(grid: Grid) -> Iterator[Grid]:
    rotations = 0
    flips = 0
    while flips <= 1:
        yield grid
        rotations += 1
        if rotations >= 4:
            grid = flip_vertical(grid)
            flips += 1
            rotations = 0
            continue
        grid = rotate_left(grid)
