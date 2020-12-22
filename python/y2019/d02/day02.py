import itertools
from typing import List

from .. import intcode
from lib import puzzle


def run_intcode_computer(data):
    intcode.run_intcode_computer(
        data,
        intcode.ListInputDevice([]),
        intcode.ListOutputDevice([]),
        label='part1',
    )
    return data


def part1(data: List[int], noun: int, verb: int) -> int:
    data[1] = noun
    data[2] = verb

    data = run_intcode_computer(data)
    return data[0]


def part2(data: List[int]) -> int:
    answer = None
    for noun, verb in itertools.product(range(0, 100), range(0, 100)):
        if part1(list(data), noun, verb) == 19690720:
            answer = 100 * noun + verb
    assert answer is not None
    return answer


def expand_brackets(s):
    orig = s
    print(f'orig: {s}')

    # Remove unnecessary outer brackets
    while s[0] == '(' and s[-1] == ')':
        s = s[1:-1]

    p1 = None
    p2 = None
    op = None

    # Find op
    op = s[0]
    s = s[1:]

    # Find p1
    if s[0] == '(':
        # Find index of matching bracket
        level = 1
        i = 0
        while level > 0:
            i += 1
            if s[i] == '(':
                level += 1
            elif s[i] == ')':
                level -= 1
        p1 = s[0:i]
        print(f'p1: {p1}')
        s = s[i:]
    else:
        p1 = s[0]
        print(f'p1: {p1}')
        s = s[1:]
        print(s)

    print(p1, op, s)

    # Find p2
    if s[0] == '(':
        # Find index of matching bracket
        level = 1
        i = 0
        print(s)
        while level > 0:
            i += 1
            if s[i] == '(':
                level += 1
            elif s[i] == ')':
                level -= 1
        p2 = s[0:]
    else:
        p2 = s[0]

    if p1[0] == '(':
        p1 = expand_brackets(p1)
    if p2[0] == '(':
        p2 = expand_brackets(p2)

    return orig


def collect_terms(s):
    return s


def simplify_linear_eq(s):
    s = expand_brackets(s)
    return collect_terms(s)


def part1a(data, noun, verb):
    data[1] = 'x'
    data[2] = 'y'

    i = 0
    while True:
        op, p1, p2, r = data[i:i+4]
        if r != 3:
            break
        i += 4

    while True:
        op, p1, p2, r = data[i:i + 4]

        if op not in {1, 2}:
            break

        eq = []
        eq.append('(')
        eq.append([None, '+', '*'][op])
        eq.append(str(data[p1]))
        eq.append(str(data[p2]))
        eq.append(')')

        data[r] = ''.join(eq)

        i += 4

    print(data[0])
    data[0] = simplify_linear_eq(data[0])
    print(data[0])

    def f(noun, verb):
        #return eval(data[0].replace('x', str(noun)).replace('y', str(verb)))
        return 303750 * noun + verb + 250703

    print(f'Answer part 1a: {f(noun, verb)}')

    answer = None
    for noun, verb in itertools.product(range(0, 100), range(0, 100)):
        if f(noun, verb) == 19690720:
            answer = 100 * noun + verb
    assert answer is not None

    print(f'Answer part 2a: {answer}')


class Day02(puzzle.Puzzle):
    year = '2019'
    day = '2'

    def get_data(self) -> List[int]:
        return [int(x) for x in self.input_data.strip().split(',')]

    def run(self):
        #print(f'Answer part 1: {part1(self.get_data(), 12, 2)}')
        #print(f'Answer part 2: {part2(self.get_data())}')
        part1a(self.get_data(), 12, 2)
