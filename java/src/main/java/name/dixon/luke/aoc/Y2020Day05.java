package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.*;
import java.util.stream.Stream;

public class Y2020Day05 extends Day {
    public Y2020Day05() {
        super();
    }

    public Y2020Day05(PrintStream printStream) {
        super(printStream);
    }

    static class Seat {
        String binaryRowPartitioning;
        Seat(String binaryRowPartitioning) {
            this.binaryRowPartitioning = binaryRowPartitioning;
        }

        int getRow() {
            return Integer.parseInt(
                binaryRowPartitioning
                    .substring(0, 7)
                    .replace('B', '1')
                    .replace('F', '0'),
                2
            );
        }

        int getColumn() {
            return Integer.parseInt(
                binaryRowPartitioning
                    .substring(7)
                    .replace('L', '0')
                    .replace('R', '1'),
                2);
        }

        int getSeatId() {
            return getRow() * 8 + getColumn();
        }
    }

    static class SeatIdCompare implements Comparator<Seat> {
        @Override
        public int compare(Seat o1, Seat o2) {
            return o1.getSeatId() - o2.getSeatId();
        }
    }

    static class SeatColumnCompare implements Comparator<Seat> {
        @Override
        public int compare(Seat o1, Seat o2) {
            return o1.getColumn() - o2.getColumn();
        }
    }

    int part1(String[] data) {
        Optional<Seat> seat = Arrays.stream(data)
            .map(Seat::new)
            .max(new SeatIdCompare());
        if (seat.isPresent()) {
            return seat.get().getSeatId();
        } else {
            throw new RuntimeException("Answer 1 not found");
        }
    }

    int part2(String[] data) {
        SortedMap<Integer, SortedSet<Seat>> seatRowMap = new TreeMap<>();

        for (String line : data) {
            Seat seat = new Seat(line);
            if (!seatRowMap.containsKey(seat.getRow())) {
                seatRowMap.put(seat.getRow(), new TreeSet<>(new SeatColumnCompare()));
            }
            seatRowMap.get(seat.getRow()).add(seat);
        }

        for (int row : seatRowMap.keySet()) {
            SortedSet<Seat> seats = seatRowMap.get(row);
            int previousColumn = seats.first().getColumn();
            for (Seat seat : seats) {
                if ((seat.getColumn() - previousColumn) > 1) {
                    return row * 8 + seat.getColumn() - 1;
                }
                previousColumn = seat.getColumn();
            }
        }
        throw new RuntimeException("Answer 2 not found");
    }

    @Override
    void run(Stream<String> input) {
        String[] data = input.toArray(String[]::new);
        writer("Answer part 1: " + part1(data));
        writer("Answer part 2: " + part2(data));
    }
}
