import re


# Rounds with no kills before we decide it is a stalemate
STALEMATE_ROUNDS = 5


class Army:
    def __init__(self, line):
        self.name = line.rstrip(':')
        self.groups = []

    def __repr__(self):
        return f'Army(\'{self.name}\')'


class Group:
    stage = 'target selection'

    def __init__(self, line):
        self.line = line
        m = re.search(r'(\d+) units each with (\d+) hit points \((.*)\) with an attack that does (\d+) (\w+) damage at initiative (\d+)', line)
        if m:
            self.units = int(m.group(1))
            self.hitpoints = int(m.group(2))
            self.attack = int(m.group(4))
            self.attack_type = m.group(5)
            self.initiative = int(m.group(6))
            self.immune_to = []
            self.weak_to = []
            for attr in m.group(3).split('; '):
                if 'weak to ' in attr:
                    self.weak_to = attr.lstrip('weak to ').split(', ')
                if 'immune to ' in attr:
                    self.immune_to = attr.lstrip('immune to ').split(', ')
        else:
            m = re.search(
                r'(\d+) units each with (\d+) hit points with an attack that does (\d+) (\w+) damage at initiative (\d+)',
                line)
            if m:
                self.units = int(m.group(1))
                self.hitpoints = int(m.group(2))
                self.attack = int(m.group(3))
                self.attack_type = m.group(4)
                self.initiative = int(m.group(5))
                self.immune_to = []
                self.weak_to = []
            else:
                print(line)
                assert False

    @property
    def effective_power(self):
        return self.units * self.attack

    def calculate_damage(self, other: 'Group'):
        if self.attack_type in other.immune_to:
            return 0
        if self.attack_type in other.weak_to:
            return 2 * self.effective_power
        return self.effective_power


    def select_target(self, targets: ['Group']):
        try:
            max_damage_target: Group = targets[0]
            max_damage: int = self.calculate_damage(targets[0])
        except IndexError:
            return None, None
        for target in targets[1:]:
            damage = self.calculate_damage(target)
            if damage == max_damage:
                if target.effective_power == max_damage_target.effective_power:
                    if target.initiative > max_damage_target.initiative:
                        max_damage_target = target
                        max_damage = damage
                        continue
                    assert target.initiative < max_damage_target.initiative
                    continue
                if target.effective_power > max_damage_target.effective_power:
                    max_damage_target = target
                    max_damage = damage
                    continue
                assert target.effective_power < max_damage_target.effective_power
                continue
            if damage > max_damage:
                max_damage_target = target
                max_damage = damage
                continue
            assert damage < max_damage

        if max_damage <= 0:
            return None, None
        targets.remove(max_damage_target)
        return max_damage_target, max_damage

    def apply_damage(self, other: 'Group', damage: int):
        if self.units <= 0:
            return
        while damage >= other.hitpoints:
            other.units -= 1
            damage -= other.hitpoints

    def __repr__(self):
        return f'Group(units={self.units}, hitpoints={self.hitpoints}, attack={self.attack})'

    def __lt__(self, other):
        if self.stage == 'target selection':
            if self.effective_power == other.effective_power:
                return self.initiative < other.initiative
            return self.effective_power < other.effective_power
        elif self.stage == 'attacking':
            return self.initiative < other.initiative


def run(boost=0):
    with open('input24.txt') as f:
        data = f.read().splitlines()

    armies = []
    for i, line in enumerate(data):
        if line in ['Immune System:', 'Infection:']:
            armies.append(Army(line))
        if 'units' in line:
            armies[-1].groups.append(Group(data[i]))
            #armies[-1].groups.append(Group(''.join([data[i], data[i + 1]])))

    for group in armies[0].groups:
        group.attack += boost

    stalemate_check = STALEMATE_ROUNDS

    while len(armies[0].groups) and len(armies[1].groups):
        Group.stage = 'target selection'
        targets = {}

        for army in armies:
            for group in army.groups:
                assert group.units > 0

        target_choices = list(armies[0].groups)
        for group in reversed(sorted(armies[1].groups)):
            target, damage = group.select_target(target_choices)
            if target is not None:
                targets[group] = (target, damage)

        target_choices = list(armies[1].groups)
        for group in reversed(sorted(armies[0].groups)):
            target, damage = group.select_target(target_choices)
            if target is not None:
                targets[group] = (target, damage)

        Group.stage = 'attacking'
        total_kills = 0
        for group in reversed(sorted(targets.keys())):
            target, damage = targets[group]
            if group.units <= 0:
                continue
            if group:
                start_units = target.units
                if start_units <= 0:
                    continue
                damage = group.calculate_damage(target)
                #print(f'{group} attacking {target} {damage} damage, ', end='')
                group.apply_damage(target, damage)
                total_kills += start_units - max(target.units, 0)
                #print(f'killing {start_units - max(target.units, 0)}')
        #print()

        if total_kills <= 0:
            stalemate_check -= 1
        else:
            stalemate_check = STALEMATE_ROUNDS
        if stalemate_check < 0:
            break

        for group in list(armies[0].groups):
            if group.units <= 0:
                armies[0].groups.remove(group)
        for group in list(armies[1].groups):
            if group.units <= 0:
                armies[1].groups.remove(group)

        for army in armies:
            for group in army.groups:
                assert group.units > 0

    immune_system_units_left = 0
    for group in armies[0].groups:
        immune_system_units_left += group.units

    infection_units_left = 0
    for group in armies[1].groups:
        infection_units_left += group.units

    immune_system_wins = False
    if immune_system_units_left > 0 and infection_units_left <= 0:
        immune_system_wins = True

    return immune_system_wins, immune_system_units_left + infection_units_left


def part1():
    _, units_left = run()
    print(f'Day 24 Part 1 Answer: {units_left}')

def part2():
    for boost in range(1, 100):
        print(f'boost: {boost}')
        won, units_left = run(boost)
        if won:
            break

    print(f'Day 24 Part 2 Answer: {units_left}')


def main():
    part1()
    part2()

if __name__ == '__main__':
    main()
