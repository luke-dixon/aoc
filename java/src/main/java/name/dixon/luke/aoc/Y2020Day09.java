package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.Arrays;
import java.util.OptionalLong;
import java.util.stream.Stream;

public class Y2020Day09 extends Day {
    public Y2020Day09() {
        super();
    }

    public Y2020Day09(PrintStream printStream) {
        super(printStream);
    }

    int previousNumbersToConsider = 25;

    long part1(long[] numbers) {
        for (int k = previousNumbersToConsider; k < numbers.length; k++) {

            boolean found = false;

            outer:
            for (int j = k - previousNumbersToConsider; j < k; j++) {
                for (int i = j + 1; i < k; i++) {
                    if ((numbers[i] + numbers[j]) == numbers[k]) {
                        found = true;
                        break outer;
                    }
                }
            }

            if (!found) {
                return numbers[k];
            }
        }
        throw new RuntimeException("Answer not found");
    }

    long part2(long[] numbers, long part1Answer) {
        for (int k = 2; k < numbers.length; k++) {
            for (int j = 0; j < numbers.length - (k - 1); j++) {
                long[] range = Arrays.copyOfRange(numbers, j, j + k);
                if (Arrays.stream(range).sum() == part1Answer) {
                    OptionalLong min = Arrays.stream(range).min();
                    OptionalLong max = Arrays.stream(range).max();
                    return min.getAsLong() + max.getAsLong();
                }
            }
        }
        throw new RuntimeException("Answer not found");
    }

    @Override
    void run(Stream<String> input) {
        long[] numbers = input.mapToLong(Long::parseLong).toArray();

        long part1Answer = part1(numbers);

        writer("Answer part 1: " + part1Answer);
        writer("Answer part 2: " + part2(numbers, part1Answer));
    }
}
