from collections import Counter


def create_new_grid(old_grid, surrounding_acres):
    grid = []
    for y, row in enumerate(old_grid):
        l = []
        for x, current_acre in enumerate(row):
            counter = Counter()
            for ay, ax in surrounding_acres[(y, x)]:
                adjacent_acre = old_grid[ay][ax]
                counter.update(adjacent_acre)
            if current_acre == '.':
                if counter['|'] >= 3:
                    l.append('|')
                else:
                    l.append('.')
            elif current_acre == '|':
                if counter['#'] >= 3:
                    l.append('#')
                else:
                    l.append('|')
            elif current_acre == '#':
                if counter['#'] >= 1 and counter['|'] >= 1:
                    l.append('#')
                else:
                    l.append('.')
        grid.append(''.join(l))
    return grid


def get_resource_area(grid):
    counter = Counter()
    for row in grid:
        counter.update(row)
    return counter['|'] * counter['#']


def main():
    with open('input18.txt') as f:
        grid = f.read().splitlines()

    surrounding_acres = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            surrounding_acres[(y, x)] = []
            for y0 in range(max(0, y - 1), min(len(grid), y + 2)):
                for x0 in range(max(0, x - 1), min(len(grid[x]), x + 2)):
                    assert grid[y0]
                    assert grid[y0][x0]
                    if (y0, x0) == (y, x):
                        continue
                    surrounding_acres[(y, x)].append((y0, x0))

    minutes = 0
    areas = [get_resource_area(grid)]

    for i in range(1, 11):
        minutes += 1
        grid = create_new_grid(grid, surrounding_acres)
        areas.append(get_resource_area(grid))

    predictions_in_a_row = 0
    predict_next_index = -1
    pattern_start_index = -1

    while predictions_in_a_row < 100:
        minutes += 1
        grid = create_new_grid(grid, surrounding_acres)
        new_area = get_resource_area(grid)

        if predict_next_index >= 0 and new_area == areas[predict_next_index]:
            predictions_in_a_row += 1
            predict_next_index += 1

            assert new_area in areas
            assert pattern_start_index >= 0
            if new_area == areas[pattern_start_index] and predictions_in_a_row > 0:
                areas.append(new_area)
                break
        elif new_area in areas:
            last_index = len(areas) - areas[:areas.index(new_area) - 1:-1].index(new_area) - 1
            predict_next_index = last_index + 1
            if predict_next_index < len(areas):
                pattern_start_index = len(areas)
            else:
                pattern_start_index = -1
                predictions_in_a_row = 0
                predict_next_index = -1
        else:
            pattern_start_index = -1
            predictions_in_a_row = 0
            predict_next_index = -1

        areas.append(new_area)

    values = {}
    for i in range(pattern_start_index, pattern_start_index + predictions_in_a_row + 1):
        values[i % predictions_in_a_row] = areas[i]

    print(f'Day 18 Answer 1: {areas[10]}')
    print(f'Day 18 Answer 2: {values[1000000000 % 28]}')


if __name__ == "__main__":
    main()
