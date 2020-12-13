package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Y2020Day04 extends Day {
    public Y2020Day04() {
        super();
    }

    public Y2020Day04(PrintStream printStream) {
        super(printStream);
    }

    static class Passport {
        Map<String, String> properties = new HashMap<>();
        Set<String> requiredFields = Stream.of(
                "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"
            ).collect(Collectors.toSet());
        Set<String> validEcl = Stream.of(
                "amb blu brn gry grn hzl oth".split(" ")
        ).collect(Collectors.toSet());

        static Passport fromRaw(List<String> rawPassport) {
            Passport passport = new Passport();
            for (String line : rawPassport) {
                for (String kv : line.split(" ")) {
                    String key = kv.split(":")[0];
                    String value = kv.split(":")[1];
                    passport.properties.put(key, value);
                }
            }
            return passport;
        }

        boolean hasRequiredFields() {
            return properties.keySet().containsAll(requiredFields);
        }

        boolean isByrValid() {
            return 1920 <= Integer.parseInt(properties.get("byr")) && Integer.parseInt(properties.get("byr")) <= 2002;
        }
        boolean isIyrValid() {
            return 2010 <= Integer.parseInt(properties.get("iyr")) && Integer.parseInt(properties.get("iyr")) <= 2020;
        }
        boolean isEyrValid() {
            return 2020 <= Integer.parseInt(properties.get("eyr")) && Integer.parseInt(properties.get("eyr")) <= 2030;
        }
        boolean isHgtValid() {
            String hgt = properties.get("hgt");
            try {
                if (hgt.endsWith("cm")) {
                    int height = Integer.parseInt(hgt.substring(0, hgt.length() - 2));
                    return 150 <= height && height <= 193;
                } else if (hgt.endsWith("in")) {
                    int height = Integer.parseInt(hgt.substring(0, hgt.length() - 2));
                    return 59 <= height && height <= 76;
                } else {
                    return false;
                }
            } catch (NumberFormatException e) {
                return false;
            }
        }
        boolean isHclValid() {
            String hcl = properties.get("hcl");
            if (hcl.startsWith("#") && hcl.length() == 7) {
                try {
                    int hclInt = Integer.parseInt(hcl.substring(1), 16);
                    return 0 <= hclInt && hclInt <= 0xffffff;
                } catch (NumberFormatException e) {
                    return false;
                }
            } else {
                return false;
            }
        }
        boolean isEclValid() {
            return validEcl.contains(properties.get("ecl"));
        }
        boolean isPidValid() {
            return properties.get("pid").length() == 9 && 0 <= Integer.parseInt(properties.get("pid")) && Integer.parseInt(properties.get("pid")) <= 999999999;
        }
    }

    long part1(List<Passport> passports) {
        return passports.stream()
            .filter(Passport::hasRequiredFields)
            .count();
    }

    long part2(List<Passport> passports) {
        return passports.stream()
            .filter(Passport::hasRequiredFields)
            .filter(Passport::isByrValid)
            .filter(Passport::isIyrValid)
            .filter(Passport::isEyrValid)
            .filter(Passport::isHgtValid)
            .filter(Passport::isHclValid)
            .filter(Passport::isEclValid)
            .filter(Passport::isPidValid)
            .count();
    }

    @Override
    void run(Stream<String> input) {
        String[] inputLines = (String[]) input.toArray(String[]::new);

        List<Passport> passports = new ArrayList<>();
        List<String> rawPassport = new ArrayList<>();
        for (String line : inputLines) {
            if (line.strip().equals("")) {
                passports.add(Passport.fromRaw(rawPassport));
                rawPassport = new ArrayList<>();
            } else {
                rawPassport.add(line);
            }
        }
        passports.add(Passport.fromRaw(rawPassport));

        writer("Answer part 1: " + part1(passports));
        writer("Answer part 2: " + part2(passports));
    }
}
