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
        self.playable = None
        self.age = None
        self.binit = True

    def __deepcopy__(self, memo):
        return None

    def move(self, newstate):
        self.state = newstate
        handsize = self.state.hands[self.number].size

        if self.binit:
            self.playable = []
            self.age = []
            for i in range(len(self.state.hands)):
                self.playable.append([False for j in range(handsize)])
                self.age.append([handsize - j - 1 for j in range(handsize)])
            self.binit = False

        for i in range(len(self.playable[self.number])):
            if self.playable[self.number][i]:
                return Action("play", i, None)

        playerlist = range(len(self.state.hands))
        playerlist = playerlist[self.number + 1:] + playerlist[:self.number]

        if self.state.hints > 0:
            for player in playerlist:
                for card in self.state.hands[player].cards:
                    if self.legal(card):
                        for type in ["number", "color"]:
                            if self.state.hands[player].cards[self.youngest(player, self.hintcards(type, player, card))] == card:
                                print "hinting", card.number, card.color, "pos", self.state.hands[player].cards.index(card), "player", player + 1
                                return Action(type, self.state.hands[player].cards.index(card), player)
        
        return Action("discard", len(self.state.hands[self.number].info) - 1, None)

    def rearrange(self, newstate):
        self.oldstate = self.state
        self.state = newstate
        curplayer = self.state.curplayer
                        
        handsize = self.state.hands[self.number].size
        permute = list(range(handsize))

        if self.binit:
            self.playable = []
            self.age = []
            for i in range(len(self.state.hands)):
                self.playable.append([False for j in range(handsize)])
                self.age.append([handsize - j - 1 for j in range(handsize)])
            self.binit = False

        if self.state.action.type in ["number", "color"]:
            tplayer = self.state.action.player
            tcard = self.youngest(tplayer, self.state.action.cards)
            tage = self.age[tplayer].pop(tcard)
            del(self.playable[tplayer][tcard])
            self.playable[tplayer].insert(0, True)
            self.age[tplayer].insert(0, tage)
            if tplayer == self.number:
                print "player", self.number + 1, "received hint pos", tcard
                tpos = permute.pop(tcard)
                permute.insert(0, tpos)

        if self.state.action.type in ["play", "discard"]:
            pcard = self.state.action.cards
            del(self.playable[curplayer][pcard])
            del(self.age[curplayer][pcard])
            self.age[curplayer] = [a + 1 for a in self.age[curplayer]]

            if self.oldstate == None or self.state.hands[curplayer].size == self.oldstate.hands[curplayer].size:
                pos = 0
                if False in self.playable[curplayer]:
                    pos = self.playable[curplayer].index(False)
                self.playable[curplayer].insert(pos, False)
                self.age[curplayer].insert(pos, 0)
                if curplayer == self.number:
                    del(permute[handsize - 1])
                    permute.insert(pos, handsize - 1)

        return permute

    def scan(self, newstate):
        self.state = newstate

    def legal(self, card):
        match = False
        for i in range(len(self.playable)):
            if i != self.number:
                for j in range(len(self.playable[i])):
                    if self.playable[i][j]:
                        qcard = self.state.hands[i].cards[j]
                        if card.number == qcard.number and card.color == qcard.color:
                            match = True
        if self.state.stacks[card.color] == card.number and match == False:
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
        # print result
        return result

    def youngest(self, target, cards):
        mincard = None
        for card in cards:
            if (mincard == None or self.age[target][card] < self.age[target][mincard]) and not self.playable[target][card]:
                mincard = card
        return mincard
