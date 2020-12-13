package name.dixon.luke.aoc;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class Y2020Day05Test {
    @ParameterizedTest
    @CsvSource({
            "BFFFBBFRRR, 70, 7, 567",
            "FFFBBBFRRR, 14, 7, 119",
            "BBFFBBFRLL, 102, 4, 820",
            "FFFFFFFLLL, 0, 0, 0",
    })
    void seat(String binaryRowPartitioning, int row, int column, int seadId) {
        Y2020Day05.Seat seat = new Y2020Day05.Seat(binaryRowPartitioning);
        assertEquals(row, seat.getRow());
        assertEquals(column, seat.getColumn());
        assertEquals(seadId, seat.getSeatId());
    }

    @Test
    void run() {
        OutputStream out = new ByteArrayOutputStream();
        Y2020Day05 day = new Y2020Day05(new PrintStream(out));

        List<String> input = Arrays.asList(
            "FFFFFFFLLL",
            "FFFFFFFLLR",
            "FFFFFFFLRL",
            "FFFFFFFLRR",
            "FFFFFFFRLL",
            "FFFFFFFRLR",
            "FFFFFFFRRL",
            "FFFFFFFRRR",
            "FFFFFFBLLL",
            "FFFFFFBLLR",
            "FFFFFFBLRL",
            "FFFFFFBLRR",
            // "FFFFFFBRLL", <- this is where our seat is
            "FFFFFFBRLR",
            "FFFFFFBRRL",
            "FFFFFFBRRR" // this is the max seat

        );
        day.run(input.stream());
        assertEquals("Answer part 1: 15\nAnswer part 2: 12\n", out.toString());
    }
}