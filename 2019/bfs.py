from abc import ABC
from collections import deque
from typing import Deque


class BFS(ABC):
    def __init__(self):
        self.q: Deque = deque([])

    def initialise_queue(self):
        raise NotImplementedError

    def break_condition(self, state):
        raise NotImplementedError

    def skip_state_condition(self, state):
        raise NotImplementedError

    def add_to_visited(self, state):
        raise NotImplementedError

    def get_neighbours(self, state):
        raise NotImplementedError

    def process_neighbour(self, state, neighbour):
        raise NotImplementedError

    def search(self):
        self.initialise_queue()
        while len(self.q) > 0:
            state = self.q.popleft()

            if self.skip_state_condition(state):
                continue

            self.add_to_visited(state)

            if self.break_condition(state):
                # Done, exit successfully
                break

            for neighbour in self.get_neighbours(state):
                self.process_neighbour(state, neighbour)
        else:
            # Finished without hitting break condition
            print('Not found')
            return None

        return state
