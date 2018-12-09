with open('input2.txt') as f:
    data = f.read()


total = 0
for d in data.split():
  if d.startswith('+'):
    total += int(d[1:])
  if d.startswith('-'):
    total -= int(d[1:])

print(total)




total = 0
frequencies = set()
frequencies.add(total)

found = False
repeats = -1
while not found:
  repeats += 1
  for d in data.split():
    if d.startswith('+'):
      total += int(d[1:])
    if d.startswith('-'):
      total -= int(d[1:])
    if d == '':
      print('breaking')
      break
    if total == 502:
      print('502 found', d)
    if total in frequencies:
      print('Duplicate', total)
      found = True
      break
    frequencies.add(total)

print('Total', total)
print('Repeats', repeats)




from collections import Counter
with open('input2.txt') as f:
  data = f.read()


twos = 0
threes = 0

for d in data.split():
  values = Counter(d).values()
  if 2 in values:
    twos += 1
  if 3 in values:
    threes += 1

print(twos, ' x ', threes, ' = ', twos * threes)


sorted_data = sorted(data.split())
for i in range(len(sorted_data)):
  for j in range(i + 1, len(sorted_data)):
    assert i != j
    assert len(sorted_data[i]) == len(sorted_data[j])
    diff = 0
    diff_index = 0
    for n in range(len(sorted_data[i])):
      if sorted_data[i][n] != sorted_data[j][n]:
        #print('d[n] != x[n]', d[n], x[n])
        diff += 1
        diff_index = n
    if diff == 1:
      print(sorted_data[i])
      print(sorted_data[j])
      print(('-' * diff_index) + '^')
      print(sorted_data[i][:diff_index] + sorted_data[i][diff_index + 1:])
