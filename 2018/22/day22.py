import networkx as nx


possible_moves = {
    'torch': ('.', '|'),
    'climbing gear': ('.', '='),
    'neither': ('=', '|'),
}


def get_data():
    with open('input22.txt') as f:
        depth = int(f.readline().strip('\n').lstrip('depth: '))
        target = f.readline().strip('\n').lstrip('target: ').split(',')
    target = (int(target[1]), int(target[0]))
    return depth, target


def calculate_risk_level(grid_data, target):
    risk_level = 0
    for y in range(target[0] + 1):
        for x in range(target[1] + 1):
            erosion_level = grid_data[(y, x)][1]
            risk_level += (erosion_level % 3)
    return risk_level


def construct_grid(depth, target):
    grid = []
    beyond_target_limit = 20  # TODO: how much is safe?
    for y in range(min(depth, target[0] + beyond_target_limit)):
        row = []
        for x in range(min(depth, target[1] + beyond_target_limit)):
            row.append('.')
        grid.append(row)
    grid_data = {}
    for y, row in enumerate(grid):
        for x, square in enumerate(row):
            if y == 0 and x == 0:
                grid[y][x] = 'M'
                geologic_index = 0
                erosion_level = (geologic_index + depth) % 20183
                grid_data[(y, x)] = (geologic_index, erosion_level)
                continue
            elif y == target[0] and x == target[1]:
                geologic_index = 0
                erosion_level = (geologic_index + depth) % 20183
                grid_data[(y, x)] = (geologic_index, erosion_level)
            elif y == 0 and x != 0:
                geologic_index = x * 16807
                erosion_level = (geologic_index + depth) % 20183
                grid_data[(y, x)] = (geologic_index, erosion_level)
            elif y != 0 and x == 0:
                geologic_index = y * 48271
                erosion_level = (geologic_index + depth) % 20183
                grid_data[(y, x)] = (geologic_index, erosion_level)
            else:
                geologic_index = grid_data[(y, x - 1)][1] * grid_data[(y - 1, x)][1]
                erosion_level = (geologic_index + depth) % 20183
                grid_data[(y, x)] = (geologic_index, erosion_level)
            if erosion_level % 3 == 0:
                grid[y][x] = '.'
            elif erosion_level % 3 == 1:
                grid[y][x] = '='
            elif erosion_level % 3 == 2:
                grid[y][x] = '|'
            else:
                assert False
    return grid, grid_data


def graph_add_edges_to_tool_changes(graph, grid, nodes_processed, stack, tool, y, x):
    for next_tool in ['torch', 'climbing gear', 'neither']:
        if next_tool == tool:
            continue
        if grid[y][x] not in possible_moves[next_tool]:
            continue
        graph.add_edge((y, x, tool), (y, x, next_tool), weight=7)
        if (y, x, next_tool) not in nodes_processed:
            stack.append((y, x, next_tool))
            nodes_processed.add((y, x, next_tool))


def graph_add_edges_to_adjacent(graph, grid, nodes_processed, stack, y, x, tool, new_y, new_x):
    if new_y < 0 or new_x < 0:
        return

    try:
        if grid[new_y][new_x] in possible_moves[tool]:
            graph.add_edge((y, x, tool), (new_y, new_x, tool), weight=1)
            if (new_y, new_x, tool) not in nodes_processed:
                stack.append((new_y, new_x, tool))
                nodes_processed.add((new_y, new_x, tool))
    except IndexError:
        pass


def graph_from_grid(grid):
    nodes_processed = set()
    stack = []
    graph = nx.Graph()
    graph.add_node((0, 0, 'torch'))
    stack.append((0, 0, 'torch'))
    nodes_processed.add((0, 0, 'torch'))
    while len(stack):
        y, x, tool = stack.pop()

        graph_add_edges_to_tool_changes(graph, grid, nodes_processed, stack, tool, y, x)

        graph_add_edges_to_adjacent(graph, grid, nodes_processed, stack, y, x, tool, y + 1, x)
        graph_add_edges_to_adjacent(graph, grid, nodes_processed, stack, y, x, tool, y - 1, x)
        graph_add_edges_to_adjacent(graph, grid, nodes_processed, stack, y, x, tool, y, x + 1)
        graph_add_edges_to_adjacent(graph, grid, nodes_processed, stack, y, x, tool, y, x - 1)
    return graph


def part1(grid_data, target):
    print(f'Day 22 Part 1 Answer: {calculate_risk_level(grid_data, target)}')


def part2(grid, target):
    graph = graph_from_grid(grid)
    shortest_path = nx.algorithms.dijkstra_path(graph, source=(0, 0, 'torch'), target=(target[0], target[1], 'torch'))
    weight = 0
    for edge in zip(shortest_path[:-1], shortest_path[1:]):
        weight += graph.edges[edge]['weight']
    print(f'Day 22 Part 2 Answer: {weight}')


def main():
    depth, target = get_data()
    grid, grid_data = construct_grid(depth, target)

    part1(grid_data, target)
    part2(grid, target)


if __name__ == "__main__":
    main()
