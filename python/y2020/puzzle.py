from functools import cached_property

from aocd.models import Puzzle as BasePuzzle, User

import argparse


class Puzzle(BasePuzzle):
    def add_additional_args(self, parser):
        pass

    def __init__(self, args=None, user=None):
        args = [] if args is None else args

        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file', type=open, action='store', required=False, dest='file')

        self.add_additional_args(parser)

        self.args = parser.parse_args(args)
        if not user:
            user = User('') if self.args.file else None

        super().__init__(self.year, int(self.day), user=user)

    @cached_property
    def input_data(self):
        if self.args.file:
            return self.args.file.read().strip()
        return super().input_data
