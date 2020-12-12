package name.dixon.luke.aoc;

import name.dixon.luke.aoc.iterables.Combinations;

import java.io.PrintStream;
import java.util.List;
import java.util.stream.Stream;

public class Y2020Day01 extends Day {
    public Y2020Day01() {
        super();
    }

    public Y2020Day01(PrintStream printStream) {
        super(printStream);
    }

    int sumOfListElements(int[] data, List<Integer> elems) {
        return elems.stream()
            .mapToInt(elem -> elem)
            .map(elem -> data[elem])
            .sum();
    }

    int productOfElements(int[] data, List<Integer> elems) {
        if (elems.isEmpty()) {
            return 0;
        }
        return elems.stream()
            .mapToInt(elem -> elem)
            .map(elem -> data[elem])
            .reduce(1, (a, b) -> a * b);
    }

    int answer(int[] data, int num) {
        for (List<Integer> l : new Combinations(data.length, num)) {
            if (sumOfListElements(data, l) == 2020) {
                return productOfElements(data, l);
            }
        }
        throw new RuntimeException("Answer not found!");
    }

    void part1(int[] data) {
        writer("Part 1 answer: " + answer(data, 2));
    }

    void part2(int[] data) {
        writer("Part 2 answer: " + answer(data, 3));
    }

    @Override
    void run(Stream<String> input) {
        int[] data = input
            .mapToInt(Integer::parseInt)
            .toArray();
        part1(data.clone());
        part2(data);
    }
}
