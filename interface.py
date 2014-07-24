"""
Project Advisor: Mira Bernstein
Project Members: Andrew Li, Nathan Wolfe, Jerry Wu, Patrick Revilla, Alvin Kao, Cristina ________, Alex Chen, hope I didn't forget anyone
"""
from card import Card
from state import State
from deck import Deck
from game import Game
from player import Player
import deck_generator  # this is one of our own files


def main():
    deck_list = deck_generator.generate()
    deck = Deck(deck_list)
    # print deck.to_string()

    discard_pile = []
    lives = 3
    hints = 8
    card_stacks = [[0 for i in range(5)] for j in range(4)]

    p1_hand = []
    for i in range(5):
        p1_hand.append(deck.pop_card())
    p1 = Player(p1_hand)
    for i in p1.cards:
        print i.to_string()
    p1.play(deck, 2)
    p1.discard(deck, discard_pile, 1)
    for i in p1.cards:
        print i.to_string()
    print "-----------"
    print discard_pile[0].to_string()

main()
