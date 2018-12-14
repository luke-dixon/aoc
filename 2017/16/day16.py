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



with open('input16.txt') as f:
    moves = [x.strip('\n') for x in f.read().strip().split(',')]

programs = [chr(x) for x in range(ord('a'), ord('p') + 1)]
start_programs = list(programs)


move_lookup = {
    's': spin,
    'x': exchange,
    'p': partner,
}


for move in moves:
    move_lookup[move[0]](move, programs)

print('Day 16 Answer 1: ', end='')
print(''.join(programs))

i = 1
dance_iterations = [''.join(start_programs), ''.join(programs)]
for i in range(2, 1000000000):
    for move in moves:
        move_lookup[move[0]](move, programs)
    dance_iterations.append(''.join(programs))
    if start_programs == programs:
        break

print('Day 16 Answer 2: ', end='')
print(dance_iterations[(1000000000) % (i)])
