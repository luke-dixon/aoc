with open('input5.txt') as f:
  data = f.read().strip()

def react1(d):
  for i in range(len(d) - 1):
    if d[i].islower() and d[i + 1].isupper():
      if d[i].upper() == d[i + 1]:
        return True, d[:i] + d[i+2:]
    if d[i].isupper() and d[i + 1].islower():
      if d[i].lower() == d[i + 1]:
        return True, d[:i] + d[i+2:]
  return False, d




def react2(d):
  reactions = False
  reaction_this_cycle = False
  i = 0
  while i + 1 < len(d):
    if d[i].islower() and d[i + 1].isupper():
      if d[i].upper() == d[i + 1]:
        reactions = True
        reaction_this_cycle = True
        d = d[:i] + d[i+2:]
    elif d[i].isupper() and d[i + 1].islower():
      if d[i].lower() == d[i + 1]:
        reactions = True
        reaction_this_cycle = True
        d = d[:i] + d[i+2:]
    if not reaction_this_cycle:
      i += 1
    reaction_this_cycle = False
  if reactions:
    return True, d
  return False, d


sample = data

rc = True
while rc:
  rc, sample = react1(sample)

#print(sample)
print('Day 5 Part 1 Answer: ', len(sample))



results = []
for c in sorted(list(set(sample.upper()))):
  sample2 = sample
  sample2 = ''.join(sample2.split(c))
  sample2 = ''.join(sample2.split(c.lower()))
  rc = True
  while rc:
    rc, sample2 = react1(sample2)
  results.append(len(sample2))

print('Day 5 Part 2 Answer: ', min(results))
