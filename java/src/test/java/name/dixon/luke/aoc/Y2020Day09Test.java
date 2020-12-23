package name.dixon.luke.aoc;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class Y2020Day09Test {

    @Test
    void part1() {
        long[] numbers = {
                35,
                20,
                15,
                25,
                47,
                40,
                62,
                55,
                65,
                95,
                102,
                117,
                150,
                182,
                127,
                219,
                299,
                277,
                309,
                576
        };
        Y2020Day09 day = new Y2020Day09();
        day.previousNumbersToConsider = 5;
        day.part1(numbers);
    }

    @Test
    void run() {
        OutputStream out = new ByteArrayOutputStream();
        Y2020Day09 day = new Y2020Day09(new PrintStream(out));

        day.previousNumbersToConsider = 5;
        List<String> input = Arrays.asList(
            "35",
            "20",
            "15",
            "25",
            "47",
            "40",
            "62",
            "55",
            "65",
            "95",
            "102",
            "117",
            "150",
            "182",
            "127",
            "219",
            "299",
            "277",
            "309",
            "576"
        );

        day.run(input.stream());
        assertEquals("Answer part 1: 127\nAnswer part 2: 62\n", out.toString());
    }
}