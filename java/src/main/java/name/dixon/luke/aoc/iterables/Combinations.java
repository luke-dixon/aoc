package name.dixon.luke.aoc.iterables;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class Combinations implements Iterable<List<Integer>> {
    class CombinationsIterator implements Iterator<List<Integer>> {
        List<Integer> iterators;

        CombinationsIterator() {
            iterators = new ArrayList<>(k);
            for (int i = 0; i < k; i++) {
                iterators.add(i);
            }
        }

        @Override
        public boolean hasNext() {
            return iterators.get(iterators.size() - 1) < n;
        }

        @Override
        public List<Integer> next() {
            List<Integer> result = new ArrayList<>(iterators);

            iterators.set(iterators.size() - 1, iterators.get(iterators.size() - 1) + 1);

            for (int i = iterators.size() - 1; i > 0; i--) {
                if (iterators.get(i) > (n - (iterators.size() - i))) {
                    iterators.set(i - 1, iterators.get(i - 1) + 1);
                    for (int j = i - 1; j < iterators.size() - 1; j++) {
                        iterators.set(j + 1, iterators.get(j) + 1);
                    }
                }
            }

            return result;
        }
    }

    int n;
    int k;

    public Combinations(int n, int k) {
        this.n = n;
        this.k = k;
    }

    @Override
    public CombinationsIterator iterator() {
        return new CombinationsIterator();
    }
}
