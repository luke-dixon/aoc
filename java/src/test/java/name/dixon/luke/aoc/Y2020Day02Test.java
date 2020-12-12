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

class Y2020Day02Test {

    @Test
    void run() {
        OutputStream out = new ByteArrayOutputStream();
        Y2020Day02 day = new Y2020Day02(new PrintStream(out));

        List<String> input = Arrays.asList(
            "1-3 a: abcde",
            "1-3 b: cdefg",
            "2-9 c: ccccccccc"
        );

        day.run(input.stream());

        assertEquals("Answer part 1: 2\nAnswer part 2: 1\n", out.toString());
    }

    @ParameterizedTest
    @CsvSource({
            "1-3 a: abcde, true",
            "1-3 b: cdefg, false",
            "2-9 c: ccccccccc, true"
    })
    public void Part1PolicyIsValid(String password, boolean result) {
        Y2020Day02.PasswordPolicy policy = new Y2020Day02.Part1Policy();
        assertEquals(result, Y2020Day02.Password.fromData(password).isValid(policy));
    }

    @ParameterizedTest
    @CsvSource({
            "1-3 a: abcde, true",
            "1-3 b: cdefg, false",
            "2-9 c: ccccccccc, false"
    })
    public void Part2PolicyIsValid(String password, boolean result) {
        Y2020Day02.PasswordPolicy policy = new Y2020Day02.Part2Policy();
        assertEquals(result, Y2020Day02.Password.fromData(password).isValid(policy));
    }
}
