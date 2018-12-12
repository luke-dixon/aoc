# 2018 Day 12

def calculate_totals(totals, state, zero_index=0):
    total = 0
    for i, pot in enumerate(state[zero_index:]):
        if pot == '#':
            total += i
    for i, pot in enumerate(state[zero_index - 1:0:-1]):
        if pot == '#':
            total -= i
    totals.append(total)


def expand_pots(state, zero_index):
    if '#' in state[:6]:
        for i in range(30):
            state.insert(0, '.')
            zero_index += 1
    if '#' in state[-6:]:
        for i in range(30):
            state.append('.')
    return zero_index


def run_next_generation(state, rules, generation, do_print=False):
    new_line = ['.'] * len(state)
    for i in range(2, len(state) - 2):
        rule = rules.get(''.join([state[i - 2], state[i - 1], state[i], state[(i + 1)],
                                  state[(i + 2)]]), '.')

        new_line[i] = rule
    if do_print:
        gen_line = ''.join(new_line)
        print(f'{generation + 1}: {gen_line}')
    state = new_line
    return state


# Read in the data
with open('input12.txt') as f:
    data = [d.strip('\n') for d in f.readlines()]

# Extract the starting state
initial_state = [d.strip('\n') for d in data.pop(0)[len('initial state: '):].strip('\n')]

data.pop(0)

rules = {}
for d in data:
    rule, result = d.split(' => ')
    rules[rule] = result

# Give ourselves a few extra pots each side
pot_0_index = expand_pots(initial_state, 0)

# Set up the totals, need to keep track of these
totals = []
calculate_totals(totals, initial_state, pot_0_index)

# Print out the initial state
initial_line = ''.join(initial_state)
print(f'0: {initial_line}')

# Run 20 generations for Answer 1
state = initial_state
for gen in range(20):
    state = run_next_generation(state, rules, gen, do_print=True)
    pot_0_index = expand_pots(state, pot_0_index)
    calculate_totals(totals, state, pot_0_index)

print(f'Day 12 part 1 answer: {totals[-1]}')


# After a while the rate of change becomes steady.
# For me that meant it was increasing by 109 each iteration.
# (50000000000 - 1000) * 109 + totals[1000]

num_generations_until_today = 50000000000

# Guess it has stabilised after we see it grow the same amount 10 times
# There's got to be a better way than this to work out growth has stabilised
max_same_growth = 10
same_growth = 0

# Run up to the required amount of generations
rate_of_change = totals[-1] - totals[-2]
gen = 20
for gen in range(gen, num_generations_until_today):
    state = run_next_generation(state, rules, gen)
    pot_0_index = expand_pots(state, pot_0_index)
    calculate_totals(totals, state, pot_0_index)

    # Check if the rate of change has stabilised
    old_rate_of_change = rate_of_change
    rate_of_change = totals[-1] - totals[-2]
    if old_rate_of_change == rate_of_change:
        same_growth += 1
    else:
        same_growth = 0
    if same_growth > max_same_growth:
        break

part2_answer = (num_generations_until_today - gen) * rate_of_change + totals[gen]
print(f'Day 12 part 2 answer: {part2_answer}')
