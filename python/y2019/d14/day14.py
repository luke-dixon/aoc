from collections import deque

from .. import puzzle


class Day14(puzzle.Puzzle):
    year = '2019'
    day = '14'

    def get_data(self):
        orig_data = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''
        orig_data = self.input_data
        data = orig_data.splitlines()
        return data

    def part1(self):
        data = [x.split(' => ') for x in self.get_data()]
        ingredient_qty = {}
        ingredients = {}
        for d in data:
            qty, name = d[-1].split(' ')
            assert (name, int(qty)) not in ingredient_qty
            ingredient_qty[(name, int(qty))] = []
            ingredients[name] = int(qty)
            x = d[:-1][0]
            for i in x.split(', '):
                i_qty, i_name = i.split(' ')
                ingredient_qty[(name, int(qty))].append((i_name, int(i_qty)))

        total_ore_required = 0

        have = {}
        for ingredient in ingredients:
            have[ingredient] = 0
        assert 'ORE' not in have
        have['ORE'] = 0

        required = {}
        for ingredient in ingredients:
            required[ingredient] = 0
        required['FUEL'] = 1

        left_overs = {}

        stack = []
        processesd = {}
        stack.append(('FUEL', 1, None))

        required = {}

        while stack:
            name, qty, produces = stack.pop()
            assert qty > 0

            if name not in required:
                required[name] = 0
            required[name] += qty

            if name == 'ORE':
                total_ore_required += qty
                print(f'{qty} ORE -> {produces}')
                continue

            if name in left_overs:
                if qty >= left_overs[name]:
                    qty -= left_overs[name]
                    del left_overs[name]
                    assert qty >= 0
                elif qty < left_overs[name]:
                    left_overs[name] -= qty
                    qty = 0

            assert qty >= 0

            if not qty:
                continue

            assert qty > 0

            qty_required = ingredients[name]

            batches_required = 1
            while (qty_required * batches_required) < qty:
                batches_required += 1
            for i_name, i_qty in reversed(ingredient_qty[(name, qty_required)]):
                stack.append((i_name, i_qty * batches_required, name))
            if (qty_required * batches_required) > qty:
                left_overs[name] = (qty_required * batches_required) - qty

            processesd[(name, qty)] = (qty_required * batches_required) - qty

        print(f'processed: {processesd}')
        print(f'total ore required {total_ore_required}')
        print(f'left over: {left_overs}')
        print(f'required: {required}')
        return total_ore_required

    def part2(self):

        left_overs_empty = False  # False initially to get the loop to run
        count = 0
        left_overs = {}
        left_overs_set = set()

        totals = []
        max_total = 0

        data = [x.split(' => ') for x in self.get_data()]
        ingredient_qty = {}
        ingredients = {}
        for d in data:
            qty, name = d[-1].split(' ')
            assert (name, int(qty)) not in ingredient_qty
            ingredient_qty[(name, int(qty))] = []
            ingredients[name] = int(qty)
            x = d[:-1][0]
            for i in x.split(', '):
                i_qty, i_name = i.split(' ')
                ingredient_qty[(name, int(qty))].append((i_name, int(i_qty)))

        required = {}

        processesd = {}

        while not left_overs_empty:
            r = int(1000000000000 // (max(sum(totals), 1) / max(count, 1)))
            if count > 0 and r > max_total:
                max_total = r
                print(max_total)

            total_ore_required = 0

            stack_qty = {'FUEL': 1}
            stack = deque(['FUEL'])

            while stack:
                name = stack.popleft()
                qty = stack_qty[name]
                del stack_qty[name]

                if name == 'ORE':
                    total_ore_required += qty
                    continue

                if count == 0:
                    if name not in required:
                        required[name] = 0
                    required[name] += qty

                if name in left_overs:
                    if qty >= left_overs[name]:
                        qty -= left_overs[name]
                        del left_overs[name]
                    elif qty < left_overs[name]:
                        left_overs[name] -= qty
                        qty = 0

                if not qty:
                    continue

                qty_required = ingredients[name]

                batches_required = 1
                while (qty_required * batches_required) < qty:
                    batches_required += 1
                for i_name, i_qty in reversed(ingredient_qty[(name, qty_required)]):
                    if i_name in stack_qty:
                        stack_qty[i_name] += i_qty * batches_required
                    else:
                        stack.append(i_name)
                        stack_qty[i_name] = i_qty * batches_required
                if (qty_required * batches_required) > qty:
                    left_overs[name] = (qty_required * batches_required) - qty

                processesd[(name, qty)] = (qty_required * batches_required) - qty

            totals.append(total_ore_required)
            count += 1
            if str({x: left_overs[x] for x in sorted(left_overs)}) in left_overs_set:
                break
            left_overs_set.add(str({x: left_overs[x] for x in sorted(left_overs)}))
            if len(left_overs) == 0:
                left_overs_empty = True

        print(sum(totals))
        print(left_overs)
        print(count)
        print(sum(totals) / count)
        print(1000000000000 / (sum(totals) / count))
        return int(1000000000000 // (sum(totals) / count))

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
