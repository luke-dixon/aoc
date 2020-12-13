import math
from functools import reduce
from itertools import combinations

from .. import puzzle


class Day13(puzzle.Puzzle):
    year = '2020'
    day = '13'

    def get_data(self):
        orig_data = self.input_data
        data = orig_data.splitlines()
        # data = [
        #     "939",
        #     "7,13,x,x,59,x,31,19"
        # ]
        # data = [
        #     "1",
        #     "7,13,x,x,59,x,31,19"
        # ]
        # data = [
        #     "1",
        #     "1789,37,47,1889"
        # ]
        return data

    def part1(self):
        timestamp = int(self.get_data()[0])
        bus_ids = [int(x) for x in self.get_data()[1].split(',') if x != 'x']

        possible_times = []
        for bus_id in bus_ids:
            d, r = divmod(timestamp, bus_id)
            possible_times.append((d + 1) * bus_id)

        return (min(possible_times) - timestamp) * 823

    def part2(self):
        bus_ids = [x for x in self.get_data()[1].split(',')]
        b = []
        for i, bus_id in enumerate(bus_ids):
            if bus_id != 'x':
                b.append((int(bus_id), i))

        # Use the Chinese Remainder Theorem (Thanks M303)
        modulos = [x[0] for x in b]
        a_i = [(x[0] - x[1]) % x[0] for x in b]
        for p, q in combinations(modulos, r=2):
            assert math.gcd(p, q) == 1
        print(f'a_i: {a_i}')
        print(f'modulos: {modulos}')

        # x = (a_1)*(N_1)*(x_1) + (a_2)*(N_2)*(x_2) + ...

        n = reduce(lambda x, y: x * y, modulos)
        print(f'n: {n}')

        N_i = []
        for x_i in b:
            N_i.append(reduce(lambda x, y: x * y, [x for x in modulos if x != x_i[0]]))
        print(f'N_i: {N_i}')

        x_i = []
        for i, n_i in enumerate(modulos):
            for z in range(modulos[i]):
                if ((z * N_i[i]) % modulos[i]) == 1:
                    x_i.append(z)
                    break

        print(f'x_i: {x_i}')

        total = 0
        for i in range(len(modulos)):
            total += (a_i[i] * N_i[i] * x_i[i]) % n
            total = total % n

        return total

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
