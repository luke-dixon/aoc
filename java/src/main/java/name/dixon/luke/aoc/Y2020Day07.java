package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.*;
import java.util.stream.Stream;

public class Y2020Day07 extends Day {
    public Y2020Day07() {
        super();
    }

    public Y2020Day07(PrintStream printStream) {
        super(printStream);
    }

    int part1(Map<String, Map<String, Integer>> rules) {
        Map<String, Set<String>> reverse = new HashMap<>();

        for (String containerBag : rules.keySet()) {
            for (String bag : rules.get(containerBag).keySet()) {
                if (!reverse.containsKey(bag)) {
                    Set<String> bags = new HashSet<>();
                    reverse.put(bag, bags);
                }
                reverse.get(bag).add(containerBag);
            }
        }

        Set<String> shinyGoldBagContainers = new HashSet<>(reverse.get("shiny gold"));

        while (true) {
            int newBags = 0;

            for (String bag : new HashSet<>(shinyGoldBagContainers)) {
                Set<String> containerBags = reverse.get(bag);
                if (containerBags != null) {
                    for (String containerBag : containerBags) {
                        if (!shinyGoldBagContainers.contains(containerBag)) {
                            shinyGoldBagContainers.add(containerBag);
                            newBags++;
                        }
                    }
                }
            }

            if (newBags == 0) {
                break;
            }
        }

        return shinyGoldBagContainers.size();
    }

    int part2(Map<String, Map<String, Integer>> rules) {
        int shinyGoldBagContents = -1;

        Deque<String> stack = new ArrayDeque<>();
        stack.push("shiny gold");

        //Set<String> bagsSeen = new HashSet<>();

        while (stack.size() > 0) {
            String currentBag = stack.pop();
            shinyGoldBagContents++;

            Map<String, Integer> currentBagContents = rules.get(currentBag);
            if (currentBagContents != null) {
                for (String bag : currentBagContents.keySet()) {
                    int quantity = rules.get(currentBag).get(bag);
                    for (int i = 0; i < quantity; i++) {
                        stack.push(bag);
                    }
                }
            }
        }

        return shinyGoldBagContents;
    }

    @Override
    void run(Stream<String> input) {
        Map<String, Map<String, Integer>> rules = new HashMap<>();
        for (String rawRule : input.toArray(String[]::new)) {
            String containerBag = rawRule.split(" contain ")[0].replace( " bags", "");
            String rawContainsBags = rawRule.split(" contain ")[1].replace(".", "");
            if (rawContainsBags.equals("no other bags")) {
                rules.put(containerBag, new HashMap<>());
            } else {
                Map<String, Integer> containsBags = new HashMap<>();
                for (String rawBagQuantity : rawContainsBags.split(", ")) {
                    String s = rawBagQuantity
                        .replace(" bags", "")
                        .replace(" bag", "");
                    int quantity = Integer.parseInt(s.split(" ")[0]);
                    containsBags.put(s.split(" ")[1] + " " + s.split(" ")[2], quantity);
                }
                rules.put(containerBag, containsBags);
            }
        }

        writer("Answer part 1: " + part1(rules));
        writer("Answer part 2: " + part2(rules));
    }
}
