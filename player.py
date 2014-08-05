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
        self.hage = [4, 3, 2, 1, 0]
        self.xage = {}
        self.drew = False
        self.initage = True

    def move(self, newstate):
        self.state = newstate
        if self.initage:
            for i in range(len(self.state.hands)):
                if i != self.number:
                    for j in range(len(self.state.hands[i].cards)):
                        self.xage[self.state.hands[i].cards[j]] = 4 - j
            self.initage = False

        for i in range(len(self.hplayable)):
            if self.hplayable[i]:
                return Action("play", i, None)

        playerlist = range(len(self.state.hands))
        playerlist = playerlist[self.number + 1:] + playerlist[:self.number]

        for player in playerlist:
            for card in self.state.hands[player].cards:
                if self.legal(card):
                    for type in ["number", "color"]:
                        if self.state.hands[player].cards[self.youngest(player, self.hintcards(type, player, card))] == card:
                            return Action(type, self.state.hands[player].cards.index(card), player)
        
        return Action("discard", len(self.state.hands[self.number].info) - 1, None)

    def rearrange(self, newstate):
        self.oldstate = self.state
        self.state = newstate
        if self.initage:
            for i in range(len(self.state.hands)):
                if i != self.number:
                    if i == self.state.curplayer and self.state.action.type == "discard":
                        for j in range(len(self.state.hands[i].cards)):
                            self.xage[self.state.hands[i].cards[j]] = 5 - j
                        self.xage[self.state.hands[i].cards[0]] = 0
                    else:
                        for j in range(len(self.state.hands[i].cards)):
                            self.xage[self.state.hands[i].cards[j]] = 4 - j
            self.initage = False
        else:
            for card in self.state.hands[self.state.curplayer].cards:
                if card in self.xage:
                    self.xage[card] += 1
                else:
                    self.xage[card] = 0
                        
        handsize = len(self.state.hands[self.number].info)
        if self.state.action.type in ["number", "color"]:
            target = self.state.action.player
            if target == self.number:
                mincard = None
                for card in self.state.action.cards:
                    if mincard == None or self.hage[card] < self.hage[mincard]:
                        mincard = card
                self.hplayable[mincard] = True
            else:
                self.xplayable.append(self.state.hands[target].cards[self.youngest(target, self.state.action.cards)])
        if self.state.action.type in ["play", "discard"]:
            if self.state.curplayer == self.number:
                del(self.hplayable[self.state.action.cards])
                self.hplayable.append(False)
                self.drew = True
            elif oldstate != None:
                curcard = self.oldstate.hands[self.state.curplayer].cards[self.state.action.cards]
                if curcard in self.xplayable:
                    del(self.xplayable[self.xplayable.index(curcard)])
        for i in range(handsize):
            if -1 not in self.state.hands[self.number].info[i]:
                self.hplayable[i] = True
        for i in range(len(self.state.hands)):
            if i != self.number:
                for j in range(len(self.state.hands[i].cards)):
                    if -1 not in self.state.hands[i].info[j] and self.state.hands[i].cards[j] not in self.xplayable:
                        self.xplayable.append(self.state.hands[i].cards[j])
        if self.drew:
            del(self.hplayable(handsize - 1))
        hasinfo = [[False, i] for i in range(len(self.hplayable))]
        for i in range(len(hasinfo)):
            if self.hplayable[i] #or self.state.hands[self.number].info[i] != [-1, -1]:
                hasinfo[i][0] = True
        hasinfo.sort(reverse=True, key=lambda card: card[0])
        if self.drew:
            if False in zip(*hasinfo)[0]: # if the set of 0th elements of hasinfo has False in it
                hasinfo.insert(zip(*hasinfo)[0].index(False), [False, handsize - 1])
            else:
                hasinfo.append([False, handsize - 1])
            self.hplayable.append(False)
            self.drew = False
        temphplayable = [self.hplayable[hasinfo[i][1]] for i in range(handsize)]
        self.hplayable = temphplayable
        return [hasinfo[i][1] for i in range(handsize)]

    def scan(self, newstate):
        self.state = newstate

    def legal(self, card):
        match = False
        for qcard in self.xplayable:
            if card.number == qcard.number and card.color == qcard.color:
                match = True
        if self.state.stacks[card.color] == card.number and not match:
            return True
        else:
            return False

    def hintcards(self, type, target, card):
        result = []
        if type == "number":
            for i in range(len(self.state.hands[target].cards)):
                if self.state.hands[target].cards[i].number == card.number:
                    result.append(i)
        else:
            for i in range(len(self.state.hands[target].cards)):
                if self.state.hands[target].cards[i].color == card.color:
                    result.append(i)
        return result

    def youngest(self, target, cards):
        mincard = None
        for card in cards:
            if mincard == None or self.xage[self.state.hands[target].cards[card]] < self.xage[self.state.hands[target].cards[mincard]]:
                mincard = card
        return mincard
