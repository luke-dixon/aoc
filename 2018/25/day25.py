def distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2]) + abs(p[3] - q[3])


def main():
    with open('input25.txt') as f:
        data = [(int(w), int(x), int(y), int(z)) for w, x, y, z in [line.split(',') for line in f.read().splitlines()]]
    data = sorted(data)

    constellations2 = []
    for point in data:
        constellations2.append({point})
    print(constellations2)

    changes = 1
    while changes:
        changes = 0
        for constellation in list(constellations2):
            for other_constellation in list(constellations2):
                if constellation == other_constellation:
                    continue
                if constellation not in constellations2 or other_constellation not in constellations2:
                    continue
                stars1 = list(constellation)
                stars2 = list(other_constellation)
                for p in stars1:
                    local_changes = 0
                    for q in stars2:
                        if distance(p, q) <= 3:
                            local_changes += 1
                            constellations2.remove(other_constellation)
                            constellation.update(other_constellation)
                            break
                    if local_changes:
                        changes += local_changes
                        break
        print(len(constellations2))

    print(constellations2)
    print(f'Day 25 Part 1 Answer: {len(constellations2)}')


if __name__ == '__main__':
    main()
