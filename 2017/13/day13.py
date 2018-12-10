with open('input13.txt') as f:
  data = [[int(y) for y in x.strip().split(': ')] for x in f.readlines()]


class Scanner:
  def __init__(self, range):
    self.range = (2 * range) - 2
    self.current = 0

  def update(self, steps=1):
    self.current += steps
    self.current = self.current % (self.range)

  def __repr__(self):
    return f'Scanner(current={self.current}, range={self.range})'


scanners = {}
for d in data:
  scanners[d[0]] = Scanner(d[1])


def run(player_initial=-1):
  caught = 0
  player = -1
  while player < max(scanners.keys()):
    player += 1
    if player in scanners and scanners[player].current == 0:
      caught += player * scanners[player].range
    for scanner in scanners:
      scanners[scanner].update()
  return caught

print(f'Day 13 Answer 1 {run()}')

i = -1
found = False
while not found:
  i += 1
  found = True
  for scanner in scanners:
    if (i + scanner) % scanners[scanner].range == 0:
      found = False
      break

print(f'Day 13 Answer 2 {i - 1}')
