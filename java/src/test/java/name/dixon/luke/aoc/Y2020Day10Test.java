package name.dixon.luke.aoc;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class Y2020Day10Test {

    @Test
    void run() {
        OutputStream out = new ByteArrayOutputStream();
        Day day = new Y2020Day10(new PrintStream(out));

        List<String> input = Arrays.asList(
            "16",
            "10",
            "15",
            "5",
            "1",
            "11",
            "7",
            "19",
            "6",
            "12",
            "4"
        );

        day.run(input.stream());
        assertEquals("Answer part 1: 35\nAnswer part 2: 8\n", out.toString());
    }
}