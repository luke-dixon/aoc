package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.stream.Stream;

public abstract class Day {
    private final PrintStream printStream;

    public Day() {
        printStream = System.out;
    }

    public Day(PrintStream printStream) {
        this.printStream = printStream;
    }

    protected void writer(String line) {
        printStream.println(line);
    }

    abstract void run(Stream<String> input);
}
