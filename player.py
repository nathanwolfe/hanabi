from card import Card
from deck import Deck

HAND_SIZE = 5
"""
I assume 5 for now, this can be reset later on

Note: 0 is the leftmost card, 4 the rightmost (from player perspective)
"""


class Player:
    def __init__(self, c):
        # c should be a list of card objects
        self.cards = c

    def play(self, d, n):
        # d is the deck (should only be one), n is the index 0-4 of the card being played
        # NOT COMPLETE DOES NOT PUT CARD IN A PILE....
        self.cards.pop(n)
        self.draw(d)

    def discard(self, d, disc, n):
        # d is the deck, disc is the discard
        disc.append(self.cards.pop(n))
        self.draw(d)

    def draw(self, d):
        # d is the deck
        self.cards.append(d.pop_card())
