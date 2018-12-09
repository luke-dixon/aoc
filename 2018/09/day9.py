from itertools import cycle


class Marble:
  __slots__ = ('value', 'prev', 'next')

  def __init__(self, value, prev=None, next=None):
    self.value = value
    self.prev = prev
    self.next = next

  def __repr__(self):
    return f'Marble({self.value})'


class Circle:
  __slots__ = ('current_marble', 'count')

  def __init__(self):
    self.current_marble = None
    self.count = 0

  def add_marble(self, marble):
    if self.current_marble == None:
      marble.prev, marble.next = marble, marble
      self.current_marble = marble
    else:
      # Move one marble forward
      self.current_marble = self.current_marble.next

      # Place the new marble
      next_marble = self.current_marble.next
      marble.prev, marble.next = self.current_marble, next_marble
      (
          self.current_marble.next,
          marble.prev,
          marble.next,
          next_marble.prev,
          self.current_marble,
          self.count,
      ) = (
           marble,
           self.current_marble,
           next_marble,
           marble,
           marble,
           self.count + 1,
      )
    assert self.current_marble is not None
    assert self.current_marble.next is not None
    assert self.current_marble.prev is not None

  def take_marble(self):
    assert self.current_marble is not None
    # Go back seven marbles
    for _ in range(7):
        self.current_marble = self.current_marble.prev

    # Take this marble
    taken_marble = self.current_marble

    # Update links for surrounding marbles
    prev_marble, next_marble = taken_marble.prev, taken_marble.next
    (
        prev_marble.next,
        next_marble.prev,
        self.current_marble,
        self.count,
    ) = (
        next_marble,
        prev_marble,
        next_marble,
        self.count + 1,
    )

    taken_marble.prev, taken_marble.next = None, None
    return taken_marble


def run_game(player_count, marble_count):
  current_marble = None
  circle_count = 0
  player_score = {}
  circle = Circle()
  for marble, player in zip(range(0, marble_count + 1), cycle(range(player_count))):
    assert player < player_count
    assert marble <= marble_count
    if marble == 0:
      circle.add_marble(Marble(marble))
      continue
    if marble % 23 == 0:
      # special case
      taken_marble = circle.take_marble()
      if player not in player_score:
        player_score[player] = 0
      player_score[player] += marble + taken_marble.value
      continue
    circle.add_marble(Marble(marble))
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
