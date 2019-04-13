from collections import deque, namedtuple

import networkx as nx


def draw_grid(grid):
    for row in grid:
        print(''.join(row))


CellData = namedtuple('CellData', ['geologic_index', 'erosion_level', 'torch_visited', 'climbing_gear_visited', 'unequiped_visited'])
possible_moves = {
    'torch': ('.', '|'),
    'climbing gear': ('.', '='),
    'neither': ('=', '|'),
}


def main():
    depth, target = get_data()
    print(target)
    grid, grid_data = construct_grid(depth, target)

    #draw_grid(grid)
    print(f'Day 22 Part 1 Answer: {calculate_risk_level(grid_data, target)}')

    print(f'length of grid-data {len(grid_data)}')

    print('Constructing graph')
    nodes_in_queue = set()
    nodes_processed = set()
    queue = deque()
    graph = nx.Graph()
    graph.add_node((0, 0, 'torch'))
    queue.append((0, 0, 'torch'))
    nodes_in_queue.add((0, 0, 'torch'))
    i = 0
    while len(queue):
        i += 1
        if i % 2500000 == 0 and (0, 0, 'torch') in graph.nodes and (target[0], target[1], 'torch') in graph.nodes:
            print(f'Graph Nodes: {len(graph.nodes)}')
            print(f'Graph Edges: {len(graph.edges)}')
            try:
                shortest_path = nx.algorithms.shortest_path(graph, source=(0, 0, 'torch'), target=(target[0], target[1], 'torch'))
                weight = 0
                for edge in zip(shortest_path[:-1], shortest_path[1:]):
                    weight += graph.edges[edge]['weight']
                print(f'shortest path length: {len(shortest_path)} {weight}')
            except Exception:
                pass
        y, x, tool = queue.popleft()
        #y, x, tool = queue.pop()
        if i % 100000 == 0:
            print(i, (x, y, tool))

        nodes_in_queue.remove((y, x, tool))
        nodes_processed.add((y, x, tool))

        for next_tool in ['torch', 'climbing gear', 'neither']:
            if next_tool == tool:
                continue
            if grid[y][x] not in possible_moves[next_tool]:
                continue
            graph.add_edge((y, x, tool), (y, x, next_tool), weight=7)
            if not ((y, x, next_tool) in nodes_in_queue or (y, x, next_tool) in nodes_processed):
                queue.append((y, x, next_tool))
                nodes_in_queue.add((y, x, next_tool))

        search_add_edge_and_queue(graph, grid, nodes_in_queue, nodes_processed, queue, y, x, tool, y + 1, x, target)
        search_add_edge_and_queue(graph, grid, nodes_in_queue, nodes_processed, queue, y, x, tool, y - 1, x, target)
        search_add_edge_and_queue(graph, grid, nodes_in_queue, nodes_processed, queue, y, x, tool, y, x + 1, target)
        search_add_edge_and_queue(graph, grid, nodes_in_queue, nodes_processed, queue, y, x, tool, y, x - 1, target)

    print(f'Graph Nodes: {len(graph.nodes)}')
    print(f'Graph Edges: {len(graph.edges)}')
    shortest_path = nx.algorithms.dijkstra_path(graph, source=(0, 0, 'torch'), target=(target[0], target[1], 'torch'))
    weight = 0
    for edge in zip(shortest_path[:-1], shortest_path[1:]):
        weight += graph.edges[edge]['weight']
    print(shortest_path)
    print(f'shortest path length: {len(shortest_path)} {weight}')


def search_add_edge_and_queue(graph, grid, nodes_in_queue, nodes_processed, queue, y, x, tool, new_y, new_x, target):
    if new_y < 0 or new_x < 0:
        return

    # Guess it's kind of not going to be way out
    if new_y > target[0] + 20 or new_x > target[1] + 20:
        return

    try:
        if grid[new_y][new_x] in possible_moves[tool]:
            graph.add_edge((y, x, tool), (new_y, new_x, tool), weight=1)
            if not ((new_y, new_x, tool) in nodes_in_queue or (new_y, new_x, tool) in nodes_processed):
                queue.append((new_y, new_x, tool))
                nodes_in_queue.add((new_y, new_x, tool))
    except IndexError:
        pass


def calculate_risk_level(grid_data, target):
    risk_level = 0
    for y in range(target[0] + 1):
        for x in range(target[1] + 1):
            erosion_level = grid_data[(y, x)][1]
            risk_level += (erosion_level % 3)
    return risk_level


def construct_grid(depth, target):
    grid = []
    for y in range(depth):
        row = []
        for x in range(depth):
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


def get_data():
    with open('input22.txt') as f:
        depth = int(f.readline().strip('\n').lstrip('depth: '))
        target = f.readline().strip('\n').lstrip('target: ').split(',')
    target = (int(target[1]), int(target[0]))
    return depth, target


if __name__ == "__main__":
    main()
