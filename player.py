from card import Card
from deck import Deck
from action import Action

import random

"""
This is an example player file. AI developers should be able to specify their own players later.
"""


class Player:
    def __init__(self, n): # n = player number
        self.number = n

    def move(self, state): # state = current state of the game which is has player's own hand as empty list and deck as list of dummy cards (red 1s)
		#temporary example function
        #for i in range(len(self.cards)):
        #    if self.play_is_valid(cs, self.cards[i]):
        #        return Action("play", i, None)
        return Action("discard", 0, None)
		
	def rearrange(self, state):	# state: same as in move()
		# Rearrange your hand if you want to
		return [i for i in range(len(state.hands[(self.number + 1) % 2].cards))] #get non-self's hand length
	
	def scan(self, state): # state: same as in move()
		# Look around if you want
	
	# Is this necessary? 
    def play_is_valid(self, cs, c): 
        # NEEDS TO BE FIXED SOON. THIS IS EXACT COPY OF is_valid()
        # (if we're fine with redundancy, this is ok)
        if cs[c.color] is c.number:
            return True
        return False
