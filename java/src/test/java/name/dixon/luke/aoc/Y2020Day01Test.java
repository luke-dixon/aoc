package name.dixon.luke.aoc;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class Y2020Day01Test {

    @Test
    public void run() {
        OutputStream out = new ByteArrayOutputStream();
        Y2020Day01 day01 = new Y2020Day01(new PrintStream(out));
        List<String> input = Arrays.asList(
            "1721", "979", "366", "299", "675", "1456"
        );
        day01.run(input.stream());

        assertEquals("Part 1 answer: 514579\nPart 2 answer: 241861950\n", out.toString());
    }

    @Test
    void productOfElements() {
        Y2020Day01 day01 = new Y2020Day01();
        assertEquals(0, day01.productOfElements(new int[0], new ArrayList<Integer>()));
        assertThrows(ArrayIndexOutOfBoundsException.class, () -> {
            day01.productOfElements(new int[0], Arrays.asList(1, 2));
        });
        assertEquals(15, day01.productOfElements(new int[]{5, 3, 9}, Arrays.asList(0, 1)));
    }
}
