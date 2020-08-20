package name.dixon.luke.aoc;

import com.ginsberg.junit.exit.ExpectSystemExitWithStatus;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertTrue;

class AppTest {
    @Test
    @ExpectSystemExitWithStatus(1)
    void usage() {
        // Run app with wrong number of args
        String[] args = {"empty"};
        App.main(args);
    }

    @Test
    @ExpectSystemExitWithStatus(2)
    void badDay() {
        // Run app with wrong number of args
        String[] args = {"2019.0", "input.txt"};
        App.main(args);
    }

    @Test
    @ExpectSystemExitWithStatus(3)
    void mainMissingFile() {
        // Set up app
        App.days = new HashMap<>();
        App.days.put("empty", new EmptyDay());

        // Run app with no input file
        String[] args = {"empty", "input.txt"};
        App.main(args);
    }

    @Test
    void main(@TempDir Path tempDir) throws IOException {
        // Set up app
        App.days = new HashMap<>();
        App.days.put("empty", new EmptyDay());

        // Set up input file
        File file = new File(tempDir.resolve("test.txt").toString());
        assertTrue(file.createNewFile());

        // Run app
        String[] args = {"empty", file.toString()};
        App.main(args);
    }

    static class EmptyDay extends Day {
        @Override
        void run(Stream<String> input) {
        }
    }
}
