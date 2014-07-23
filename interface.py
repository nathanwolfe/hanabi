"""
Project Advisor: Mira Bernstein
Project Members: Andrew Li, Nathan Wolfe, Jerry Wu, Patrick Revilla, Alvin Kao, Cristina ________, Alex Chen, hope I didn't forget anyone
"""
from card import Card
from state import State
from deck import Deck
from game import Game
import deck_generator  # this is one of our own files


def main():
    deck_list = deck_generator.generate()
    deck = Deck(deck_list)
    print deck.to_string()

main()
