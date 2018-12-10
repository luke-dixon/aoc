import time

with open('input10.txt') as f:
  data = f.readlines()


class Star:
  def __init__(self, values):
    self.x = values[0]
    self.y = values[1]
    self.v_x = values[2]
    self.v_y = values[3]
  def __repr__(self):
    return f'Star({self.x}, {self.y})'


def get_position_x_data_begin(d):
  return len('position=<')

def get_position_x_data_end(d):
  return d.index(',')

def get_position_y_data_begin(d):
  return d.index(',') + 1

def get_position_y_data_end(d):
  return d.index('>')

def get_velocity_x_data_begin(d):
  return d.rindex('<') + 1

def get_velocity_x_data_end(d):
  return d.rindex(',')

def get_velocity_y_data_begin(d):
  return d.rindex(',') + 1

def get_velocity_y_data_end(d):
  return d.rindex('>')


stars = []
for d in data:
  x = int(d[get_position_x_data_begin(d):get_position_x_data_end(d)])
  y = int(d[get_position_y_data_begin(d):get_position_y_data_end(d)])
  velocity_x = int(d[get_velocity_x_data_begin(d):get_velocity_x_data_end(d)])
  velocity_y = int(d[get_velocity_y_data_begin(d):get_velocity_y_data_end(d)])
  stars.append(Star((x, y, velocity_x, velocity_y)))



def update(stars):
  for star in stars:
    star.x += star.v_x
    star.y += star.v_y
  return 1


def reverse(stars):
  for star in stars:
    star.x -= star.v_x
    star.y -= star.v_y
  return -1


def find_star_range(stars):
  min_x, max_x = stars[0].x, stars[0].x
  min_y, max_y = stars[0].y, stars[0].y
  for star in stars:
    if star.x < min_x:
      min_x = star.x
    if star.x > max_x:
      max_x = star.x
    if star.y < min_y:
      min_y = star.y
    if star.y > max_y:
      max_y = star.y
  return (min_x, max_x), (min_y, max_y)


def distance(x1, x2):
  return abs(x2 - x1)


last_range_x, last_range_y = find_star_range(stars)
seconds = 0
seconds += update(stars)
range_x, range_y = find_star_range(stars)


# Go until the distance between the most distance stars begins to increase
while distance(*last_range_x) > distance(*range_x) and distance(*last_range_y) > distance(*range_y):
  seconds += update(stars)
  last_range_x, last_range_y = range_x, range_y
  range_x, range_y = find_star_range(stars)


# Back up a bit for dramatic effect
for i in range(5):
  seconds += reverse(stars)


def draw(stars):
  range_x, range_y = find_star_range(stars)
  # Hope the stars all have positive locations
  # For my data set they do, I should probably account for that though
  assert range_x[0] > 0 and range_x[1] > 0
  assert range_y[0] > 0 and range_y[1] > 0
  star_map = []
  for i in range(range_y[1] + 1):
    star_map.append([])
    for j in range(range_x[1] + 1):
      star_map[i].append(' ')
  for star in stars:
    star_map[star.y][star.x] = '*'
  for row in star_map[range_y[0]:]:
    print(''.join(row[range_x[0]:]))


for i in range(3):
  seconds += update(stars)
  draw(stars)
  print(f'{seconds} seconds')
  time.sleep(1)

print('2018 Day 10 Answer 1:')
seconds += update(stars)
draw(stars)
# Answer 2
print(f'2018 Day 10 Answer 2: {seconds} seconds')

