with open('input13.txt') as f:
  data = [[int(y) for y in x.strip().split(': ')] for x in f.readlines()]


class Scanner:
  def __init__(self, range):
    self.range = range
    self.current = 0
    self.direction = 0

  def update(self, steps=1):
    for _ in range(steps):
      if self.direction == 0 and self.current < self.range - 1:
        self.current += 1
      elif self.direction == 0 and self.current == self.range - 1:
        self.current -= 1
        self.direction = 1
      elif self.direction == 1 and self.current > 0:
        self.current -= 1
      elif self.direction == 1 and self.current == 0:
        self.current += 1
        self.direction = 0

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


# First scanner was too slow, need a new one
class Scanner2:
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
  scanners[d[0]] = Scanner2(d[1])


i = 0
found = False
while not found:
  # Reset all scanners
  for scanner in scanners:
    scanners[scanner].current = 0

  # Run scanners to their current configuration for this run
  for scanner in scanners:
    scanners[scanner].update(steps=scanner + i)

  # Check we don't get caught
  found = True
  for scanner in scanners:
    if scanners[scanner].current == 0:
      found = False
      break

  # Another go
  i += 1

print(f'Day 13 Answer 2 {i - 1}')
