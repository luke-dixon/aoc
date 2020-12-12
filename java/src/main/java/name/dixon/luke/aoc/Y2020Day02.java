package name.dixon.luke.aoc;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

public class Y2020Day02 extends Day {
    public Y2020Day02() {
        super();
    }

    public Y2020Day02(PrintStream printStream) {
        super(printStream);
    }

    interface PasswordPolicy {
        boolean isValid(int rmin, int rmax, char rc, String password);
    }

    static class Password {
        int rmin;
        int rmax;
        char rc;
        String password;

        Password(int rmin, int rmax, char rc, String password) {
            this.rmin = rmin;
            this.rmax = rmax;
            this.rc = rc;
            this.password = password;
        }

        static Password fromData(String rawPassword) {
            String policy = rawPassword.split(": ")[0];
            String password = rawPassword.split(": ")[1];

            String range = policy.split(" ")[0];
            String rc = policy.split(" ")[1];

            int rmin = Integer.parseInt(range.split("-")[0]);
            int rmax = Integer.parseInt(range.split("-")[1]);
            return new Password(rmin, rmax, rc.charAt(0), password);
        }

        boolean isValid(PasswordPolicy policy) {
            return policy.isValid(rmin, rmax, rc, password);
        }
    }

    static class Part1Policy implements PasswordPolicy {
        @Override
        public boolean isValid(int rmin, int rmax, char rc, String password) {
            int occurrences = 0;
            for (char c : password.toCharArray()) {
                if (c == rc) {
                    occurrences++;
                }
            }
            return rmin <= occurrences && occurrences <= rmax;
        }
    }

    static class Part2Policy implements PasswordPolicy {
        @Override
        public boolean isValid(int rmin, int rmax, char rc, String password) {
            return password.toCharArray()[rmin - 1] == rc ^ password.toCharArray()[rmax - 1] == rc;
        }
    }

    int answer(List<Password> passwords, PasswordPolicy policy) {
        int total = 0;
        for (Password password : passwords) {
            if (password.isValid(policy)) {
                total += 1;
            }
        }
        return total;
    }

    @Override
    void run(Stream<String> input) {
        List<Password> passwords = new ArrayList<>();
        input.forEach(rawPassword -> {
            passwords.add(Password.fromData(rawPassword));
        });
        writer("Answer part 1: " + answer(passwords, new Part1Policy()));
        writer("Answer part 2: " + answer(passwords, new Part2Policy()));
    }
}
