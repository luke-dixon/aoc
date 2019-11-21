def part1_update_strategy(instruction_value):
    return instruction_value + 1


def part2_update_strategy(instruction_value):
    return instruction_value - 1 if instruction_value >= 3 else instruction_value + 1


def run(data, update_strategy):
    next_instruction, steps = 0, 0
    try:
        while True:
            instruction_value = data[next_instruction]
            data[next_instruction] = update_strategy(instruction_value)
            next_instruction, steps = next_instruction + instruction_value, steps + 1
    except IndexError:
        return steps


def main():
    with open('input5.txt') as f:
        data = [int(n) for n in f.read().splitlines()]

    print('Day 5 part 1 Answer: {0}'.format(run(list(data), part1_update_strategy)))
    print('Day 5 part 2 Answer: {0}'.format(run(list(data), part2_update_strategy)))
    

if __name__ == "__main__":
    main()
