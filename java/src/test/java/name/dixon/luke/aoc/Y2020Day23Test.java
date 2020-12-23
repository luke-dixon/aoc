package name.dixon.luke.aoc;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class Y2020Day23Test {

    @Test
    void run() {
        OutputStream out = new ByteArrayOutputStream();
        Y2020Day23 day = new Y2020Day23(new PrintStream(out));

        List<String> input = Arrays.asList(new String[]{"389125467"});
        day.run(input.stream());
        assertEquals("Answer part 1: 67384529\nAnswer part 2: 149245887792\n", out.toString());
    }
}