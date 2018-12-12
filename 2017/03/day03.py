with open('input3.txt') as f:
    data = int(f.read().strip('\n'))


class Node:
    def __init__(self, x, y, i):
        self.x, self.y = x, y
        self.i = i
        self.value = 0

    def __repr__(self):
        return f'Node({self.x}, {self.y}, {self.i}, {self.value})'


(x, y) = (0, 0)

i = 1
min_x, max_x, min_y, max_y = 0, 0, 0, 0
last_node = Node(0, 0, i)
last_node.value = 1
nodes = {}
nodes_by_coords = {}
nodes[i] = last_node
nodes_by_coords[(0, 0)] = last_node

answer2_node = None

while i < data:
    i += 1
    if x == max_x and y == min_y:
        x += 1
        max_x += 1
        min_x -= 1
        max_y += 1
        min_y -= 1
    elif x == max_x and y < max_y:
        y += 1
    elif x > min_x and y == max_y:
        x -= 1
    elif x == min_x and y > min_y:
        y -= 1
    elif x < max_x and y == min_y:
        x += 1
    else:
        assert False
    new_node = Node(x, y, i)
    nodes[i] = new_node
    nodes_by_coords[(x, y)] = new_node
    if not answer2_node:
        adjacent_values = []
        for j in range(new_node.x - 1, new_node.x + 2):
            for k in range(new_node.y - 1, new_node.y + 2):
                adjacent_node = nodes_by_coords.get((j, k))
                if adjacent_node:
                    adjacent_values.append(adjacent_node.value)
        new_node.value = sum(adjacent_values)
        assert new_node.value >= last_node.value
    last_node = new_node
    if last_node.value > data:
        answer2_node = last_node

print(f'Day 3 part 1 Answer: {abs(last_node.x) + abs(last_node.y)}')
print(f'Day 3 part 2 Answer: {answer2_node.value}')
