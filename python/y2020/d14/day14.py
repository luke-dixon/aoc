from .. import puzzle


def update_memory1(mem, line, current_mask: str):
    address = int(line[len("mem["):line.find(']')])
    value = int(line[line.find('=') + 2:])

    value |= int(current_mask.replace('X', '0'), 2)
    value &= int(current_mask.replace('X', '1'), 2)

    mem[address] = value


def update_memory2(mem, line, current_mask):
    orig_address = int(line[len("mem["):line.find(']')])
    value = int(line[line.find('=') + 2:])

    addresses = {orig_address}
    for i, b in enumerate(reversed(current_mask)):
        new_addresses = set()
        for address in addresses:
            if b == '1':
                address |= 2 ** i
                new_addresses.add(address)
            elif b == 'X':
                new_address = address | 2 ** i
                new_addresses.add(new_address)
                new_address = address & ((1 << 36) - 1) - 2 ** i
                new_addresses.add(new_address)
            elif b == '0':
                new_addresses.add(address)
            else:
                assert False
        addresses = new_addresses

    for address in addresses:
        mem[address] = value


class Day14(puzzle.Puzzle):
    year = '2020'
    day = '14'

    def get_data(self):
        return self.input_data.splitlines()

    def get_mask(self, line):
        return line[line.find('=') + 1:].strip()

    def answer(self, update_memory):
        data = self.get_data()

        mem = {}
        current_mask = 0
        for line in data:
            if line.startswith("mask"):
                current_mask = self.get_mask(line)
            elif line.startswith("mem"):
                update_memory(mem, line, current_mask)
            else:
                assert False

        return sum(mem[x] for x in mem)

    def part1(self):
        return self.answer(update_memory1)

    def part2(self):
        return self.answer(update_memory2)

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
