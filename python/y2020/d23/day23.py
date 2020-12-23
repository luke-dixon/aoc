from collections import deque

from lib import puzzle


def move(cups, cups_set):
    current_cup = cups[0]
    cups.rotate(-1)
    cup1, cup2, cup3 = cups.popleft(), cups.popleft(), cups.popleft()
    destination_cup = current_cup - 1
    while destination_cup not in cups_set - {cup1, cup2, cup3}:
        destination_cup -= 1
        if destination_cup < min(cups_set):
            destination_cup = max(cups_set)
    while cups[0] != destination_cup:
        cups.rotate(1)
    cups.rotate(-1)
    cups.appendleft(cup3)
    cups.appendleft(cup2)
    cups.appendleft(cup1)
    while current_cup != cups[0]:
        cups.rotate(-1)
    cups.rotate(-1)


class Cup:
    def __init__(self, label, prev, next):
        self.label = label
        self.prev = prev
        self.next = next

    def __repr__(self):
        return f'{self.label}'


class Day23(puzzle.Puzzle):
    year = '2020'
    day = '23'

    def get_data(self):
        data = self.input_data
        return [int(c) for c in data.splitlines()[0]]
        # return [3, 8, 9, 1, 2, 5, 4, 6, 7]

    def part1(self):
        cups = deque(self.get_data())
        cups_set = set(cups)

        for i in range(100):
            move(cups, cups_set)

        while cups[0] != 1:
            cups.rotate(-1)

        cups = list(cups)
        return ''.join(str(x) for x in cups[1:])

    def part2(self):

        # Create linked list of given cards
        head = None
        current_cup = None
        tail = None
        for cup in self.get_data():
            cup = Cup(cup, tail, None)
            if current_cup is None:
                current_cup = cup
            if head is None:
                head = cup
            if tail:
                tail.next = cup
            tail = cup

        # Add extra cards
        for i in range(10, 1000001):
            cup = Cup(i, tail, None)
            tail.next = cup
            tail = cup

        # Create a table of cards for fast lookup
        current_cup = head
        cup_lookup = {current_cup.label: current_cup}
        while current_cup.next:
            current_cup = current_cup.next
            cup_lookup[current_cup.label] = current_cup

        # Form a ring and set the current cup
        head.prev = tail
        tail.next = head
        current_cup = head

        for i in range(10000000):
            # Take next three cups out of ring
            cup1 = current_cup.next
            cup2 = cup1.next
            cup3 = cup2.next

            # Keep ring consistent
            current_cup.next = cup3.next
            cup3.next.prev = current_cup

            # Get destination
            destination = current_cup.label - 1
            while destination in {cup1.label, cup2.label, cup3.label, 0}:
                destination -= 1
                if destination < 1:
                    destination = 1000000

            # Find destination
            destination_cup = cup_lookup[destination]

            # Place cups after destination
            destination_cup.next.prev = cup3
            cup3.next = destination_cup.next
            cup1.prev = destination_cup
            destination_cup.next = cup1

            # Move to next cup
            current_cup = current_cup.next

            if i % 1000000 == 0 and i != 0:
                print(i)

        # Go to card 1
        current_cup = cup_lookup[1]

        # Answer is in next two cards
        cup1 = current_cup.next
        cup2 = cup1.next

        return cup1.label * cup2.label

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
