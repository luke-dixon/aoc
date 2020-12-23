package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;

public class Y2020Day08 extends Day {
    public Y2020Day08() {
        super();
    }

    public Y2020Day08(PrintStream printStream) {
        super(printStream);
    }

    static class Computer {
        long accumulator;
        int instructionPointer;

        Computer() {
            accumulator = 0;
            instructionPointer = 0;
        }
    }

    static abstract class Instruction {
        abstract void apply(Computer computer);
    }

    static class AccInstruction extends Instruction {
        long value;

        AccInstruction(long aValue) {
            value = aValue;
        }

        @Override
        public void apply(Computer computer) {
            computer.accumulator += value;
            computer.instructionPointer++;
        }
    }

    static class JmpInstruction extends Instruction {
        long value;

        JmpInstruction(long aValue) {
            value = aValue;
        }

        @Override
        public void apply(Computer computer) {
            computer.instructionPointer += value;
        }
    }

    static class NopInstruction extends Instruction {
        long value;

        NopInstruction(long aValue) {
            value = aValue;
        }

        @Override
        public void apply(Computer computer) {
            computer.instructionPointer++;
        }
    }

    long part1(Instruction[] instructions) {
        Computer computer = new Computer();

        Set<Integer> seen = new HashSet<>();

        while (!seen.contains(computer.instructionPointer)) {
            seen.add(computer.instructionPointer);
            Instruction instruction = instructions[computer.instructionPointer];
            instruction.apply(computer);
        }

        return computer.accumulator;
    }

    long part2(Instruction[] instructions) {
        for (int i = 0; i < instructions.length; i++) {
            Instruction origInstruction = instructions[i];

            // Patch original instruction
            if (origInstruction instanceof JmpInstruction) {
                JmpInstruction jmpInstruction = (JmpInstruction) origInstruction;
                instructions[i] = new NopInstruction(jmpInstruction.value);
            } else if (origInstruction instanceof NopInstruction) {
                NopInstruction nopInstruction = (NopInstruction) origInstruction;
                instructions[i] = new JmpInstruction(nopInstruction.value);
            } else {
                continue;
            }

            Computer computer = new Computer();
            Set<Integer> seen = new HashSet<>();

            try {
                while (!seen.contains(computer.instructionPointer)) {
                    seen.add(computer.instructionPointer);
                    Instruction instruction = instructions[computer.instructionPointer];
                    instruction.apply(computer);
                }
            } catch (ArrayIndexOutOfBoundsException e) {
                if (computer.instructionPointer == instructions.length) {
                    return computer.accumulator;
                }
            }

            instructions[i] = origInstruction;
        }

        throw new RuntimeException("Answer not found");
    }

    Instruction instructionFactory(String instructionWithArg) {
        String op = instructionWithArg.split(" ")[0];
        int value = Integer.parseInt(instructionWithArg.split(" ")[1]);

        Map<String, Class<? extends Instruction>> map = new HashMap<>();
        map.put("jmp", JmpInstruction.class);
        map.put("acc", AccInstruction.class);
        map.put("nop", NopInstruction.class);

        try {
            Constructor<? extends Instruction> constructor = map.get(op).getDeclaredConstructor(long.class);
            return constructor.newInstance(value);
        } catch (NoSuchMethodException | InstantiationException | IllegalAccessException | InvocationTargetException e) {
            e.printStackTrace();
            throw new RuntimeException("Problem initialising class");
        }
    }

    @Override
    void run(Stream<String> input) {
        Instruction[] instructions = input.map(this::instructionFactory).toArray(Instruction[]::new);

        writer("Answer part 1: " + part1(instructions));
        writer("Answer part 2: " + part2(instructions));
    }
}
