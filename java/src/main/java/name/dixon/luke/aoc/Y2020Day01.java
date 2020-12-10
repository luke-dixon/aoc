package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.stream.Stream;

public class Y2020Day01 extends Day {
    public Y2020Day01() {
        super();
    }

    public Y2020Day01(PrintStream printStream) {
        super(printStream);
    }

    void part1(int[] data) {
        outer:
        for (int i : data) {
            for (int j : data) {
                if (i == j) {
                    continue;
                }
                if ((i + j) == 2020) {
                    writer("Part 1 answer: " + i * j);
                    break outer;
                }
            }
        }
    }

    void part2(int[] data) {
        outer:
        for (int i : data) {
            for (int j : data) {
                if (i == j) {
                    continue;
                }
                for (int k : data) {
                    if (i == k || k == j) {
                        continue;
                    }
                    if ((i + j + k) == 2020) {
                        writer("Part 2 answer: " + i * j * k);
                        break outer;
                    }
                }
            }
        }
    }

    @Override
    void run(Stream<String> input) {
        int[] data = input
                .flatMap(x -> Stream.of(x.split(",")))
                .mapToInt(Integer::parseInt).toArray();
        part1(data.clone());
        part2(data);
    }
}