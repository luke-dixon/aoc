package name.dixon.luke.aoc;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class Y2020Day08Test {

    @Test
    void accInstruction() {
        Y2020Day08.Instruction instruction = new Y2020Day08.AccInstruction(5);
        Y2020Day08.Computer computer = new Y2020Day08.Computer();
        assertEquals(0, computer.accumulator);
        assertEquals(0, computer.instructionPointer);

        instruction.apply(computer);

        assertEquals(5, computer.accumulator);
        assertEquals(1, computer.instructionPointer);
    }

    @Test
    void jmpInstruction() {
        Y2020Day08.Instruction instruction = new Y2020Day08.JmpInstruction(5);
        Y2020Day08.Computer computer = new Y2020Day08.Computer();
        assertEquals(0, computer.accumulator);
        assertEquals(0, computer.instructionPointer);

        instruction.apply(computer);

        assertEquals(0, computer.accumulator);
        assertEquals(5, computer.instructionPointer);
    }

    @Test
    void nopInstruction() {
        Y2020Day08.Instruction instruction = new Y2020Day08.NopInstruction(5);
        Y2020Day08.Computer computer = new Y2020Day08.Computer();
        assertEquals(0, computer.accumulator);
        assertEquals(0, computer.instructionPointer);

        instruction.apply(computer);

        assertEquals(0, computer.accumulator);
        assertEquals(1, computer.instructionPointer);
    }

    @Test
    void part1() {
        OutputStream out = new ByteArrayOutputStream();
        Day day = new Y2020Day08(new PrintStream(out));

        List<String> input = Arrays.asList(
            "nop +0",
            "acc +1",
            "jmp +4",
            "acc +3",
            "jmp -3",
            "acc -99",
            "acc +1",
            "jmp -4",
            "acc +6"
        );

        day.run(input.stream());
        assertEquals("Answer part 1: 5\nAnswer part 2: 8\n", out.toString());
    }
}