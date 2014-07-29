from card import Card
from deck import Deck
from action import Action
from operator import attrgetter
"""
This is an example player file. AI developers should be able to specify their own players later.
"""


class Player:
    def __init__(self, n):  # n = player number
        self.number = n
        self.hintlist = []  # we need a list of hints because the info list doesn't provide any information about how recent that info was obtained. Hintlist is a list of duples [p, a] where p is the index of the player giving the hint and a is an action.

    def move(self, state, nplayers):
        
        # If we see critical problemos, hint
        for i in range(nplayers):
            if self.is_last(state, state.hands[i].cards[0].color, state.hands[i].cards[0].number, 0):
                # this also needs to be optimized: pick one of the two to hint (here I just went with number)
                return Action("number", 0, i)

        # Same as before, play a card if you know what it is.
        for i in range(state.hands[self.number].size):
            if self.playable(state.hands[self.number].info[i][0], state.hands[self.number].info[i][1], state.stacks):
                print "Played a card."
                return Action("play", i, None)
            if state.hands[self.number].info[i][1] != -1:
            # for j in range(len(state.stacks)):
            # for j in range(5):
                # if self.playable(j, state.hands[self.number].info[i][1], state.stacks):  # state.stacks[j] == state.hands[self.number].info[i][1]:
                print "Played a card, only knew number."
                print str(state.hands[self.number].info)
                return Action("play", i, None)

        """
        last_hints = self.hintlist[max(0, len(self.hintlist) - nplayers):]  # look back at most nplayers many hints
        for i in range(len(last_hints)):
            curhint = last_hints[i]
            if curhint.type == "color" and curhint.player == self.number:  # if the hint is of type color and pertains to us
                # optimize from which color group a card is played later...
                colcards = []
                for j in range(state.hands[self.number].size):  # look at all the cards of the same color as the hint
                    if state.hands[self.number].info[j][0] == state.hands[self.number].info[curhint.cards[0]][0]:  # look carefully
                        colcards.append(state.hands[self.number].cards[j])
                if len(colcards) > 0:  # make sure at least 1 of that color
                    print "played newest card of color " + str(state.hands[self.number].info[curhint.cards[0]][0])
                    print state.hands[self.number].info
                    return Action("play", state.hands[self.number].cards.index(self.newest_card(colcards)), None)

        """
        # If was hinted _last round_ in color form, play newest card
        curcolor = 0
        colnumbers = [0, 0, 0, 0, 0]
        while curcolor <= 4:
            colcards = []
            for j in range(state.hands[self.number].size):
                if state.hands[self.number].info[j][0] == curcolor:
                    colnumbers[curcolor] += 1
                    colcards.append(state.hands[self.number].cards[j])
            if colnumbers[curcolor] >= 1:
                print "played newest card of color " + str(curcolor)
                print state.hands[self.number].info
                return Action(
                    "play", state.hands[self.number].cards.index(self.newest_card(colcards)), None
                )
            # optimization idea: make AI think through all possibilities before deciding what to play
            curcolor += 1

        # If there are no hints left, and no playable cards, discard the oldest with no knowledge.
        if state.hints == 0:
            print "No hints, discarding."
            # rearrange() should place the card we want to discard in the 0 position
            return Action("discard", 0, None)
        # If we can/want to give a hint, this is where that happens
        # The list of badcards [color, number] ensures that no player will accidentally play a card someone else is already going to play
        badcards = []
        for i in range(nplayers):
            if i == self.number:
                continue
            for j in range(len(state.hands[i].info)):
                for k in state.stacks:
                    if state.hands[i].info[j][1] == k:
                        badcards.append([state.hands[i].cards[j].color, state.hands[i].cards[j].number])
                    
        # First, see if the AI can hint a number, all cards of that number being playable.
        curnumber = 0
        sizelist = [[0 for i in range(5)] for j in range(nplayers)]

        while curnumber <= 4:
            for i in range(nplayers):
                if i == self.number:
                    continue
                clist = []
                for j in range(state.hands[i].size):
                    if state.hands[i].cards[j].number == curnumber:
                        c = state.hands[i].cards[j]
                        if [c.color, c.number] not in badcards and self.playable(c.color, c.number, state.stacks) and [c.color, c.number] not in clist:
                            sizelist[i][curnumber] += 1
                            clist.append([c.color, c.number])
                        else:
                            sizelist[i][curnumber] = 0
                            break
            curnumber += 1

        maxvalue = 0
        maxindex = [0, 0]
        for i in range(len(sizelist)):
            for j in range(len(sizelist[i])):
                if sizelist[i][j] > maxvalue:
                    maxvalue = sizelist[i][j]
                    maxindex = [i, j]

        cardindex = -1
        for i in range(len(state.hands[maxindex[0]].cards)):
            if state.hands[maxindex[0]].cards[i].number == maxindex[1]:
                cardindex = i
                break

        #maxvalues = map(max, sizelist)
        #maxindices = [sizelist[i].index(max(sizelist[i])) for i in range(len(sizelist))]
        #hintplayer = maxindices[maxvalues.index(max(maxvalues))]
        #hintnumber = sizelist[hintplayer].index(max(sizelist[hintplayer]))
        #print maxvalues

        if sizelist[maxindex[0]][maxindex[1]] > 0:
            a = Action("number", cardindex, maxindex[0])
            state.players[maxindex[0]].hintlist.append([self.number, a])
            print "hinting a number" + str(maxindex[1]) + ", all cards of which are playable"
            return a

        #if sizelist[hintplayer][hintnumber] > 0:
        #    a = Action("number", hintnumber, hintplayer)
        #    state.players[hintplayer].hintlist.append([self.number, a])
        #    print "hinting a number, all cards of which are playable"
        #    return a

        # Otherwise, see if the AI can hint a color, the newest card of which is playable.
        curcolor = 0
        while curcolor <= 4:
            colcards = []
            for i in range(nplayers):
                if i == self.number:
                    continue
                c = state.hands[i].cards
                for j in range(state.hands[i].size):
                    if c[j].color == curcolor:
                        colcards.append(c[j])
                for j in range(state.hands[i].size):
                    if len(colcards) > 0 and c[j] is self.newest_card(colcards) and [c[j].color, c[j].number] not in badcards and self.playable(c[j].color, c[j].number, state.stacks):
                        a = Action("color", j, i)
                        state.players[i].hintlist.append([self.number, a])
                        print "hinting color " + str(curcolor) + "; newest card is playable"
                        return a
            curcolor += 1

        # If there is nothing else to do, discard the oldest card.
        print "Nothing else to do; discarding"
        return Action("discard", 0, None)

    def rearrange(self, state):  # state: same as in move()
        # Rearrange your hand if you want to
        # takes the hand into two parts - moves older cards to the left (nearer to discard) and known cards to the right (or 5's)
        last = []
        play = []
        known = []
        other = []
        for i in range(state.hands[self.number].size):
            if self.is_last(state, state.hands[self.number].info[i][0], state.hands[self.number].info[i][1], i):
                last.append(i)
            elif self.playable(state.hands[self.number].info[i][0], state.hands[self.number].info[i][1], state.stacks):
                play.append(i)
            elif (not state.hands[self.number].info[i][0] == -1) or (not state.hands[self.number].info[i][1]):
                known.append(i)
            else:
                other.append(i)
        return other + known + play + last

    def find_playable(self, state):
        playable_cards = []
        # h is a number, c is a number
        for h in range(len(state.hands)):
            if h == self.number:
                continue
            for c in range(state.hands[h].size):
                if self.playable(state.hands[h].cards[c].color, state.hands[h].cards[c].number, state.stacks):
                    playable_cards.append([h, c])
        return playable_cards

    def playable(self, color, number, stacks):
        # Is the card guaranteed playable on stacks (list)?
        # color and number should be -1 if unknown
        # print str(color) + " " + str(number) + " -> " + str(stacks[color]) + " " + str(number)
        if color == -1 or number == -1:
            return False
        if stacks[color] == number:
            return True
        else:
            return False

    def newest_card(self, cards):
        return max(cards, key=attrgetter("turn_drawn"))

    def oldest_card(self, cards):
        return min(cards, key=attrgetter("turn_drawn"))

    def is_last(self, state, card_color, card_num, n):
        # function determines whether a card is the last of its kind
        # NOTE: If the card is a red 1, and a red 1 has been successfully played in the past, this will still return FALSE even if this is the last red 1
        counter = 0

        if card_color == -1 or card_num == -1:
            return False
        if card_num == 4:
            return True
        # if card is smaller than the highest card played of its color (see function comments)
        if card_num < state.stacks[card_color]:
            return False
        for i in state.discards:
            if i.color == card_color and i.number == card_num:
                counter += 1

        assert counter <= 2
        # this stuff basically counts # of cards
        if counter == 0:
            return False
        elif counter == 1:
            if card_num == 1 or card_num == 2 or card_num == 3:
                return False
            elif card_num == 0:
                return True
        elif counter == 2:
            assert card_num == 0
            return True

    def scan(self, state):
        if state.action.type == "color" or state.action.type == "number":
            self.hintlist.append(state.action)

