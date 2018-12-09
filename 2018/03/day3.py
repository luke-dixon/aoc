from collections import namedtuple

with open('input3.txt') as f:
  data = f.read()

Rectangle = namedtuple('Rectangle', ['id', 'x', 'y', 'w', 'h'])

rectangles = []


split_data = data.split()
for i in range(len(split_data) // 4):
  id, _, pos, size = split_data[i * 4:(i * 4) + 4]
  pos = pos.strip(':')
  id = id.strip('#')
  x, y = pos.split(',')
  w, h = size.split('x')
  rectangles.append(Rectangle(int(id), int(x), int(y), int(w), int(h)))


fabric = []
for i in range(1000):
  i_l = []
  for j in range(1000):
    i_l.append(0)
  fabric.append(i_l)


for r in rectangles:
  for i in range(r.w):
    for j in range(r.h):
      fabric[r.x + i][r.y + j] += 1


count = 0
for row in range(len(fabric)):
  for col in range(len(fabric[row])):
    if fabric[row][col] > 1:
      count += 1

print('Day 3 part one answer: %d' % count)


for r in rectangles:
  overlaps = False
  for i in range(r.w):
    for j in range(r.h):
      if fabric[r.x + i][r.y + j] > 1:
        overlaps = True
        break
    if overlaps:
      break
  if not overlaps:
    print('Day 3 part two answer: %d' % r.id)
