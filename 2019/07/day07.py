import itertools
import queue
import threading

from .. import intcode, puzzle


class Day07(puzzle.Puzzle):
    year = '2019'
    day = '7'

    def get_data(self):
        return [int(x) for x in self.input_data.splitlines()[0].split(',')]

    def part1(self):
        data = self.get_data()

        thruster_inputs = []

        for i in itertools.permutations(range(5)):
            input_ = [0, 0]
            for phase in i:
                input_[0] = phase
                output = []
                intcode.run_intcode_computer(
                    data,
                    intcode.ListInputDevice(input_),
                    intcode.ListOutputDevice(output),
                    'part 1',
                )
                input_ = [None, output.pop()]
            thruster_inputs.append(input_[1])

        return max(thruster_inputs)

    def part2(self):
        data = self.get_data()
        thruster_inputs = []
        amplifier_indexes = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

        for i in itertools.permutations(range(5, 10)):
            threads = []
            channels = []
            for _ in range(5):
                channels.append(queue.Queue())
            for channel_index, phase in enumerate(i):
                channels[channel_index].put(phase)
                t = threading.Thread(
                    target=intcode.run_intcode_computer,
                    args=(
                        data,
                        intcode.QueueInputDevice(channels[channel_index]),
                        intcode.QueueOutputDevice(
                            channels[(channel_index + 1) % len(channels)]
                        ),
                        amplifier_indexes[channel_index],
                    ),
                )
                threads.append(t)
                t.start()
            try:
                channels[0].put(0)
                amp_e = threads.pop()
                amp_e.join()
            finally:
                for channel in channels:
                    channel.put(intcode.Halt())
                for thread in threads:
                    thread.join()
            amp_e_output_channel = channels.pop(0)  # Or amplifier a input channel
            thruster_input = amp_e_output_channel.get()
            thruster_inputs.append(thruster_input)

        return max(thruster_inputs)

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
