package name.dixon.luke.aoc;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class Y2020Day06Test {

    @Test
    void run() {
        OutputStream out = new ByteArrayOutputStream();
        Y2020Day06 day = new Y2020Day06(new PrintStream(out));

        List<String> input = Arrays.asList(
            "abc",
            "",
            "a",
            "b",
            "c",
            "",
            "ab",
            "ac",
            "",
            "a",
            "a",
            "a",
            "a",
            "",
            "b"
        );
        day.run(input.stream());
        assertEquals("Answer part 1: 11\nAnswer part 2: 6\n", out.toString());
    }
}