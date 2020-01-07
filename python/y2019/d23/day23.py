import itertools
import queue
import threading
from collections import defaultdict, deque

from .. import intcode, puzzle


class QueueInputDevice(intcode.InputDevice):
    def __init__(self, input_queue: queue.Queue):
        self.queue = input_queue

    def read(self) -> int:
        try:
            return self.queue.popleft()
        except IndexError:
            return -1


class QueueOutputDevice(intcode.OutputDevice):
    def __init__(self, output_queue: queue.Queue):
        self.queue = output_queue

    def write(self, value: int) -> None:
        self.queue.append(value)


class Day23(puzzle.Puzzle):
    year = '2019'
    day = '23'

    def get_data(self):
        return [int(x) for x in self.input_data.splitlines()[0].split(',')]

    def run(self):
        threads = []
        inputs = []
        outputs = []
        for i in range(50):
            inputs.append(deque([]))
        for i in range(50):
            outputs.append(deque([]))
        for i in range(50):
            data = defaultdict(int)
            for j, d in enumerate(self.get_data()):
                data[j] = d
            inputs[i].append(i)
            t = threading.Thread(
                target=intcode.run_intcode_computer,
                args=(
                    data,
                    QueueInputDevice(inputs[i]),
                    QueueOutputDevice(outputs[i]),
                    str(i),
                ),
            )
            threads.append(t)
            t.start()
        try:
            last_y = None
            answer = None
            idle_count = 0
            sent_to_0 = set()
            while True:
                if all([len(inputs[i]) == 0 for i in range(50)]):
                    idle_count += 1
                else:
                    idle_count = 0
                if idle_count >= 10 and answer is not None:
                    print(f'Sending {answer[0]} {answer[1]} from NAT to 0')
                    print([len(inputs[i]) for i in range(50)])
                    if answer[1] == last_y:
                        print(f'Part 2 answer: {answer}, {answer[1]}')
                        print('#####################################')
                        print('#####################################')
                        print('#####################################')
                        print('#####################################')
                        print('#####################################')
                        print('#####################################')
                        print('#####################################')
                    last_y = answer[1]
                    inputs[0].append(int(answer[0]))
                    inputs[0].append(int(answer[1]))
                    answer = None

                for i in range(50):
                    if len(outputs[i]) >= 3:
                        idle_count = 0
                        address = outputs[i].popleft()
                        x = outputs[i].popleft()
                        y = outputs[i].popleft()
                        if address == 255:
                            print(f'Sending {x} {y} from {i} to {address}')
                            print(x, y)
                            print(f'Answer {y}')
                            answer = (x, y)
                        else:
                            #print(f'Sending {x} {y} from {i} to {address}')
                            inputs[address].append(x)
                            inputs[address].append(y)
        finally:
            for channel in inputs:
                channel.append(intcode.Halt())
            for thread in threads:
                thread.join()
        return
