package name.dixon.luke.aoc;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class Y2019Day01Test {

    @Test
    public void testTestRun() {
        OutputStream out = new ByteArrayOutputStream();
        Y2019Day01 day01 = new Y2019Day01(new PrintStream(out));
        List<String> input = Arrays.asList(
                "12", "14", "1969", "100756"
        );
        day01.run(input.stream());

        assertEquals("Part 1 answer: 34241\nPart 2 answer: 51316\n", out.toString());
    }

    @ParameterizedTest
    @CsvSource({
            "12, 2",
            "14, 2",
            "1969, 654",
            "100756, 33583"
    })
    public void testCalcFuel(int mass, int fuelRequired) {
        assertEquals(fuelRequired, Y2019Day01.calcFuel(mass));
    }

    @ParameterizedTest
    @CsvSource({
            "12, 2",
            "14, 2",
            "1969, 966",
            "100756, 50346"
    })
    public void testCalcFuel2(int mass, int fuelRequired) {
        assertEquals(fuelRequired, Y2019Day01.calcFuel2(mass));
    }
}