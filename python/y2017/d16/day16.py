from lib import puzzle


def spin(move, programs):
    num = int(move[1:])
    for _ in range(num):
        programs.insert(0, programs.pop())


def exchange(move, programs):
    a, b = [int(x) for x in move[1:].split('/')]
    programs[a], programs[b] = programs[b], programs[a]


def partner(move, programs):
    a, b = move[1:].split('/')
    a, b = programs.index(a), programs.index(b)
    programs[a], programs[b] = programs[b], programs[a]


MOVE_TABLE = {
    's': spin,
    'x': exchange,
    'p': partner,
}


class Day16(puzzle.Puzzle):
    year = '2017'
    day = '16'

    def get_data(self):
        return [x.strip('\n') for x in self.input_data.strip().split(',')]

    def part1(self):
        moves = self.get_data()
        programs = [chr(x) for x in range(ord('a'), ord('p') + 1)]

        for move in moves:
            MOVE_TABLE[move[0]](move, programs)

        return ''.join(programs)

    def part2(self):
        moves = self.get_data()

        programs = [chr(x) for x in range(ord('a'), ord('p') + 1)]
        start_programs = list(programs)

        for move in moves:
            MOVE_TABLE[move[0]](move, programs)

        i = 1
        dance_iterations = [''.join(start_programs), ''.join(programs)]
        for i in range(2, 1000000000):
            for move in moves:
                MOVE_TABLE[move[0]](move, programs)
            dance_iterations.append(''.join(programs))
            if start_programs == programs:
                break
        return dance_iterations[1000000000 % (i)]

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
