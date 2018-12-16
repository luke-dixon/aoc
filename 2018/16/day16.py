from collections import namedtuple


instruction_set = {}


def addr(reg, A, B, C):
    reg[C] = reg[A] + reg[B]

instruction_set['addr'] = addr

def addi(reg, A, B, C):
    reg[C] = reg[A] + B

instruction_set['addi'] = addi

def mulr(reg, A, B, C):
    reg[C] = reg[A] * reg[B]

instruction_set['mulr'] = mulr

def muli(reg, A, B, C):
    reg[C] = reg[A] * B

instruction_set['muli'] = muli

def banr(reg, A, B, C):
    reg[C] = reg[A] & reg[B]

instruction_set['banr'] = banr

def bani(reg, A, B, C):
    reg[C] = reg[A] & B

instruction_set['bani'] = bani

def borr(reg, A, B, C):
    reg[C] = reg[A] | reg[B]

instruction_set['borr'] = borr

def bori(reg, A, B, C):
    reg[C] = reg[A] | B

instruction_set['bori'] = bori

def setr(reg, A, B, C):
    reg[C] = reg[A]

instruction_set['setr'] = setr

def seti(reg, A, B, C):
    reg[C] = A

instruction_set['seti'] = seti

def gtir(reg, A, B, C):
    if A > reg[B]:
        reg[C] = 1
    else:
        reg[C] = 0

instruction_set['gtir'] = gtir

def gtri(reg, A, B, C):
    if reg[A] > B:
        reg[C] = 1
    else:
        reg[C] = 0

instruction_set['gtri'] = gtri

def gtrr(reg, A, B, C):
    if reg[A] > reg[B]:
        reg[C] = 1
    else:
        reg[C] = 0

instruction_set['gtrr'] = gtrr

def eqir(reg, A, B, C):
    if A == reg[B]:
        reg[C] = 1
    else:
        reg[C] = 0

instruction_set['eqir'] = eqir

def eqri(reg, A, B, C):
    if reg[A] == B:
        reg[C] = 1
    else:
        reg[C] = 0

instruction_set['eqri'] = eqri

def eqrr(reg, A, B, C):
    if reg[A] == reg[B]:
        reg[C] = 1
    else:
        reg[C] = 0

instruction_set['eqrr'] = eqrr


assert len(set(instruction_set.values())) == len(instruction_set)
assert len(instruction_set) == 16


with open('input16.txt') as f:
    data = [x.strip() for x in f.readlines()]


Sample = namedtuple('Sample', ['before', 'instruction', 'after'])

i = 0
before = None
instruction = None
after = None
sample_instructions = []
program = []
while i < len(data):
    if data[i].startswith('Before: '):
        before = [int(x) for x in data[i].lstrip('Before: [').rstrip(']').split(', ')]
    elif data[i].startswith('After: '):
        after = [int(x) for x in data[i].lstrip('After: [').rstrip(']').split(', ')]
        sample_instructions.append(Sample(before, instruction, after))
    elif data[i - 1].startswith('Before: '):
        instruction = [int(x) for x in data[i].split(' ')]
    elif data[i] == '':
        pass
    else:
        program.append([int(x) for x in data[i].split(' ')])
    i += 1


three_or_more_samples = 0

for sample in sample_instructions:
    matching_instructions = 0
    for instruction_name in instruction_set:
        instruction = instruction_set[instruction_name]
        reg = list(sample.before)
        instruction(reg, *sample.instruction[1:])
        if reg == sample.after:
            matching_instructions += 1

    if matching_instructions >= 3:
        three_or_more_samples += 1

print(f'Day 16 Part 1 Answer: {three_or_more_samples}')

possibilities = {}
for x in range(0, len(instruction_set)):
    possibilities[x] = set()

for sample in sample_instructions:
    for instruction_name in instruction_set:
        instruction = instruction_set[instruction_name]
        reg = list(sample.before)
        instruction(reg, *sample.instruction[1:])
        opcode = sample.instruction[0]
        if reg == sample.after:
            possibilities[opcode].add(instruction_name)

for sample in sample_instructions:
    for instruction_name in instruction_set:
        instruction = instruction_set[instruction_name]
        reg = list(sample.before)
        instruction(reg, *sample.instruction[1:])
        opcode = sample.instruction[0]
        if reg != sample.after:
            possibilities[opcode].discard(instruction_name)


more_than_one_possibility = True
while more_than_one_possibility:
    one_possibility = [x for x in possibilities if len(possibilities[x]) == 1]
    for n in one_possibility:
        instruction_name = possibilities[n].pop()
        for op in possibilities:
            possibilities[op].discard(instruction_name)
        possibilities[n].add(instruction_name)

    more_than_one_possibility = 0
    for n in possibilities:
        if len(possibilities[n]) != 1:
            more_than_one_possibility += 1

opcodes = {}
for p in possibilities:
    opcodes[p] = instruction_set[possibilities[p].pop()]

reg = [0, 0, 0, 0]
for opcode, a, b, c in program:
    instruction = opcodes[opcode]
    instruction(reg, a, b, c)

print(f'Day 16 Part 2 Answer: {reg[0]}')
