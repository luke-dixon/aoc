from collections import *

import re

from lib import puzzle


class Day19(puzzle.Puzzle):
    year = '2020'
    day = '19'

    def get_data(self):
        orig_data = self.input_data.splitlines()
        data = orig_data

        rules = {}
        received_messages = []

        blank_line_seen = False
        for line in data:
            if line == '':
                blank_line_seen = True
            if blank_line_seen:
                received_messages.append(line)
            else:
                rules[int(line.split(': ')[0])] = tuple(line.split(': ')[1].split(' '))

        new_rules = {}
        for rule in rules:
            rule_body = [[]]
            i = 0
            for c in rules[rule]:
                try:
                    x = int(c)
                    rule_body[i].append(x)
                except ValueError:
                    if c == '|':
                        i += 1
                        rule_body.append([])
                    else:
                        rule_body[i].append(c)
            new_rules[rule] = tuple(rule_body)

        rules = new_rules

        return rules, received_messages

    def part1(self):
        rules, received_messages = self.get_data()

        regex = ""
        stack = deque()
        stack.append(0)
        while stack:
            rule = stack.popleft()

            if isinstance(rule, str):
                regex += rule.strip('"')
            else:
                rule = rules[rule]

                regex_parts = []
                for i, l in enumerate(rule):
                    if i == 0:
                        regex_parts.append('(?:')
                    for next_rule in l:
                        regex_parts.append(next_rule)
                    if i < len(rule) - 1:
                        regex_parts.append('|')
                    else:
                        regex_parts.append(')')
                assert regex_parts[0] == '(?:'
                assert regex_parts[-1] == ')'
                if len(regex_parts) == 3:
                    stack.appendleft(regex_parts[1])
                else:
                    for part in reversed(regex_parts):
                        stack.appendleft(part)
            c = Counter(regex)
            c.update(stack)

        regex = '^' + regex + '$'
        regex = re.compile(regex)

        valid_messages = []
        for message in received_messages:
            if regex.match(message):
                valid_messages.append(message)

        for valid_message in valid_messages:
            print(valid_message.replace('a', ' ').replace('b', '#'))

        return len(valid_messages)

    def part2(self):
        rules, received_messages = self.get_data()

        rules[8] = tuple([[42], [42, 8]])
        rules[11] = tuple([[42, 31], [42, 11, 31]])

        max_message_len = max([len(x) for x in received_messages])

        regex = ""
        stack = deque()
        stack.append(0)
        while stack:
            rule = stack.popleft()

            if isinstance(rule, str):
                regex += rule.strip('"')
            else:
                if rule == 8:
                    # ([42], [42, 8])
                    regex_parts = [
                        '(?:',
                        42,
                        '|',
                        42,
                        '+',
                        ')'
                    ]
                    assert regex_parts[0] == '(?:'
                    assert regex_parts[-1] == ')'
                    for part in reversed(regex_parts):
                        stack.appendleft(part)
                elif rule == 11:
                    # ([42, 31], [42, 11, 31])
                    regex_parts = ['(?:', 42, 31]
                    for i in range(2, max_message_len):
                        regex_parts.extend(['|', 42, f'{{{i}}}', 31, f'{{{i}}}'])

                    regex_parts.append(')')

                    assert regex_parts[0] == '(?:'
                    assert regex_parts[-1] == ')'
                    for part in reversed(regex_parts):
                        stack.appendleft(part)
                else:
                    rule = rules[rule]

                    regex_parts = []
                    for i, l in enumerate(rule):
                        if i == 0:
                            regex_parts.append('(?:')
                        for next_rule in l:
                            regex_parts.append(next_rule)
                        if i < len(rule) - 1:
                            regex_parts.append('|')
                        else:
                            regex_parts.append(')')
                    assert regex_parts[0] == '(?:'
                    assert regex_parts[-1] == ')'
                    if len(regex_parts) == 3:
                        stack.appendleft(regex_parts[1])
                    else:
                        for part in reversed(regex_parts):
                            stack.appendleft(part)

        regex = '^' + regex + '$'
        regex = re.compile(regex)

        valid_messages = []
        for message in received_messages:
            if regex.match(message):
                valid_messages.append(message)

        for valid_message in valid_messages:
            print(valid_message.replace('a', '#').replace('b', ' '))

        return len(valid_messages)

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
