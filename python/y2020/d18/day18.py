from collections import deque

from lib import puzzle


class Day18(puzzle.Puzzle):
    year = '2020'
    day = '18'

    def get_data(self):
        orig_data = self.input_data.splitlines()
        data = orig_data

        #data = ['1 + 2 * 3 + 4 * 5 + 6', '1 + (2 * 3) + (4 * (5 + 6))', '2 * 3 + (4 * 5)', '5 + (8 * 3 + 9 + 3 * 4 * 3)', '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2']

        return data

    def part1(self):
        data = self.get_data()

        operators = {'+', '*'}
        brackets = {'(', ')'}

        answer = 0

        for line in data:
            line = ''.join(line.split(' '))
            queue = deque()

            i = 0
            while i < len(line):
                number = ''
                while i < len(line) and '0' <= line[i] <= '9':
                    number += line[i]
                    i += 1
                if number:
                    queue.append(int(number))
                elif i < len(line) and line[i] in operators:
                    queue.append(line[i])
                    i += 1
                elif i < len(line) and line[i] in brackets:
                    queue.append(line[i])
                    i += 1
                else:
                    i += 1

            def find_inner_most_bracket(line):
                pos, pos_end, level, max_level = -1, len(line), 0, 0
                for i, c in enumerate(line):
                    if c == '(':
                        level += 1
                        max_level = max(max_level, level)
                        if level == max_level:
                            pos = i
                    elif c == ')':
                        if level == max_level:
                            pos_end = i
                        level -= 1
                return pos, pos_end

            while '(' in queue or '*' in queue or '+' in queue:
                pos, pos_end = find_inner_most_bracket(queue)
                if True:
                    i = pos + 1
                    total = queue[i]
                    i += 1
                    while i < pos_end:
                        if queue[i] == '*':
                            total *= queue[i + 1]
                            i += 2
                        elif queue[i] == '+':
                            total += queue[i + 1]
                            i += 2
                        else:
                            assert False, f'{i}, {queue[i]}, {list(queue)}, {pos}:{pos_end}'
                    new_queue = deque()
                    i = 0
                    while i < pos:
                        new_queue.append(queue[i])
                        i += 1
                    new_queue.append(total)
                    i = pos_end + 1
                    while i < len(queue):
                        new_queue.append(queue[i])
                        i += 1

                    queue = new_queue

            answer += queue[0]

        return answer

    def part2(self):
        data = self.get_data()

        operators = {'+', '*'}
        brackets = {'(', ')'}

        answer = 0

        for line in data:
            line = ''.join(line.split(' '))
            queue = deque()

            i = 0
            while i < len(line):
                number = ''
                while i < len(line) and '0' <= line[i] <= '9':
                    number += line[i]
                    i += 1
                if number:
                    queue.append(int(number))
                elif i < len(line) and line[i] in operators:
                    queue.append(line[i])
                    i += 1
                elif i < len(line) and line[i] in brackets:
                    queue.append(line[i])
                    i += 1
                else:
                    i += 1

            def find_inner_most_bracket(line):
                pos, pos_end, level, max_level = -1, len(line), 0, 0
                for i, c in enumerate(line):
                    if c == '(':
                        level += 1
                        max_level = max(max_level, level)
                        if level == max_level:
                            pos = i
                    elif c == ')':
                        if level == max_level:
                            pos_end = i
                        level -= 1
                return pos, pos_end

            while '(' in queue or '*' in queue or '+' in queue:
                pos, pos_end = find_inner_most_bracket(queue)
                if True:
                    while '+' in list(queue)[pos + 1:pos_end]:
                        j = pos + 1
                        while j < pos_end:
                            if queue[j] == '+':
                                total = queue[j - 1] + queue[j + 1]
                                new_queue = deque()
                                i = 0
                                while i < j - 1:
                                    new_queue.append(queue[i])
                                    i += 1
                                new_queue.append(total)
                                i = j + 2
                                while i < len(queue):
                                    new_queue.append(queue[i])
                                    i += 1

                                queue = new_queue

                                pos_end -= 2
                            j += 1

                    while '*' in list(queue)[pos + 1:pos_end]:
                        # find first '*'
                        j = pos + 1
                        while j < pos_end:
                            if queue[j] == '*':
                                product = queue[j - 1] * queue[j + 1]
                                new_queue = deque()
                                i = 0
                                while i < j - 1:
                                    new_queue.append(queue[i])
                                    i += 1
                                new_queue.append(product)
                                i = j + 2
                                while i < len(queue):
                                    new_queue.append(queue[i])
                                    i += 1

                                queue = new_queue

                                pos_end -= 2
                            j += 1

                    total = queue[pos + 1]

                    new_queue = deque()
                    i = 0
                    while i < pos:
                        new_queue.append(queue[i])
                        i += 1
                    new_queue.append(total)
                    i = pos_end + 1
                    while i < len(queue):
                        new_queue.append(queue[i])
                        i += 1

                    queue = new_queue

            answer += queue[0]

        return answer

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
