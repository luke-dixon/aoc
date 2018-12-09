from collections import namedtuple, Counter

with open('input6.txt') as f:
  data = f.readlines()

data = [s.strip() for s in data]

def taxicab_distance(p, q):
  return abs(p.x - q.x) + abs(p.y - q.y)


class Point:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label


labels = list(map(chr, range(ord('A'), ord('A') + len(data))))
data = [x.split(', ') for x in data]
data = [Point(int(x_y[0]), int(x_y[1]), label) for x_y, label in zip(data, labels)]


max_x = 0
min_x = 500
max_y = 0
min_y = 500


for d in data:
  if d.x > max_x:
    max_x = d.x
  if d.x < min_x:
    min_x = d.x
  if d.y > max_y:
    max_y = d.y
  if d.y < min_x:
    min_y = d.y


# normalize the points
for d in data:
  d.x -= min_x
  d.y -= min_y


grid = []
for i in range(min_x, max_x + 1):
  row = []
  grid.append(row)
  for j in range(min_y, max_y + 1):
    row.append(0)


for col_i in range(len(grid)):
  for row_i in range(len(grid[0])):
    current_point = Point(col_i, row_i, label='?')
    distances = {}
    for point in data:
      distances[taxicab_distance(point, current_point)] = point
    grid[col_i][row_i] = distances[min(distances)]


for row in grid:
  s = ''
  for cell in row:
    s += cell.label

c = Counter()
for row in grid:
  s = ''
  for cell in row:
    s += cell.label
  c.update(s)


# Remove edge values
inf_values = set()
for col_i in range(len(grid)):
  for row_i in range(len(grid[0])):
    if col_i == 0 or (col_i == len(grid) - 1):
      inf_values.add(grid[col_i][row_i])
    if row_i == 0 or (row_i == len(grid[0]) - 1):
      inf_values.add(grid[col_i][row_i])

for inf_value in inf_values:
  del c[inf_value.label]


print('Day 6 Part 1 Answer: ', c.most_common(1)[0][1])



# Part 2

# This time create the grid a little larger.
# What if the area goes off the other side?
# Maybe I'm just lucky the input I got doesn't do that.
grid = []
for i in range(min_x, max_x + 100):
  row = []
  grid.append(row)
  for j in range(min_y, max_y + 100):
    row.append(0)


for col_i in range(len(grid)):
  for row_i in range(len(grid[0])):
    current_point = Point(col_i, row_i, label='?')
    distance = 0
    for point in data:
      distance += taxicab_distance(point, current_point)
    grid[col_i][row_i] = distance





#for row in grid:
#  s = ''
#  for cell in row:
#    if cell < 10000:
#      s += 'T'
#    else:
#      s += 'F'
#  print(s)


area = 0


for row in grid:
  for cell in row:
    if cell < 10000:
      area += 1

print('Day 6 Part 1 Answer: ', area)
