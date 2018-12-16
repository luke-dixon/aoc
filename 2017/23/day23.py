with open('input23.txt') as f:
    program = [x.strip('\n').split(' ') for x in f.readlines()]


def set_(reg, x, y):
    try:
        reg[x] = int(y)
    except ValueError:
        reg[x] = reg[y]


def sub(reg, x, y):
    try:
        reg[x] -= int(y)
    except ValueError:
        reg[x] -= reg[y]


def mul(reg, x, y):
    reg['num_muls'] += 1
    try:
        reg[x] *= int(y)
    except ValueError:
        reg[x] *= reg[y]


def jnz(reg, x, y):
    try:
        x = int(x)
    except ValueError:
        x = reg[x]
    try:
        y = int(y)
    except ValueError:
        y = reg[y]
    if x != 0:
        reg['instruction_pointer'] += y - 1


ops = {
    'set': set_,
    'sub': sub,
    'mul': mul,
    'jnz': jnz,
}
reg = {}
for i in range(ord('a'), ord('h') + 1):
    reg[chr(i)] = 0

reg['instruction_pointer'] = 0
reg['num_muls'] = 0

while 0 <= reg['instruction_pointer'] < len(program):
    op, a, b = program[reg['instruction_pointer']]
    ops[op](reg, a, b)
    reg['instruction_pointer'] += 1

print(f"Day 23 Part 1 Answer: {reg['num_muls']}")
