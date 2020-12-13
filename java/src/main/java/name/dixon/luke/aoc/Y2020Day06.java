package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Stream;

public class Y2020Day06 extends Day {
    public Y2020Day06() {
        super();
    }

    public Y2020Day06(PrintStream printStream) {
        super(printStream);
    }

    private int part2(List<List<Set<Character>>> groups) {
        List<Set<Character>> consolidatedGroups = new ArrayList<>();
        for (List<Set<Character>> group : groups) {
            Set<Character> questions = new HashSet<>();
            questions.addAll(group.get(0));
            for (Set<Character> person : group) {
                questions.retainAll(person);
            }
            consolidatedGroups.add(questions);
        }

        return consolidatedGroups.stream().mapToInt(Set::size).sum();
    }

    private int part1(List<List<Set<Character>>> groups) {
        List<Set<Character>> consolidatedGroups = new ArrayList<>();
        for (List<Set<Character>> group : groups) {
            Set<Character> questions = new HashSet<>();
            for (Set<Character> person : group) {
                questions.addAll(person);
            }
            consolidatedGroups.add(questions);
        }

        return consolidatedGroups.stream().mapToInt(Set::size).sum();
    }

    @Override
    void run(Stream<String> input) {
        String[] data = input.toArray(String[]::new);

        List<List<Set<Character>>> groups = new ArrayList<>();

        List<Set<Character>> currentGroup = new ArrayList<>();
        groups.add(currentGroup);
        for (String line : data) {
            if (line.equals("")) {
                currentGroup = new ArrayList<>();
                groups.add(currentGroup);
            } else {
                Set<Character> s = new HashSet<>();
                for (char c : line.toCharArray()) {
                    s.add(c);
                }
                currentGroup.add(s);
            }
        }

        writer("Answer part 1: " + part1(groups));
        writer("Answer part 2: " + part2(groups));
    }
}
