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

class Y2020Day04Test {

    @Test
    void run() {
        OutputStream out = new ByteArrayOutputStream();
        Y2020Day04 day = new Y2020Day04(new PrintStream(out));

        List<String> input = Arrays.asList(
            "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
            "byr:1937 iyr:2017 cid:147 hgt:183cm",
            "",
            "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
            "hcl:#cfa07d byr:1929",
            "",
            "hcl:#ae17e1 iyr:2013",
            "eyr:2024",
            "ecl:brn pid:760753108 byr:1931",
            "hgt:179cm",
            "",
            "hcl:#cfa07d eyr:2025 pid:166559648",
            "iyr:2011 ecl:brn hgt:59in"
        );
        day.run(input.stream());
        assertEquals("Answer part 1: 2\nAnswer part 2: 2\n", out.toString());
    }

    @ParameterizedTest
    @CsvSource({
            "1919, false",
            "1920, true",
            "2002, true",
            "2003, false",
    })
    public void isByrValid(String byr, boolean result) {
        Y2020Day04.Passport passport = new Y2020Day04.Passport();
        passport.properties.put("byr", byr);
        assertEquals(result, passport.isByrValid());
    }

    @ParameterizedTest
    @CsvSource({
            "149cm, false",
            "150cm, true",
            "193cm, true",
            "194cm, false",
            "58in, false",
            "59in, true",
            "76in, true",
            "77in, false",
            "abin, false",
            "100, false",
    })
    public void isHgtValid(String hgt, boolean result) {
        Y2020Day04.Passport passport = new Y2020Day04.Passport();
        passport.properties.put("hgt", hgt);
        assertEquals(result, passport.isHgtValid());
    }

    @ParameterizedTest
    @CsvSource({
        "'#123abc', true",
        "'#123abz', false",
        "123abc, false",
    })
    public void isHclValid(String hcl, boolean result) {
        Y2020Day04.Passport passport = new Y2020Day04.Passport();
        passport.properties.put("hcl", hcl);
        assertEquals(result, passport.isHclValid());
    }

    @ParameterizedTest
    @CsvSource({
        "brn, true",
        "wat, false",
    })
    public void isEclValid(String ecl, boolean result) {
        Y2020Day04.Passport passport = new Y2020Day04.Passport();
        passport.properties.put("ecl", ecl);
        assertEquals(result, passport.isEclValid());
    }

    @ParameterizedTest
    @CsvSource({
            "000000001, true",
            "0123456789, false",
    })
    public void isPidValid(String pid, boolean result) {
        Y2020Day04.Passport passport = new Y2020Day04.Passport();
        passport.properties.put("pid", pid);
        assertEquals(result, passport.isPidValid());
    }
}
