package name.dixon.luke.aoc;

import reactor.core.publisher.ConnectableFlux;
import reactor.core.publisher.Flux;

import java.io.PrintStream;
import java.util.stream.Stream;

public class Y2019Day01 extends Day {
    public Y2019Day01() {
    }

    public Y2019Day01(PrintStream printStream) {
        super(printStream);
    }

    static protected int calcFuel(int x) {
        return x / 3 - 2;
    }

    static protected int calcFuel2(int x) {
        int fuelRequired = calcFuel(x);
        if (fuelRequired < 0) {
            return 0;
        }
        return fuelRequired + calcFuel2(fuelRequired);
    }

    public void run(Stream<String> input) {
        ConnectableFlux<Integer> f = Flux.fromStream(input.mapToInt(Integer::parseInt).boxed()).publish();
        f.map(Y2019Day01::calcFuel)
                .reduce(0, Integer::sum)
                .subscribe(x -> writer("Part 1 answer: " + x));
        f.map(Y2019Day01::calcFuel2)
                .reduce(0, Integer::sum)
                .subscribe(x -> writer("Part 2 answer: " + x));
        f.connect();
    }
}
