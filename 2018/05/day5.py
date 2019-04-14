from collections import deque


def react(polymer: str) -> str:
    d = deque(polymer)
    d.append('_')  # don't react start and end
    old_len = len(d) + 1

    # React until there is no change
    while old_len != len(d):
        i = 0
        old_len = len(d)
        while i < len(d):
            x = d.popleft()
            y = d.popleft()

            if x.upper() == y.upper() and ((x.isupper() and y.islower()) or (x.islower() and y.isupper())):
                # Reaction!
                continue

            # No reaction, put the units back and rotate
            d.append(x)
            d.appendleft(y)
            i += 1
        assert d[-1] == '_'

    assert d[-1] == '_'
    d.pop()
    return ''.join(d)


def main():
    with open('input5.txt') as f:
        unreacted_polymer = f.read().strip()

    polymer = react(unreacted_polymer)
    print(f'Day 5 Part 1 Answer: {len(polymer)}')

    polymer_lengths: [str] = []
    # for each polymer unit type
    for unit_type in set(polymer.upper()):
        # Create a shortened polymer with that unit type removed
        shortened_polymer = polymer \
            .replace(unit_type.upper(), '') \
            .replace(unit_type.lower(), '')

        # React the shortened polymer
        reacted_polymer = react(shortened_polymer)
        polymer_lengths.append(len(reacted_polymer))

    # The answer is the shortest polymer
    print(f'Day 5 Part 2 Answer {min(polymer_lengths)}')


if __name__ == '__main__':
    main()
