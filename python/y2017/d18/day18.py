from collections import deque

from lib import puzzle


def play_sound(reg, args):
    if args[0] in reg:
        reg['freq'] = reg[args[0]]
    else:
        reg['freq'] = int(args[0])
    return 1


def set_(reg, args):
    if args[1] in reg:
        reg[args[0]] = reg[args[1]]
    else:
        reg[args[0]] = int(args[1])
    return 1


def add(reg, args):
    if args[1] in reg:
        reg[args[0]] += reg[args[1]]
    else:
        reg[args[0]] += int(args[1])
    return 1


def mul(reg, args):
    if args[1] in reg:
        reg[args[0]] *= reg[args[1]]
    else:
        reg[args[0]] *= int(args[1])
    return 1


def mod(reg, args):
    if args[1] in reg:
        reg[args[0]] %= reg[args[1]]
    else:
        reg[args[0]] %= int(args[1])
    return 1


def rcv(reg, args):
    if reg['freq'] == 0:
        return 1
    reg[args[0]] = reg['freq']
    return 1


def jgz(reg, args):
    if args[1] in reg:
        jump = reg[args[1]]
    else:
        jump = int(args[1])
    if args[0] in reg:
        value = reg[args[0]]
    else:
        value = int(args[0])
    if value > 0:
        return jump
    return 1


instructions = {
    'snd': play_sound,
    'set': set_,
    'add': add,
    'mul': mul,
    'mod': mod,
    'rcv': rcv,
    'jgz': jgz,
}


def run_process(reg, program, instructions):
    if not (-1 < reg['next_instruction'] < len(program)):
        print(f"instruction out of range {reg['next_instruction']} {len(program)}")
        reg['terminated'] = True
        return 0
    if reg['terminated']:
        print('process terminated')
        return 0
    old_i = reg['next_instruction']
    next_instruction = program[old_i]
    reg['next_instruction'] += instructions[next_instruction[0]](reg, next_instruction[1:])


def new_snd(reg, args):
    if args[0] in reg:
        value = reg[args[0]]
    else:
        value = int(args[0])
    reg['snd_count'] += 1
    reg['snd_queue'].append(value)
    return 1


def new_rcv(reg, args):
    if len(reg['rcv_queue']):
        reg[args[0]] = reg['rcv_queue'].popleft()
        reg['blocked'] = 0
        return 1
    else:
        reg['blocked'] += 1
        return 0


class Day18(puzzle.Puzzle):
    year = '2017'
    day = '18'

    def get_data(self):
        data = self.input_data
        return [tuple(y.split(' ')) for y in data.splitlines()]

    def part1(self):
        data = self.get_data()

        registers = {chr(a): 0 for a in range(ord('a'), ord('z') + 1)}
        registers['freq'] = 0

        last_recovered_frequency = 0
        i = 0
        while -1 < i < len(data):
            old_i = i
            instruction = instructions[data[i][0]]
            i += instruction(registers, data[i][1:])
            if data[old_i][0] == 'rcv':
                if registers[data[old_i][1]] != 0:
                    last_recovered_frequency = registers[data[old_i][1]]
                    break

        return last_recovered_frequency

    def part2(self):
        data = self.get_data()

        registers0 = {chr(a): 0 for a in range(ord('a'), ord('z') + 1)}
        registers1 = {chr(a): 0 for a in range(ord('a'), ord('z') + 1)}

        registers0['p'] = 0
        registers1['p'] = 1

        registers0['next_instruction'] = 0
        registers1['next_instruction'] = 0

        registers0['blocked'] = 0
        registers1['blocked'] = 0

        registers0['terminated'] = False
        registers1['terminated'] = False

        registers0['snd_queue'] = deque()
        registers1['snd_queue'] = deque()

        registers0['rcv_queue'] = registers1['snd_queue']
        registers1['rcv_queue'] = registers0['snd_queue']

        registers0['snd_count'] = 0
        registers1['snd_count'] = 0

        instructions['snd'] = new_snd
        instructions['rcv'] = new_rcv

        while not registers0['terminated'] and not registers1['terminated']:
            if registers0['blocked'] > 2 and registers1['blocked'] > 2:
                break
            run_process(registers0, data, instructions)
            run_process(registers1, data, instructions)

        return registers1['snd_count']

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
