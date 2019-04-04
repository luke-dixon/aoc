import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

class Day1 {
    private static List<Integer> rawDataToNumbers(BufferedReader reader) throws IOException {
        List<Integer> numbers = new ArrayList<>();
        String line;
        while ((line = reader.readLine()) != null) {
            numbers.add(Integer.parseInt(line));
        }
        return numbers;
    }

    private static void part1(List<Integer> numbers) {
        int total = 0;
        for (Integer number : numbers) {
            total += number;
        }
        System.out.printf("Part 1 Answer: %d\n", total);
    }

    private static void part2(List<Integer> numbers) {
        boolean found = false;
        int frequency = 0;
        Set<Integer> frequencies = new HashSet<>();
        frequencies.add(frequency);
        
        while (!found) {
            for (Integer number : numbers) {
                frequency += number;
                if (frequencies.contains(frequency)) {
                    found = true;
                    break;
                }
                frequencies.add(frequency);
            }
        }
        System.out.printf("Part 2 Answer: %d\n", frequency);
    }

    public static void main(String[] args) {
        Path path = Paths.get("input1.txt");
        try (BufferedReader reader = Files.newBufferedReader(path)) {
            List<Integer> numbers = Day1.rawDataToNumbers(reader);
            Day1.part1(numbers);
            Day1.part2(numbers);
        } catch (IOException e) {
            System.err.println("Error opening file");
        }
    }
}
