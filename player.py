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

    def move(self, newstate):
        self.state = newstate

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
                self.drew = True
            else:
                curcard = self.oldstate.hands[self.oldstate.curplayer].cards[self.state.action.cards]
                if curcard in self.xplayable:
                    del(self.xplayable[self.xplayable.index(curcard)])
        for i in range(5):
            if -1 not in self.state.hands[self.number].info[i]:
                self.hplayable[i] = True
        for i in range(len(self.state.hands)):
            if i != self.number:
                for j in range(5):
                    if -1 not in self.state.hands[i].info[j] and self.state.hands[i].cards[j] not in self.xplayable:
                        self.xplayable.append(self.state.hands[i].cards[j])
        if self.drew:
            del(self.hplayable(4))
        hasinfo = [[False, i] for i in range(len(self.hplayable))]
        for i in range(len(hasinfo)):
            if self.hplayable[i] or self.state.hands[self.number].info[i] != [-1, -1]:
                hasinfo[i][0] = True
        hasinfo.sort(reverse=True, key=lambda card: card[0])
        if self.drew:
            if False in zip(*hasinfo)[0]: # if the set of 0th elements of hasinfo has False in it
                hasinfo.insert(zip(*hasinfo)[0].index(False), [False, 4])
            else:
                hasinfo.append([False, 4])
            self.hplayable.append(False)
        temphplayable = [self.hplayable[hasinfo[i][1]] for i in range(5)]
        self.hplayable = temphplayable
        return [hasinfo[i][1] for i in range(5)]

    def scan(self, newstate):
        self.state = newstate
