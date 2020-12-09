package name.dixon.luke.aoc;

import java.util.stream.Stream;

public class Y2019Day02 extends Day {
    final int OP_HALT = 99;
    final int OP_ADD = 1;
    final int OP_MULT = 2;

    final int ARG1_OFFSET = 1;
    final int ARG2_OFFSET = 2;
    final int RETURN_ADDRESS_OFFSET = 3;

    int runIntCode(int[] data) {
        int currentPos = 0;
        while (data[currentPos] != OP_HALT) {
            if (data[currentPos] == OP_ADD) {
                int address1 = data[currentPos + ARG1_OFFSET];
                int address2 = data[currentPos + ARG2_OFFSET];
                int returnAddress = data[currentPos + RETURN_ADDRESS_OFFSET];

                data[returnAddress] = data[address1] + data[address2];
            } else if (data[currentPos] == OP_MULT) {
                int address1 = data[currentPos + ARG1_OFFSET];
                int address2 = data[currentPos + ARG2_OFFSET];
                int returnAddress = data[currentPos + RETURN_ADDRESS_OFFSET];

                data[returnAddress] = data[address1] * data[address2];
            } else {
                assert false : "Unknown opcode " + data[currentPos];
            }
            currentPos += 4;
        }
        return data[0];
    }

    void part1(int[] data) {
        data[1] = 12;
        data[2] = 2;
        writer("Part 1 answer: " + runIntCode(data));
    }

    final int PART2_DESIRED_OUTPUT = 19690720;

    void part2(int[] data) {
        boolean finished = false;
        for (int i = 0; (i < 100) && (!finished); i++) {
            for (int j = 0; j < 100; j++) {
                data[0] = 0;
                data[1] = i;
                data[2] = j;

                try {
                    int result = runIntCode(data.clone());
                    if (result == PART2_DESIRED_OUTPUT) {
                        finished = true;
                        break;
                    }
                } catch (ArrayIndexOutOfBoundsException e) {
                    continue;
                }
            }
        }
        if (finished) {
            writer("Part 2 answer: " + (100 * data[1] + data[2]));
        } else {
            writer("Part 2 answer not found");
        }
    }

    @Override
    void run(Stream<String> input) {
        int[] data = input
                .flatMap(x -> Stream.of(x.split(",")))
                .mapToInt(Integer::parseInt).toArray();
        part1(data.clone());
        part2(data);
    }
}
