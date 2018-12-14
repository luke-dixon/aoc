def iterate(state, elf1, elf2):
    sum_current = int(chr(state[elf1])) + int(chr(state[elf2]))
    for c in str(sum_current):
        state.append(ord(c))
    elf1 = (elf1 + int(chr(state[elf1])) + 1) % len(state)
    elf2 = (elf2 + int(chr(state[elf2])) + 1) % len(state)
    return elf1, elf2


def check_for_input_in_iteration(state, data):
    return state[-len(str(data)) - 1:].find(str(data).encode('utf8')) != -1


with open('input14.txt') as f:
    data = int(f.read().strip())

initial_data = [3, 7]

elf1 = 0
elf2 = 1

state = bytearray(''.join((str(x) for x in initial_data)), 'utf8')
while len(state) <= 9:
    elf1, elf2 = iterate(state, elf1, elf2)

while len(state) <= data:
    elf1, elf2 = iterate(state, elf1, elf2)

while len(state) <= data + 10:
    elf1, elf2 = iterate(state, elf1, elf2)

print('Day 14 Part 1 Answer: ', end='')
print(''.join([str(chr(x)) for x in state[data:data+10]]))

while True:
    elf1, elf2 = iterate(state, elf1, elf2)
    if check_for_input_in_iteration(state, data):
        break

print('Day 14 Answer 2: ', end='')
print(state.find(str(data).encode('utf8')))
