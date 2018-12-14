from collections import deque


with open('input17.txt') as f:
    data = int(f.read().strip())

ring = deque([])

for i in range(0, 2017 + 1):
    ring.rotate(-data)
    ring.append(i)

ring.rotate(-1)
answer = ring.pop()
print(f'Day 17 Part 1 Answer: {answer}')
ring.append(answer)

# Start over
current = 0
after_zero = 0

i = 0
for i in range(1, 50000000):
    # Each time we go forward x times where x is our input.
    # Afterwards we go forward by 1.
    # The first time through it doesn't matter what we do as there is
    # only one element so it's fine to move what happens afterwards here.
    current = (current + data + 1) % (i)
    if current == 0:
        after_zero = i

print(f'Day 17 Part 2 Answer: {after_zero}')
