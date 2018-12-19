import math


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


def sum_divisors(value):
    s = 0
    rt = int(math.sqrt(value + 1))
    for i in range(1, rt + 1):
        if value % i == 0:
            s += i
            d = value // i
            if d != i:
                s += d
    return s


def run_program(reg, program, instruction_pointer_index, optimize=False):
    instruction_pointer = reg[instruction_pointer_index]

    while 0 <= instruction_pointer < len(program):
        reg[instruction_pointer_index] = instruction_pointer
        op, a, b, c = program[instruction_pointer]
        instruction_set[op](reg, a, b, c)
        instruction_pointer = reg[instruction_pointer_index]
        instruction_pointer += 1
        if optimize and instruction_pointer == 5:
            break
    print(f'Finding sum of divisors for {reg[b]}')
    if optimize:
        reg[0] = sum_divisors(reg[b])


def main():
    with open('input19.txt') as f:
        data = f.read().rstrip('\n').splitlines()

    instruction_pointer_index = int(data[0].lstrip('#ip '))
    data.pop(0)

    program = []
    for d in data:
        op, a, b, c = d.split(' ')
        a, b, c = int(a), int(b), int(c)
        program.append((op, a, b, c))

    reg = [0, 0, 0, 0, 0, 0]
    instruction_pointer = reg[instruction_pointer_index]

    run_program(reg, program, instruction_pointer_index, optimize=True)

    # print(f'reg: {reg}, ip: {instruction_pointer}')
    print(f'Day 19 Answer 1 reg: {reg[0]}')

    reg = [1, 0, 0, 0, 0, 0]
    instruction_pointer = reg[instruction_pointer_index]

    run_program(reg, program, instruction_pointer_index, optimize=True)

    print(f'Day 19 Answer 2 reg: {reg[0]}')

if __name__ == "__main__":
    main()
