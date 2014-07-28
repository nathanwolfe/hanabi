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
        #knownlist = []
        #for i in range(state.hands[self.number].size):
            #if state.hands[self.number].info[i][0] != -1 or state.hands[self.number].info[i][1] != -1:
                #knownlist.append[i]
        
        #nextplayer = (state.curplayer + 1) % nplayers
        #if state.hints > 0 and state.players[nextplayer].is_last(state, 0):
            #print "Critical hint given"
            #a = Action("number", 0, nextplayer)
            #state.players[nextplayer].hintlist.append([self.number, a])
            #return a
        # Same as before, play a card if you know what it is.
        for i in range(state.hands[self.number].size):
            if self.playable(state.hands[self.number].info[i][0], state.hands[self.number].info[i][1], state.stacks):
                print "Played a card."
                return Action("play", i, None)
            if state.hands[self.number].info[i][1] != -1:
            #for j in range(len(state.stacks)):
            #for j in range(5):
             #   if self.playable(j, state.hands[self.number].info[i][1], state.stacks):  # state.stacks[j] == state.hands[self.number].info[i][1]:
                print "Played a card, only knew number."
                print str(state.hands[self.number].info)
                return Action("play", i, None)
        # Extended play: basically, checks the number of cards that are the same color; if two or more cards are the same color, the AI will play the newest card with that color. curcolor = number referring to current color; colnumbers = list of curcolor values for each color
        curcolor = 0
        colnumbers = [0, 0, 0, 0, 0]
        while curcolor <= 4:
            for j in range(len(state.hands[self.number].cards)):
                colcards = []
                if state.hands[self.number].info[j][0] == curcolor:
                    colnumbers[curcolor] += 1
                    colcards.append(state.hands[self.number].cards[j])
            if colnumbers[curcolor] >= 2:
                return Action("play", self.newest_card(colcards), None)
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
                        if c not in badcards and self.playable(c.color, c.number, state.stacks) and [c.color, c.number] not in clist:
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
            for i in range(nplayers):
                if i == self.number:
                    continue
                for j in range(state.hands[i].size):
                    c = state.hands[i].cards
                    if state.hands[i].cards[j].color == curcolor and c[j] is self.newest_card(c) and c[j] not in badcards and self.playable(c[j].color, c[j].number, state.stacks):
                        a = Action("color", j, i)
                        state.players[i].hintlist.append([self.number, a])
                        print "hinting color " + str(j) + "; newest card is playable"
                        return a
            curcolor += 1

        # If there is nothing else to do, discard the oldest card.
        print "Nothing else to do; discarding"
        return Action("discard", 0, None)

    def move_old(self, state):  # state = current state of the game which is has player's own hand as empty list and deck as list of dummy cards (red 1s)
        # temporary example function
        # for i in range(len(self.cards)):
        #    if self.play_is_valid(cs, self.cards[i]):
        #        return Action("play", i, None)
        # If you know what a card is and it's playable, play it.
        for i in range(state.hands[self.number].size):
            if self.playable(state.hands[self.number].info[i][0], state.hands[self.number].info[i][1], state.stacks):
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
        # If someone has something playable, hint that.
        for i in range(len(state.players)):
            if i == self.number:
                continue
            for j in range(state.hands[i].size):
                #print "size: " + str(len(state.hands[i].cards)) + "; " + str(j)
                if self.playable(state.hands[i].cards[j].color, state.hands[i].cards[j].number, state.stacks):
                    if state.hands[i].info[j][0] == -1:
                        print "Hinting color: " + str(j) + " of P" + str(i + 1)
                        return Action("color", j, i)
                    if state.hands[i].info[j][1] == -1:
                        print "Hinting number: " + str(j) + " of P" + str(i + 1)
                        return Action("number", j, i)
        print "Nothing hintable, discarding."
        # Can't do anything immediately helpful, so let's just discard cards we don't have info about. If we already have max hints, whatever.
        return Action("discard", 0, None)

    def rearrange(self, state):  # state: same as in move()
        # Rearrange your hand if you want to
        # takes the hand into two parts - moves older cards to the left (nearer to discard) and known cards to the right (or 5's)
        move_right = []
        move_left = []
        for i in range(state.hands[self.number].size):
            if (not state.hands[self.number].info[i][0] == -1 and not state.hands[self.number].info[i][1] == -1) or self.is_last(state, i):
                move_right.append(i)
            else:
                move_left.append(i)
        # now split up these cards into order of preference
        last = []
        play = []
        rest = []
        for i in range(len(move_right)):
            if self.is_last(state, i):
                last.append(i)
            elif self.playable(state.hands[self.number].info[i][0], state.hands[self.number].info[i][1], state.stacks):
                play.append(i)
            else:
                rest.append(i)
        return move_left + rest + play + last

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

    def is_last(self, state, n):
        # function determines whether a card is the last of its kind
        # NOTE: If the card is a red 1, and a red 1 has been successfully played in the past, this will still return FALSE even if this is the last red 1
        card_color = state.hands[self.number].info[n][0]
        card_num = state.hands[self.number].info[n][1]
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
            assert card_num == 1
            return True

    def scan(self, state):
        pass
