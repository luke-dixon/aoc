package name.dixon.luke.aoc;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class Y2020Day03Test {

    @Test
    void run() {
        OutputStream out = new ByteArrayOutputStream();
        Y2020Day03 day = new Y2020Day03(new PrintStream(out));

        List<String> input = Arrays.asList(
            "..##.......",
            "#...#...#..",
            ".#....#..#.",
            "..#.#...#.#",
            ".#...##..#.",
            "..#.##.....",
            ".#.#.#....#",
            ".#........#",
            "#.##...#...",
            "#...##....#",
            ".#..#...#.#"
        );

        day.run(input.stream());
        assertEquals("Answer part 1: 7\nAnswer part 2: 336\n", out.toString());
    }
}