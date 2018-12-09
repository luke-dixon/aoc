with open('input4.txt') as f:
  data = f.readlines()

data = [x.strip('\n') for x in data]


guards = {}

current_guard = None

for line in sorted(data):
  year = line[1:5]
  month = line[6:8]
  day = line[9:11]
  hour = line[12:14]
  minute = line[15:17]
  message = line[19:]
  if message.startswith('Guard ') and message.endswith(' begins shift'):
    guard_id_begin = line.index('#')
    guard_id_end = line[guard_id_begin:].index(' ')
    guard_id = line[guard_id_begin:guard_id_begin + guard_id_end]
    if guard_id in guards:
      current_guard = guards[guard_id]
    else:
      current_guard = { 'id': guard_id, 'events': [] }
      guards[guard_id] = current_guard
    current_guard['events'].append({
      'year': year,
      'month': month,
      'day': day,
      'hour': hour,
      'minute': minute,
      'event': 'starts shift',
    })
  if current_guard and message == 'wakes up':
    current_guard['events'].append({
      'year': year,
      'month': month,
      'day': day,
      'hour': hour,
      'minute': minute,
      'event': message,
    })
  if current_guard and message == 'falls asleep':
    current_guard['events'].append({
      'year': year,
      'month': month,
      'day': day,
      'hour': hour,
      'minute': minute,
      'event': message,
    })



# find the guard who was asleep the most minutes
max_minutes_asleep = 0
guard_max = None
for guard_id in guards:
  guard = guards[guard_id]
  minutes_asleep = 0
  current_sleep = 0
  for event in guard['events']:
    if event['event'] == 'falls asleep':
      current_sleep = int(event['minute'])
    if event['event'] == 'wakes up':
      minutes_asleep += int(event['minute']) - current_sleep
      current_sleep = 0
  if minutes_asleep > max_minutes_asleep:
    max_minutes_asleep = minutes_asleep
    guard_max = guard

# find which minute of the hour the guard was asleep the most
from collections import Counter
minutes = Counter()
asleep_minutes = []
current_sleep = 0
for event in guard_max['events']:
  if event['event'] == 'falls asleep':
    current_sleep = int(event['minute'])
  if event['event'] == 'wakes up':
    asleep_minutes.extend(range(current_sleep, int(event['minute'])))
    current_sleep = 0
Counter(asleep_minutes).most_common(1)


print('Day 4 Answer 1: ', Counter(asleep_minutes).most_common(1)[0][0] * int(guard_max['id'].strip('#')))




max_minute_guard = None
max_minute = 0
max_minute_count = 0

for guard_id in guards:
  guard = guards[guard_id]
  asleep_minutes = Counter()
  current_sleep = 0
  for event in guard['events']:
    if event['event'] == 'falls asleep':
      current_sleep = int(event['minute'])
    if event['event'] == 'wakes up':
      asleep_minutes.update(range(current_sleep, int(event['minute'])))
      current_sleep = 0
  count = asleep_minutes.most_common(1)
  if count and count[0][1] > max_minute_count:
    max_minute = count[0][0]
    max_minute_count = count[0][1]
    max_minute_guard = guard

print('Day 4 Answer 2: ', int(max_minute_guard['id'].strip('#')) * max_minute)
