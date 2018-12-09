from collections import deque
from itertools import cycle


class Circle:
  __slots__ = ('ring')

  def __init__(self):
    self.ring = deque()

  def add_marble(self, marble):
    if len(self.ring) == 0:
      self.ring.append(marble)
    else:
      self.ring.append(self.ring.popleft())
      self.ring.append(marble)

  def take_marble(self):
    # Go back seven marbles
    self.ring.rotate(7)

    # Take this marble
    taken_marble = self.ring.pop()

    # Move forward one
    self.ring.append(self.ring.popleft())
    return taken_marble


def run_game(player_count, marble_count):
  circle_count = 0
  player_score = {}
  circle = Circle()
  for marble, player in zip(range(0, marble_count + 1), cycle(range(player_count))):
    assert player < player_count
    assert marble <= marble_count

    # Special case for marble 0 since it is divisible by 23
    if marble == 0:
      circle.add_marble(marble)
      continue

    if marble % 23 == 0:
      taken_marble = circle.take_marble()
      if player not in player_score:
        player_score[player] = 0
      player_score[player] += marble + taken_marble
      continue

    circle.add_marble(marble)
  return player_score


result_table = [
  ((9, 25), 32),
  ((10, 1618), 8317),
  ((13, 7999), 146373),
  ((17, 1104), 2764),
  ((21, 6111), 54718),
  ((30, 5807), 37305),
]
for i, o in result_table:
  result = run_game(*i)
  print(max(result.values()), o)
  assert max(result.values()) == o


with open('input9.txt') as f:
  data = f.read()

player_count = int(data.split()[0])
marble_count = int(data.split()[-2])
print(str(max(run_game(player_count, marble_count).values())))
print(str(max(run_game(player_count, marble_count * 100).values())))
