from card import Card
from deck import Deck
from action import Action

import random

HAND_SIZE = 5
"""
I assume 5 for now, this can be reset later on

Note: 0 is the leftmost card, 4 the rightmost (from player perspective)
"""


class Player:
    def __init__(self, c):
        # c should be a list of card objects
        self.cards = c

    def move(self, cs):
        for i in range(len(self.cards)):
            if self.play_is_valid(cs, self.cards[i]):
                return Action("play", [i], None, None)
        return Action("discard", [0], None, None)

    def play_is_valid(self, cs, c):
        # NEEDS TO BE FIXED SOON. THIS IS EXACT COPY OF is_valid()
        # (if we're fine with redundancy, this is ok)
        if cs[c.color] is c.number:
            return True
        return False
