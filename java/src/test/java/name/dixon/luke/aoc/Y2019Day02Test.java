package name.dixon.luke.aoc;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Y2019Day02Test {
    @Test
    void runIntCode() {
        Y2019Day02 day = new Y2019Day02();
        int[] input1 = {1,9,10,3,2,3,11,0,99,30,40,50};
        assertEquals(3500, day.runIntCode(input1));

        int[] input2 = {1,0,0,0,99};
        assertEquals(2, day.runIntCode(input2));

        int[] input3 = {2,3,0,3,99};
        assertEquals(2, day.runIntCode(input3));
        assertEquals(6, input3[3]);

        int[] input4 = {2,4,4,5,99,0};
        assertEquals(2, day.runIntCode(input4));
        assertEquals(9801, input4[5]);

        int[] input5 = {1,1,1,4,99,5,6,0,99};
        assertEquals(30, day.runIntCode(input5));
        assertEquals(2, input5[4]);

        AssertionError thrown = assertThrows(AssertionError.class, () -> {
            int[] input6 = {1,1,1,1,98};
            day.runIntCode(input6);
        });
        assertEquals("Unknown opcode 98", thrown.getMessage());
    }
}