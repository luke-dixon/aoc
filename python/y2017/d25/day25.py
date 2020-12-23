from collections import Counter

from lib import puzzle


def run_machine_until_checksum(states, checksum_after, starting_state):
    tape = []
    current_pos = 0
    current_state = starting_state

    for _ in range(checksum_after):
        state = states[current_state]
        if current_pos < 0:
            tape.insert(0, 0)
            current_pos += 1
        try:
            current_value = tape[current_pos]
        except IndexError:
            current_len = len(tape)
            if current_pos < 0:
                tape.insert(0, 0)
                current_pos += 1
            else:
                tape.append(0)
            assert current_pos >= 0
            assert len(tape) == current_len + 1
            current_value = tape[current_pos]
            assert current_value == 0
        marker_required = current_value == -1
        next_value, move, next_state = state[current_value]
        try:
            tape[current_pos] = next_value
        except IndexError:
            current_len = len(tape)
            if current_pos < 0:
                tape.insert(0, 0)
                current_pos += 1
            else:
                tape.append(0)
            assert len(tape) == current_len + 1
            tape[current_pos] = next_value
        if move < 0:
            current_pos -= 1
        if move > 0:
            current_pos += 1
        current_state = next_state
        assert current_pos >= -1

    c = Counter(tape)
    return c[1]



class Day25(puzzle.Puzzle):
    year = '2017'
    day = '25'

    def get_data(self):
        data = self.input_data
        return data.splitlines()

    def part1(self):
        data = self.get_data()
        starting_state = data.pop(0)[len('Begin in state ')]
        checksum_after = int(data.pop(0)[len('Perform a diagnostic checksum after '):-len(' steps.')])

        def create_new_state(states, data):
            state = data.pop(0)[len('In state ')]
            states[state] = {}
            while len(data) and data[0] != '':
                current_value = int(data.pop(0)[len('  If the current value is ')])
                next_value = int(data.pop(0)[len('    - Write the value ')])
                move = data.pop(0)[len('    - Move one slot to the ')]
                if move == 'r':
                    move = 1
                if move == 'l':
                    move = -1
                next_state = data.pop(0)[len('    - Continue with state ')]
                states[state][current_value] = (next_value, move, next_state)

        states = {}

        while len(data):
            d = data.pop(0)
            if d == '':
                create_new_state(states, data)
            while len(data) and data[0] != '':
                data.pop(0)

        return run_machine_until_checksum(states, checksum_after, starting_state)

    def part2(self):
        return 'Collect more stars first'

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
