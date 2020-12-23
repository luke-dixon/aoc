from lib import puzzle


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


class Day23(puzzle.Puzzle):
    year = '2017'
    day = '23'

    def get_data(self):
        data = self.input_data
        return [line.split(' ') for line in data.splitlines()]

    def part1(self):
        program = self.get_data()
        reg = {}
        for i in range(ord('a'), ord('h') + 1):
            reg[chr(i)] = 0

        reg['instruction_pointer'] = 0
        reg['num_muls'] = 0

        while 0 <= reg['instruction_pointer'] < len(program):
            op, a, b = program[reg['instruction_pointer']]
            ops[op](reg, a, b)
            reg['instruction_pointer'] += 1
        return reg['num_muls']

    def part2(self):
        return 'See hand optimised .c file'

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
