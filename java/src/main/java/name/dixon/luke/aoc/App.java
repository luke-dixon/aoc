package name.dixon.luke.aoc;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.Map;

import static java.util.Map.entry;

public class App {
    static Map<String, Day> days = Map.ofEntries(
            entry("2019.01", new Y2019Day01()),
            entry("2019.02", new Y2019Day02()),
            entry("2020.01", new Y2020Day01())
    );

    private static void usage() {
        System.out.println("Usage: aoc <year>.<day> <input-file>");
        System.out.println("For example: aoc 2019.01 input01.txt");
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            usage();
            System.exit(1);
        }
        Day day = days.get(args[0]);
        if (day == null) {
            System.err.println("That day hasn't been implemented yet.");
            System.err.println("Here's a list of days you can run: " + days.keySet().toString());
            System.exit(2);
        }
        try {
            day.run(new BufferedReader(new FileReader(args[1])).lines());
        } catch (FileNotFoundException e) {
            System.err.printf("Cannot find file %s\n", args[1]);
            System.exit(3);
        }
    }
}
