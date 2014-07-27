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

    def move(self, state):
        #Same as before, play a card if you know what it is.
        for i in range(state.hands[self.number].size):
            if self.playable(state.hands[self.number].info[i][0], state.hands[self.number].info[i][1], state.stacks):
                print "Played a card."
                return Action("play", i, None)
        #If there are no hints left, and no playable cards, discard the oldest with no knowledge.
        if state.hints == 0:
            print "No hints, discarding."
            # rearrange() should place the card we want to discard in the 0 position
            return Action("discard", 0, None)
        #If we can/want to give a hint, this is where that happens
        #Analyze state, hands, and the piles to determine which cards are of most importance
        #Next, run that card through various algorithms to see if which will clue the desire to play that card best
        goodPlays = []
        possDiscs = []
        for i in range(len(state.players)):
            if i == self.number:
                continue
            for j in range(state.hands[i].size):
                if self.playable(state.hands[i].cards[j].color, state.hands[i].cards[j].number, state.stacks):
                    goodPlays.append([i, j])
                elif state.stacks[state.hands[i].cards[j].color] > state.hands[i].cards[j].number:
                    #This is true if the card in question has already been played.  Then it may be clued for discard
                    possDiscs.append([i, j])
        # what does this do...?
        for x in goodPlays:
            pass

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
        return move_left + move_right

    def playable(self, color, number, stacks):  # Is the card guaranteed playable on stacks (list)?
        # color and number should be -1 if unknown
        # print str(color) + " " + str(number) + " -> " + str(stacks[color]) + " " + str(number)
        if color == -1 or number == -1:
            return False
        if stacks[color] == number:
            return True
        else:
            return False

    # these took a while to make surprisingly.
    def newest_card(self, state):
        return max(state.hands[self.number].cards, key=attrgetter("turn_drawn"))

    def oldest_card(self, state):
        return min(state.hands[self.number].cards, key=attrgetter("turn_drawn"))

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
