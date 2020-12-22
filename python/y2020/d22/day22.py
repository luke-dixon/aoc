from collections import *
from functools import *
from itertools import *
from pprint import pprint

from lib import puzzle


class Day22(puzzle.Puzzle):
    year = '2020'
    day = '22'

    def get_data(self):
        orig_data = self.input_data.splitlines()

#         orig_data = '''Player 1:
# 9
# 2
# 6
# 3
# 1
#
# Player 2:
# 5
# 8
# 4
# 7
# 10'''.splitlines()

        player1, player2 = [], []
        current_player = None
        for line in orig_data:
            if line == 'Player 1:':
                current_player = player1
            elif line == 'Player 2:':
                current_player = player2
            elif line == '':
                pass
            else:
                current_player.append(int(line))

        return player1, player2

    def part1(self):
        player1, player2 = self.get_data()

        deck1 = deque(player1)
        deck2 = deque(player2)

        pprint(deck1)
        pprint(deck2)

        self.game1(deck1, deck2)

        pprint(deck1)
        pprint(deck2)

        winning_deck = deck1 if len(deck1) else deck2
        pprint(winning_deck)

        score = 0
        for i in range(1, len(winning_deck) + 1):
            card = winning_deck.pop()
            print(i, card)
            score += i * card

        return score

    def game1(self, deck1, deck2):
        while len(deck1) and len(deck2):
            top1 = deck1.popleft()
            top2 = deck2.popleft()

            if top1 > top2:
                deck1.append(top1)
                deck1.append(top2)
            elif top2 > top1:
                deck2.append(top2)
                deck2.append(top1)

    def part2(self):
        player1, player2 = self.get_data()

        deck1 = deque(player1)
        deck2 = deque(player2)

        pprint(deck1)
        pprint(deck2)

        winner = self.game2(deck1, deck2)

        winning_deck = deck1 if winner == 1 else deck2

        score = 0
        for i in range(1, len(winning_deck) + 1):
            card = winning_deck.pop()
            score += i * card

        return score

    def game2(self, deck1, deck2):

        game = 1

        def recursive_combat(game, top1, top2, deck1, deck2):
            while len(deck1) > top1:
                deck1.pop()
            while len(deck2) > top2:
                deck2.pop()

            previous_rounds = set()

            # print(f'=== Game {game} ===')
            round = 1
            won_by_knockout = False
            while len(deck1) and len(deck2):
                hashable_decks = ', '.join([str(x) for x in deck1]) + ' - ' + ', '.join([str(x) for x in deck2])
                if hashable_decks in previous_rounds:
                    won_by_knockout = True
                    break
                previous_rounds.add(hashable_decks)

                # print(f'-- Round {round} (Game {game}) --')
                # print(f"Player 1's deck: {', '.join([str(x) for x in deck1])}")
                # print(f"Player 2's deck: {', '.join([str(x) for x in deck2])}")

                top1 = deck1.popleft()
                top2 = deck2.popleft()

                # print(f"Player 1 plays: {top1}")
                # print(f"Player 2 plays: {top2}")

                if top1 <= len(deck1) and top2 <= len(deck2):
                    # recursive combat
                    winner = recursive_combat(game + 1, top1, top2, deque(deck1), deque(deck2))
                    if winner == 1:
                        # print(f"Player 1 wins round {round} of game {game}!")
                        deck1.append(top1)
                        deck1.append(top2)
                    elif winner == 2:
                        # print(f"Player 2 wins round {round} of game {game}!")
                        deck2.append(top2)
                        deck2.append(top1)
                else:
                    if top1 > top2:
                        # print(f"Player 1 wins round {round} of game {game}!")
                        deck1.append(top1)
                        deck1.append(top2)
                    elif top2 > top1:
                        # print(f"Player 2 wins round {round} of game {game}!")
                        deck2.append(top2)
                        deck2.append(top1)

                round += 1

            if won_by_knockout:
                return 1

            if len(deck1) and len(deck2) == 0:
                return 1
            elif len(deck2) and len(deck1) == 0:
                return 2

        return recursive_combat(game, len(deck1), len(deck2), deck1, deck2)

    def run(self):
        print(f'Part 1 Answer: {self.part1()}')
        print(f'Part 2 Answer: {self.part2()}')
