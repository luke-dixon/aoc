from lib import puzzle


def new_deck(n=10):
    return list(range(n))


def deal_into_new_stack(deck):
    return list(reversed(deck))


def deal_with_increment(deck, increment):
    table = [None] * len(deck)
    for i, n in enumerate(range(len(deck))):
        n = n * increment % len(deck)
        table[n] = deck[i]

    new_deck = []
    for i in range(len(deck)):
        new_deck.append(table.pop())
    return list(reversed(new_deck))


def cut(deck, n):
    return deck[n % len(deck):] + deck[:n % len(deck)]


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


class Day22(puzzle.Puzzle):
    year = '2019'
    day = '22'

    def add_additional_args(self, parser):
        parser.add_argument('-d', '--draw', action='store_true')

    def get_data(self):
        data = self.input_data
        return data.splitlines()

    def part1(self):
        """
        My original solution for part 1.
        """

        deck = new_deck(n=10007)

        for technique in self.get_data():
            #print(technique, deck[:15])
            assert None not in deck, f'{deck.index(None)}, {deck[:20]}'
            if technique.startswith('deal with increment'):
                deck = deal_with_increment(deck, int(technique.split(' ')[-1]))
            elif technique.startswith('deal into new stack'):
                deck = deal_into_new_stack(deck)
            elif technique.startswith('cut'):
                deck = cut(deck, int(technique.split(' ')[-1]))
            else:
                assert False, 'bad operation'
        return deck.index(2019)

    def part1a(self):
        """
        Alternative approach for part 1 while trying to figure out part 2.
        """
        num_cards = 10007
        position = 2019

        for technique in self.get_data():
            if technique.startswith('deal with increment'):
                n = int(technique.split(' ')[-1])
                position = (position * n) % num_cards
            elif technique.startswith('deal into new stack'):
                position = (num_cards - position - 1) % num_cards
            elif technique.startswith('cut'):
                n = int(technique.split(' ')[-1])
                position = (position - n) % num_cards
            else:
                assert False, 'bad operation'
        return position

    def part1b(self):
        """
        Alternative approach for reverse of part 1 while trying to figure out part 2.
        """
        num_cards = 10007
        position = 4684

        for technique in reversed(self.get_data()):
            if technique.startswith('deal with increment'):
                n = int(technique.split(' ')[-1])
                while position % n != 0:
                    position += num_cards
                position = (position // n) % num_cards
            elif technique.startswith('deal into new stack'):
                position = (num_cards - position - 1) % num_cards
            elif technique.startswith('cut'):
                n = int(technique.split(' ')[-1])
                position = (position + n) % num_cards
            else:
                assert False, 'bad operation'
        return position

    def part1c(self):
        """
        My solution for part 1 using formula simplified with wxMaxima.

        Specific to my solution. Used to test I was along the right tracks for part 2.
        """
        num_cards = 10007

        def f(p):
            return (2284 * p + 6515) % num_cards

        return f(2019)

    def part1d(self):
        """
        My input from my answer for part 1 using formula simplified with wxMaxima.

        Specific to my solution. Used to test I was along the right tracks for part 2.
        """
        num_cards = 10007

        def g1(p):
            return ((p * pow(2284, -1, mod=10007)) + 2052) % 10007

        return g1(4684)

    def part2(self):
        num_cards = 119315717514047
        #position = 2020
        position = 2

        last_last_prime = None
        last_prime = None

        difference = set()
        last_difference = set()
        quotient = set()

        seen = {}

        for i in range(101741582076661):
            last_position = position
            for technique in reversed(self.get_data()):
                if technique.startswith('deal with increment'):
                    # 0 -> 0n % num_cards
                    # 1 -> 1n % num_cards
                    # 2 -> 2n % num_cards
                    n = int(technique.split(' ')[-1])
                    while position % n != 0:
                        position += num_cards
                    position = (position // n) % num_cards
                elif technique.startswith('deal into new stack'):
                    position = (num_cards - position) % num_cards - 1
                elif technique.startswith('cut'):
                    n = int(technique.split(' ')[-1])
                    position = (position + n) % num_cards
                else:
                    assert False, 'bad operation'

            if i % 100000 == 0:
                print(i, position)

        print(position)
        return position

    def part2b(self):
        num_cards = 119315717514047
        #num_cards = 10007
        position = 2020

        ops = []

        eq = 'p'

        for technique in self.get_data():
            if technique.startswith('deal with increment'):
                n = int(technique.split(' ')[-1])
                eq = f'(({eq}) * ({n}))'
            elif technique.startswith('deal into new stack'):
                ops.append((lambda x:
                            (num_cards - x[0] - 1) % num_cards, None))
                eq = f'({num_cards - 1} - {eq})'
            elif technique.startswith('cut'):
                n = int(technique.split(' ')[-1])
                ops.append((lambda x:
                            (x[0] - x[1]) % num_cards % num_cards, n))
                eq = f'({eq} - {n})'
            else:
                assert False, 'bad operation'

        # I took this output, and used wxMaxima to simplify and create the following functions by composing repeatedly.
        print(eq)

        def f(p):
            return (8067652995194 * p - 28645419503799) % num_cards

        def f2(p):
            return f(f(p)) % num_cards

        def f4(p):
            return f2(f2(p)) % num_cards

        def g(y):
            #return ((y * pow(8067652995194, -1, mod=num_cards)) - 59489326454439) % num_cards
            return (108721284778132 * y - 59489326450401) % num_cards

        def g2(y):
            return (57770078449189 * y - 56203125384996) % num_cards

        def g4(y):
            return (77343286961144 * y - 59793844553618) % num_cards

        def g16(y):
            return (53188999717402 * y - 55315747338937) % num_cards

        def g64(y):
            return (6659566288070 * y - 118192907204790) % num_cards

        def g256(y):
            return (12461300137083 * y - 66371857417689) % num_cards

        def g1024(y):
            return (40517277852428 * y - 86816157576063) % num_cards

        def g4096(y):
            return (27420063948637 * y - 79204553578026) % num_cards

        def g16384(y):
            return (27153229543766 * y - 68599087597574) % num_cards

        def g65536(y):
            return (73240519273788 * y - 98541109502291) % num_cards

        def g262144(y):
            return (80917406506305 * y - 114130051454407) % num_cards

        def g1048576(y):
            return (113976075592687 * y - 87665663251355) % num_cards

        def g16777216(y):
            return (68478505572738 * y - 50894692926032) % num_cards

        def g1073741824(y):
            return (44970788150205 * y - 41702139604081) % num_cards

        total = 101741582076661
        while total:
            if total - 1073741824 >= 0:
                position = g1073741824(position)
                total -= 1073741824
            elif total - 16777216 >= 0:
                position = g16777216(position)
                total -= 16777216
            elif total - 1048576 >= 0:
                position = g1048576(position)
                total -= 1048576
            elif total - 262144 >= 0:
                position = g262144(position)
                total -= 262144
            elif total - 65536 >= 0:
                position = g65536(position)
                total -= 65536
            elif total - 16384 >= 0:
                position = g16384(position)
                total -= 16384
            elif total - 4096 >= 0:
                position = g4096(position)
                total -= 4096
            elif total - 1024 >= 0:
                position = g1024(position)
                total -= 1024
            elif total - 256 >= 0:
                position = g256(position)
                total -= 256
            if total - 64 >= 0:
                position = g64(position)
                total -= 64
            elif total - 16 >= 0:
                position = g16(position)
                total -= 16
            elif total - 4 >= 0:
                position = g4(position)
                total -= 4
            elif total - 2 >= 0:
                position = g2(position)
                total -= 2
            elif total - 1 >= 0:
                position = g(position)
                total -= 1
            else:
                break
            #position = (17152310001364*position-8267020732004) % num_cards
            #print(total, position)

        #print(position)
        return position

    def main(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 1 Answer: {self.part1a()}')
        print(f'Part 1 Input: {self.part1b()}')
        print(f'Specific Part 1 Answer: {self.part1c()}')
        print(f'Part 1 Input: {self.part1d()}')
        #print(f'Part 2 Answer: {self.part2()}')
        print(f'Part 2 Answer: {self.part2b()}')
