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
            max_coords = (x + 1, y + 1)
            max_powerlevel = m[y][x]


print(f'Day 11 Part 1 Answer: {max_coords[0]},{max_coords[1]}')

max_powerlevel = -0xfffffff
max_coords = (0, 0)
max_size = 1

sum_matrix = sqmatrix_sum_squares(l, 2)

for size in range(2, len(l) + 1):
    next_size = size + 1
    print(f'size: {size}')

    # Remove a row and column from the sum matrix
    sum_matrix.pop()
    for row in sum_matrix:
        row.pop()

    # For each sum in the sum matrix, add another layer
    ws = [sum([l[i][size + j] for i in range(0, size)]) for j in range(len(l) - next_size + 1)]
    for y in range(len(l) - next_size + 1):
        h = sum([l[size + y][i] for i in range(0, size)])
        for x in range(len(l) - next_size + 1):
            w = ws[x]
            sum_matrix[y][x] += h + w + l[y + size][x + size]
            if sum_matrix[y][x] > max_powerlevel:
                max_coords = (x + 1, y + 1)
                max_powerlevel = sum_matrix[y][x]
                max_size = next_size
                print(f'new max: {max_powerlevel}, ({max_coords}), {next_size}')
            h -= l[size + y][x]
            h += l[size + y][min(x + next_size, x + size)]
        for w in range(len(ws)):
            ws[w] -= l[y][size + w]
            ws[w] += l[y + size][size + w]

print(f'Day 11 Part 2 Answer: {max_coords[0]},{max_coords[1]},{max_size}')
