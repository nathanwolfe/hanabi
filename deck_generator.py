"""
Generates a random permutation of Cards
"""
from card import Card
from deck import Deck
import random
"""
Creating a full_list of cards
"""

list_1 = [Card(i % 5, i / 5, None) for i in range(0, 25)]  # one copy of each card
list_2 = [Card(i % 5, i / 5, None) for i in range(0, 20)]
list_3 = [Card(j, 0, None) for j in range(0, 5)]
full_list = list_1 + list_2 + list_3


def generate():
    # Generate random number, pull the card at that index from full_list, add to final_list.
    final_list = []
    for i in range(50):
        curr_card = random.randint(0, len(full_list) - 1)
        full_list[curr_card].ID = i
        final_list.append(full_list.pop(curr_card))
    final_list[5].number = 4
    return Deck(final_list)
