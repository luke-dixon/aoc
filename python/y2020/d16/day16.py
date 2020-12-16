
from collections import *

from .. import puzzle

Rule = namedtuple('Rule', ['field', 'ranges'])


class Day16(puzzle.Puzzle):
    year = '2020'
    day = '16'

    def get_data(self):
        orig_data = self.input_data.splitlines()

        raw_rules = []
        your_ticket = None
        nearby_tickets = None
        for line in orig_data:
            if line == '':
                continue
            elif line == 'your ticket:':
                your_ticket = []
            elif line == 'nearby tickets:':
                nearby_tickets = []
            elif your_ticket is None and nearby_tickets is None:
                raw_rules.append(line)
            elif your_ticket is not None and nearby_tickets is None:
                your_ticket = [int(x) for x in line.split(',')]
            elif nearby_tickets is not None:
                nearby_tickets.append([int(x) for x in line.split(',')])

        rules = []
        for rule in raw_rules:
            field, ranges = rule.split(': ')
            ranges = ranges.split(' or ')
            ranges = [(int(range.split('-')[0]), int(range.split('-')[1])) for range in ranges]
            rules.append(Rule(field, ranges))


        return rules, your_ticket, nearby_tickets

    def part1(self):
        rules, your_ticket, nearby_tickets = self.get_data()

        invalid_fields = []
        for ticket in nearby_tickets:
            for value in ticket:
                found = False
                for rule in rules:
                    for lower, upper in rule.ranges:
                        if lower <= value <= upper:
                            found = True
                            break
                    if found:
                        break
                if found:
                    continue
                else:
                    invalid_fields.append(value)

        return sum(invalid_fields)

    def part2(self):
        rules, your_ticket, nearby_tickets = self.get_data()

        potentially_valid_tickets = []
        invalid = []
        invalid_fields = []
        for ticket in nearby_tickets:
            is_valid = True
            for value in ticket:
                found = False
                for rule in rules:
                    for lower, upper in rule.ranges:
                        if lower <= value <= upper:
                            found = True
                            break
                    if found:
                        break
                if found:
                    continue
                else:
                    invalid_fields.append(value)
                    is_valid = False
            if is_valid:
                potentially_valid_tickets.append(ticket)

        potential_rules = {}
        for i in range(len(potentially_valid_tickets[0])):
            potential_rules[i] = list(rules)

        for ticket in potentially_valid_tickets:
            for i, value in enumerate(ticket):
                new_rules = [x for x in potential_rules[i]]
                for rule in potential_rules[i]:
                    matches_rule = False
                    for lower, upper in rule.ranges:
                        if lower <= value <= upper:
                            matches_rule = True
                    if not matches_rule:
                        new_rules = [x for x in potential_rules[i] if x != rule]
                potential_rules[i] = new_rules

        while [x for x in potential_rules if len(potential_rules[x]) > 1]:
            for i in [x for x in potential_rules if len(potential_rules[x]) == 1]:
                for j in [x for x in potential_rules if len(potential_rules[x]) != 1]:
                    potential_rules[j] = [x for x in potential_rules[j] if x != potential_rules[i][0]]

        total = 1
        for idx in potential_rules:
            if potential_rules[idx][0].field.startswith('departure'):
                total *= your_ticket[idx]

        return total

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
