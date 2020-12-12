package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.Arrays;
import java.util.stream.Stream;

import static java.lang.Math.max;
import static java.lang.Math.min;

public class Y2020Day03 extends Day {
    public Y2020Day03() {
        super();
    }

    public Y2020Day03(PrintStream printStream) {
        super(printStream);
    }

    boolean animate = false;

    void printMap(String[] map, int drawHeight, int tobogganX, int tobogganY) {
        int height = map.length;
        int width = map[0].length();
        StringBuilder screen = new StringBuilder();
        screen.append(String.format("%n"));
        for (int y = max(0, tobogganY - drawHeight / 2); y < min(height, tobogganY + drawHeight / 2); y++) {
            for (int x = 0; x < width; x++) {
                if (x == tobogganX && y == tobogganY) {
                    screen.append('O');
                } else {
                    screen.append(map[y].charAt(x));
                }
            }
            screen.append(String.format("%n"));
        }
        System.out.println(screen);
    }

    long answer(String[] map, int slopeX, int slopeY) {
        int width = map[0].length();
        int height = map.length;
        int x = 0;
        int y = 0;

        long trees = 0;

        while (true) {
            if (animate) {
                printMap(map, 10, x, y);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    return -1;
                }
            }

            x = (x + slopeX) % width;
            y = y + slopeY;

            if (y >= height) {
                break;
            }

            if (map[y].charAt(x) == '#') {
                trees++;
            }
        }
        return trees;
    }

    long part2(String[] map) {
        int[][] slopes = {
                {1, 1},
                {3, 1},
                {5, 1},
                {7, 1},
                {1, 2}
        };
        return Arrays.stream(slopes)
            .map(x -> answer(map, x[0], x[1]))
            .reduce(1L, (a, b) -> a * b);
    }

    @Override
    void run(Stream<String> input) {
        String[] map = input.toArray(String[]::new);

        writer("Answer part 1: " + answer(map, 3, 1));
        writer("Answer part 2: " + part2(map));
    }
}
