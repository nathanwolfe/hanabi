from card import Card
from deck import Deck
from action import Action

import random

"""
This is an example player file. AI developers should be able to specify their own players later.
"""


class Player:
    def __init__(self, n):  # n = player number
        self.number = n
        # queue is card to be played
        self.queue = []

    def move(self, state):  # state = current state of the game which is has player's own hand as empty list and deck as list of dummy cards (red 1s)
        # temporary example function
        # for i in range(len(self.cards)):
        #    if self.play_is_valid(cs, self.cards[i]):
        #        return Action("play", i, None)
        # If there's anything in the queue, play it.
        if len(self.queue) > 0:
            return Action("play", self.queue.pop(0), None)
        # If you know what a card is and it's playable, play it.
        for i in range(state.hands[self.number].size):
            if self.playable(state.hands[self.number].info[i][0], state.hands[self.number].info[i][1], state.stacks) == True:
                print "Played a card."
                return Action("play", i, None)
        # If there are no hints left, discard whatever you have the least info about. I could optimize this to discard less valuable cards, but I won't.
        if state.hints == 0:
            print "No hints, discarding."
            # Look through cards, discard something with no info.
            for i in range(state.hands[self.number].size):
                if state.hands[self.number].info[i][0] == -1 and state.hands[self.number].info[i][1] == -1:
                    return Action("discard", i, None)
            # So everything has info, so let's discard something with only one piece of info.
            for i in range(state.hands[self.number].size):
                if state.hands[self.number].info[i][0] == -1 or state.hands[self.number].info[i][1] == -1:
                    return Action("discard", i, None)
            # Whatever, let's just discard something.
            return Action("discard", 0, None)
        #print "Nothing playable."
        # If someone has something playable that can be hinted unambiguously, hint that.
        for i in range(len(state.players)):
            if i == self.number: 
                continue
            for j in range(state.hands[i].size):
                #print "size: " + str(len(state.hands[i].cards)) + "; " + str(j)
                if self.playable(state.hands[i].cards[j].color, state.hands[i].cards[j].number, state.stacks):
                    if state.hands[i].info[j][0] == -1 and self.unique(state.hands[i].cards[j].color, state.hands[i].cards, 0):
                        print "Hinting color: " + str(j) + " of P" + str(i)
                        return Action("color", j, i)
                    if state.hands[i].info[j][1] == -1 and self.unique(state.hands[i].cards[j].number, state.hands[i].cards, 1):
                        print "Hinting number: " + str(j) + " of P" + str(i)
                        return Action("number", j, i)
        # If someone has something playable, hint that.
        for i in range(len(state.players)):
            if i == self.number: 
                continue
            for j in range(state.hands[i].size):
                #print "size: " + str(len(state.hands[i].cards)) + "; " + str(j)
                if self.playable(state.hands[i].cards[j].color, state.hands[i].cards[j].number, state.stacks):
                    if state.hands[i].info[j][0] == -1:
                        print "Hinting color: " + str(j) + " of P" + str(i)
                        return Action("color", j, i)
                    if state.hands[i].info[j][1] == -1:
                        print "Hinting number: " + str(j) + " of P" + str(i)
                        return Action("number", j, i)
        print "Nothing hintable, discarding."
        # Can't do anything immediately helpful, so let's just discard cards we don't have info about. If we already have max hints, whatever.        
        for i in range(state.hands[self.number].size):
            if state.hands[self.number].info[i][0] == -1 and state.hands[self.number].info[i][1] == -1:
                return Action("discard", i, None)
        for i in range(state.hands[self.number].size):
            if state.hands[self.number].info[i][0] == -1 or state.hands[self.number].info[i][1] == -1:
                return Action("discard", i, None)
        return Action("discard", 0, None)

    def rearrange(self, state):  # state: same as in move()
        # Rearrange your hand if you want to
        # This is the default permutation.
        return [i for i in range(state.hands[self.number].size)]

    def scan(self, state):  # state: same as in move()
        # Look around if you want
        # If someone hinted this player unambiguously, add that to a queue.
        if (state.action.type == "number" or state.action.type == "color") and state.action.player == self.number and len(state.action.cards) == 1:
            self.queue.append(state.action.cards[0])
        # If someone played a card, clear the queue since it might not be playable. (This could be optimized but w/e.)
        if state.action.type == "play":
            self.queue = []
        
    
    # This function isn't required; I'm implementing this to make things easier
    def playable(self, color, number, stacks):  # Is the card guaranteed playable on stacks (list)?
        # color and number should be -1 if unknown
        # print str(color) + " " + str(number) + " -> " + str(stacks[color]) + " " + str(number)
        if color == -1 or number == -1:
            return False
        if stacks[color] == number:
            return True
        else:
            return False
    
    def unique(self, value, cards, type):  # Checks uniqueness of a value in a hand.
        #type = 0 -> color, type = 1 -> number
        num = 0
        for card in cards:
            if (type == 0 and value == card.color) or (type == 1 and value == card.number):
                num += 1
        if num == 1:
            return True
        return False
