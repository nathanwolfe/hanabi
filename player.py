from card import Card
from hand import Hand
from state import State
from deck import Deck
from action import Action

class Player:
    def __init__(self, n):  # n = player number
        self.number = n
        self.state = None
        self.oldstate = None
        self.hplayable = [False, False, False, False, False]
        self.xplayable = []
        self.drew = False

    def rearrange(self, newstate):
        self.oldstate = self.state
        self.state = newstate
        if self.state.action.type in ["number", "color"] and len(self.state.action.cards) == 1:
            if self.state.action.player == self.number:
                self.hplayable[self.state.action.cards[0]] = True
            else:
                self.xplayable.append(self.state.hands[self.state.action.player].cards[self.state.action.cards[0]])
        if self.state.action.type in ["play", "discard"]:
            if self.oldstate.curplayer == self.number:
                del(self.hplayable[self.state.action.cards])
                self.hplayable.append(False)
            else:
                curcard = self.oldstate.hands[self.oldstate.curplayer].cards[self.state.action.cards]
                if curcard in self.xplayable:
                    del(self.xplayable[self.xplayable.index(curcard)])

    def scan(self, newstate):
        self.state = newstate
