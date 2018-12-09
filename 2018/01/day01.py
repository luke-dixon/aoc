with open('input1.txt') as f:
    data = [int(x) for x in f.read().strip('\n').split('\n')]

print(f'Day 1 Part 1 Answer: {sum(data)}')

found = False
frequency = 0
frequencies = {frequency}

while not found:
    for d in data:
        frequency += d
        if frequency in frequencies:
            found = True
            break
        frequencies.add(frequency)

print(f'Day 1 Part 2 Answer: {frequency}')
