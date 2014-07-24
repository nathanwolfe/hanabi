from card import Card
from deck import Deck
from action import Action

HAND_SIZE = 5
"""
I assume 5 for now, this can be reset later on

Note: 0 is the leftmost card, 4 the rightmost (from player perspective)
"""


class Player:
    def __init__(self, c):
        # c should be a list of card objects
        self.cards = c

    def move(self):
        return Action("play", [0], None, None)
