package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.Arrays;
import java.util.stream.Stream;

public class Y2020Day23 extends Day {
    public Y2020Day23() {
        super();
    }

    public Y2020Day23(PrintStream printStream) {
        super(printStream);
    }

    static class Cup {
        int label;
        Cup next;

        Cup(int aLabel, Cup aNextCup) {
            label = aLabel;
            next = aNextCup;
        }
    }

    private Cup moveCups(int numCards, int numMoves, Cup currentCup) {
        // Get a table of cards for fast lookup
        Cup[] cupLookup = getCupLookupTable(currentCup, numCards);

        for (int i = 0; i < numMoves; i++) {
            Cup cup1 = currentCup.next;
            Cup cup2 = cup1.next;
            Cup cup3 = cup2.next;

            currentCup.next = cup3.next;

            int destination = currentCup.label;
            do {
                destination--;
                if (destination < 1) {
                    destination = numCards;
                }
            } while (
                destination == cup1.label
                || destination == cup2.label
                || destination == cup3.label
                || destination == currentCup.label
            );

            Cup destinationCup = cupLookup[destination];
            cup3.next = destinationCup.next;
            destinationCup.next = cup1;

            currentCup = currentCup.next;
        }

        return cupLookup[1];
    }

    private Cup[] getCupLookupTable(Cup startCup, int size) {
        Cup[] cupLookup = new Cup[size + 1];
        cupLookup[startCup.label] = startCup;
        Cup currentCup = startCup;
        while (currentCup.next != startCup) {
            currentCup = currentCup.next;
            cupLookup[currentCup.label] = currentCup;
        }
        return cupLookup;
    }

    String part1(int[] cups) {
        int numCards = cups.length;
        int numMoves = 100;

        // Create the cups from the input
        Cup head = null;
        Cup tail = null;
        for (int i : cups) {
            Cup cup = new Cup(i, null);
            if (head == null) {
                head = cup;
            }
            if (tail != null) {
                tail.next = cup;
            }
            tail = cup;
        }
        assert(tail != null);

        Cup currentCup = head;

        // Close the loop
        tail.next = head;

        currentCup = moveCups(numCards, numMoves, currentCup);

        StringBuilder answer = new StringBuilder();
        currentCup = currentCup.next;
        while (currentCup.label != 1) {
            answer.append(currentCup.label);
            currentCup = currentCup.next;
        }

        return answer.toString();
    }

    long part2(int[] cups) {
        int numCards = 1000000;
        int numMoves = 10000000;

        // Create the cups from the input
        Cup head = null;
        Cup tail = null;
        for (int i : cups) {
            Cup cup = new Cup(i, null);
            if (head == null) {
                head = cup;
            }
            if (tail != null) {
                tail.next = cup;
            }
            tail = cup;
        }
        assert(tail != null);

        // Add the extra cards
        for (int i = 10; i <= numCards; i++) {
            Cup cup = new Cup(i, null);
            tail.next = cup;
            tail = cup;
        }

        Cup currentCup = head;

        // Close the loop
        tail.next = head;

        currentCup = moveCups(numCards, numMoves, currentCup);

        Cup cup1 = currentCup.next;
        Cup cup2 = cup1.next;

        return (long) cup1.label * (long) cup2.label;
    }

    @Override
    void run(Stream<String> input) {
        int[] cups = Arrays.stream(
            input.toArray(String[]::new)[0].split("")
        ).mapToInt((Integer::parseInt)).toArray();

        writer("Answer part 1: " + part1(cups));
        writer("Answer part 2: " + part2(cups));
    }
}
