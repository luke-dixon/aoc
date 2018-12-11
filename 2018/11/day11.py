from itertools import chain
from functools import lru_cache


with open('input11.txt') as f:
  data = int(f.read().strip())

l = []
for i in range(300):
    l.append([])
    for j in range(300):
        y = i + 1
        x = j + 1
        rack_id = x + 10
        power_level = rack_id * y
        power_level += data
        power_level *= rack_id
        l[i].append(((power_level % 1000) // 100) - 5)


def sqmatrix_sum_squares(m, size=2):
    m2 = []
    for i in range(len(m) - size + 1):
        r2 = []
        m2.append(r2)
        for j in range(len(m) - size + 1):
            r2.append(sum([sum(tuple(m[j:j + size])) for m in m[i:i + size]]))
    return m2


def print_matrix(m, rows, cols):
    for row in range(rows):
        print(m[row][:cols])


max_powerlevel = 0
max_coords = (0, 0)

m = sqmatrix_sum_squares(l, 3)
for y in range(len(m)):
    for x in range(len(m)):
        if m[y][x] > max_powerlevel:
            print(f'new max: {m[y][x]}, {x + 1},{y + 1},3')
            max_coords = (x + 1, y + 1)
            max_powerlevel = m[y][x]


print(max_powerlevel)
print(max_coords)

max_powerlevel = -0xfffffff
max_coords = (0, 0)
max_size = 1

sum_matrix = sqmatrix_sum_squares(l, 2)

for size in range(3, len(l)):
    print(f'size: {size}')

    # Remove a row and column from the sum matrix
    sum_matrix.pop()
    for row in sum_matrix:
        row.pop()

    # For each sum in the sum matrix, add another layer
    for y in range(len(l) - size + 1):
        for x in range(len(l) - size + 1):
            h = sum([l[size - 1 + y][i] for i in range(x, x + size - 1)])
            w = sum([l[i][size - 1 + x] for i in range(y, y + size - 1)])
            sum_matrix[y][x] += h + w + l[y + size - 1][x + size - 1]
            if sum_matrix[y][x] > max_powerlevel:
                max_coords = (x + 1, y + 1)
                max_powerlevel = sum_matrix[y][x]
                print(f'new max: {max_powerlevel}, ({max_coords}), {size}')


print(max_powerlevel)
print(max_coords)
print(max_size)
