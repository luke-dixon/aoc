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

print(f'Part 1 Answer: {twos * threes}')


sorted_data = sorted(data.split())
for i in range(len(sorted_data)):
  for j in range(i + 1, len(sorted_data)):
    assert i != j
    assert len(sorted_data[i]) == len(sorted_data[j])
    diff = 0
    diff_index = 0
    for n in range(len(sorted_data[i])):
      if sorted_data[i][n] != sorted_data[j][n]:
        diff += 1
        diff_index = n
    if diff == 1:
      answer = sorted_data[i][:diff_index] + sorted_data[i][diff_index + 1:]
      print(f'Part 2 Answer: {answer}')
