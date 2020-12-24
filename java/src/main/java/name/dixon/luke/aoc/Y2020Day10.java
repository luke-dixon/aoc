package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Stream;

public class Y2020Day10 extends Day {
    public Y2020Day10() {
        super();
    }

    public Y2020Day10(PrintStream printStream) {
        super(printStream);
    }

    int part1(long[] numbers) {
        int ones = 0;
        int threes = 0;
        long last = 0;
        for (long number : numbers) {
            if (number - last == 1) {
                ones++;
            } else if (number - last == 3) {
                threes++;
            }
            last = number;
        }

        // Adapter joltage is always 3 greater than max
        threes++;

        return ones * threes;
    }

    long part2(long[] numbers) {
        Map<Long, Long> possibilities = new HashMap<>();
        possibilities.put(numbers[numbers.length - 1] + 3, 1L);

        // Work backwards through the adapters
        for (int j = numbers.length - 1; j >= 0; j--) {
            long total = 0;
            // Sum the possibilities the next three greater adapters
            for (int i = 1; i < 4; i++) {
                total += possibilities.getOrDefault(numbers[j] + i, 0L);
            }
            possibilities.put(numbers[j], total);
        }

        long total = 0;
        for (long i = 1; i < 4; i++) {
            total += possibilities.getOrDefault(i, 0L);
        }

        return total;
    }

    @Override
    void run(Stream<String> input) {
        long[] numbers = input.mapToLong(Long::parseLong).toArray();

        Arrays.sort(numbers);

        writer("Answer part 1: " + part1(numbers));
        writer("Answer part 2: " + part2(numbers));
    }
}
