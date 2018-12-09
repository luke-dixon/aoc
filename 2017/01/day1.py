with open('input1.txt') as f:
    data = f.read().strip('\n')

print(data)

numbers = []

if data[-1] == data[0]:
    numbers.append(int(data[0]))

for i in range(len(data) - 1):
    if data[i] == data[i + 1]:
        numbers.append(int(data[i]))

print(f'2017 Day 1 Part 1 Answer: {sum(numbers)}')

numbers = []

for i in range(len(data)):
    halfway_from_i = ((len(data) // 2) + i) % len(data)
    if data[i] == data[((len(data) // 2) + i) % len(data)]:
        numbers.append(int(data[i]))

print(f'2017 Day 1 Part 2 Answer: {sum(numbers)}')
