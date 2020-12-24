from lib import puzzle


DIRECTIONS = ['e', 'ne', 'nw', 'w', 'sw', 'se']
DIRECTION_TO_CUBE_COORDS = {
    'e': (1, -1, 0),
    'ne': (1, 0, -1),
    'nw': (0, 1, -1),
    'w': (-1, 1, 0),
    'sw': (-1, 0, 1),
    'se': (0, -1, 1),
}
CUBE_COORDS = tuple(DIRECTION_TO_CUBE_COORDS.values())


def add_coords(a, b):
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


class Tile:
    def __init__(self, coord):
        self.coord = coord
        self.black = False


def add_extra_adjacent_tiles(tiles_by_coord):
    """
    We want to consider tiles that are adjacent to black tiles
    as they might also need to be flipped.
    This function adds any extra tiles we need to consider.
    """
    for tile in list(tiles_by_coord.values()):
        if tile.black:
            for direction_coord in DIRECTION_TO_CUBE_COORDS.values():
                tile_coord = add_coords(tile.coord, direction_coord)
                if tile_coord not in tiles_by_coord:
                    tiles_by_coord[tile_coord] = Tile(tile_coord)


def traverse_tiles(reference_tile, tiles, tiles_by_coord):
    for tile in tiles:
        current_tile = reference_tile
        for direction in tile:
            direction_coord = DIRECTION_TO_CUBE_COORDS[direction]
            tile_coord = add_coords(current_tile.coord, direction_coord)
            if tile_coord not in tiles_by_coord:
                tiles_by_coord[tile_coord] = Tile(tile_coord)
            current_tile = tiles_by_coord[tile_coord]
        current_tile.black = not current_tile.black


def count_flipped_tiles(tiles):
    num_flipped = 0
    for tile in tiles:
        if tile.black:
            num_flipped += 1
    return num_flipped


class Day24(puzzle.Puzzle):
    year = '2020'
    day = '24'

    def get_data(self):
        data = self.input_data.splitlines()

#         data = '''\
# sesenwnenenewseeswwswswwnenewsewsw
# neeenesenwnwwswnenewnwwsewnenwseswesw
# seswneswswsenwwnwse
# nwnwneseeswswnenewneswwnewseswneseene
# swweswneswnenwsewnwneneseenw
# eesenwseswswnenwswnwnwsewwnwsene
# sewnenenenesenwsewnenwwwse
# wenwwweseeeweswwwnwwe
# wsweesenenewnwwnwsenewsenwwsesesenwne
# neeswseenwwswnwswswnw
# nenwswwsewswnenenewsenwsenwnesesenew
# enewnwewneswsewnwswenweswnenwsenwsw
# sweneswneswneneenwnewenewwneswswnese
# swwesenesewenwneswnwwneseswwne
# enesenwswwswneneswsenwnewswseenwsese
# wnwnesenesenenwwnenwsewesewsesesew
# nenewswnwewswnenesenwnesewesw
# eneswnwswnwsenenwnwnwwseeswneewsenese
# neswnwewnwnwseenwseesewsenwsweewe
# wseweeenwnesenwwwswnew'''.splitlines()

        tiles = []
        for line in data:
            tile = []
            i = 0
            while i < len(line):
                if line[i] == 's':
                    tile.append(line[i] + line[i + 1])
                    i += 1
                elif line[i] == 'n':
                    tile.append(line[i] + line[i + 1])
                    i += 1
                elif line[i] == 'w':
                    tile.append('w')
                elif line[i] == 'e':
                    tile.append('e')
                i += 1

            tiles.append(tile)

        return tiles

    def part1(self):
        tiles = self.get_data()

        tiles_by_coord = {}
        reference_tile = Tile((0, 0, 0))
        tiles_by_coord[reference_tile.coord] = reference_tile

        traverse_tiles(reference_tile, tiles, tiles_by_coord)

        return count_flipped_tiles(tiles_by_coord.values())

    def part2(self):
        tiles = self.get_data()

        tiles_by_coord = {}
        reference_tile = Tile((0, 0, 0))
        tiles_by_coord[reference_tile.coord] = reference_tile

        traverse_tiles(reference_tile, tiles, tiles_by_coord)
        add_extra_adjacent_tiles(tiles_by_coord)

        black_tiles = set()
        for tile in tiles_by_coord.values():
            if tile.black:
                black_tiles.add(tile)

        for _ in range(100):
            need_flip = []

            tiles_to_consider = set()
            for tile in black_tiles:
                tiles_to_consider.add(tile)
                tiles_to_consider |= set([tiles_by_coord[add_coords(tile.coord, d)] for d in CUBE_COORDS])

            for tile in tiles_to_consider:
                tiles = [
                    tiles_by_coord[add_coords(tile.coord, d)]
                    for d in CUBE_COORDS
                    if add_coords(tile.coord, d) in tiles_by_coord
                ]
                num_flipped = count_flipped_tiles(tiles)
                if not tile.black and num_flipped == 2:
                    need_flip.append(tile)
                elif tile.black and (num_flipped == 0 or num_flipped > 2):
                    need_flip.append(tile)

            for tile in need_flip:
                if tile.black:
                    tile.black = not tile.black
                    black_tiles.remove(tile)
                else:
                    tile.black = not tile.black
                    black_tiles.add(tile)

            add_extra_adjacent_tiles(tiles_by_coord)

        return count_flipped_tiles(tiles_by_coord.values())

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
