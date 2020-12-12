package name.dixon.luke.aoc.iterables;

import org.junit.jupiter.api.Test;

import java.util.Iterator;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class CombinationsTest {

    @Test
    void iteratork1() {
        Combinations comb = new Combinations(3, 1);
        Iterator<List<Integer>> it = comb.iterator();
        assertTrue(it.hasNext());
        List<Integer> l = it.next();
        assertEquals(1, l.size());
        assertEquals(0, l.get(0));

        assertTrue(it.hasNext());
        l = it.next();
        assertEquals(1, l.size());
        assertEquals(1, l.get(0));

        assertTrue(it.hasNext());
        l = it.next();
        assertEquals(1, l.size());
        assertEquals(2, l.get(0));

        assertFalse(it.hasNext());
    }

    @Test
    void iteratork2() {
        Combinations comb = new Combinations(3, 2);
        Iterator<List<Integer>> it = comb.iterator();
        assertTrue(it.hasNext());
        List<Integer> l = it.next();
        assertEquals(2, l.size());
        assertEquals(0, l.get(0));
        assertEquals(1, l.get(1));

        assertTrue(it.hasNext());
        l = it.next();
        assertEquals(2, l.size());
        assertEquals(0, l.get(0));
        assertEquals(2, l.get(1));

        assertTrue(it.hasNext());
        l = it.next();
        assertEquals(2, l.size());
        assertEquals(1, l.get(0));
        assertEquals(2, l.get(1));

        assertFalse(it.hasNext());
    }

    @Test
    void iteratork3() {
        Combinations comb = new Combinations(4, 3);
        Iterator<List<Integer>> it = comb.iterator();
        assertTrue(it.hasNext());
        List<Integer> l = it.next();
        assertEquals(3, l.size());
        assertEquals(0, l.get(0));
        assertEquals(1, l.get(1));
        assertEquals(2, l.get(2));

        assertTrue(it.hasNext());
        l = it.next();
        assertEquals(3, l.size());
        assertEquals(0, l.get(0));
        assertEquals(1, l.get(1));
        assertEquals(3, l.get(2));

        assertTrue(it.hasNext());
        l = it.next();
        assertEquals(3, l.size());
        assertEquals(0, l.get(0));
        assertEquals(2, l.get(1));
        assertEquals(3, l.get(2));

        assertTrue(it.hasNext());
        l = it.next();
        assertEquals(3, l.size());
        assertEquals(1, l.get(0));
        assertEquals(2, l.get(1));
        assertEquals(3, l.get(2));

        assertFalse(it.hasNext());
    }
}