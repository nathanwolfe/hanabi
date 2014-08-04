from card import Card
from deck import Deck
from action import Action
from operator import attrgetter
"""
This is an example player file. AI developers should be able to specify their own players later.
"""


class Player:
    def __init__(self, n, nplayers):  # n = player number
        self.number = n
        self.play_queue = []  # list of cards to be played
        self.all_queues = [[] for i in xrange(nplayers)]

    def move(self, state, nplayers):
        # assume we've figured out all of our variables and rearranged all of our cards.
        """
        Order of Cases:
        critical discard of next person
        there are playable cards in queue
        critical discard of person later one
        give hints to players
        if nothing else can be done, discard
        """
        next_p = (self.number + 1) % nplayers  # generally helpful index

        ''''# Case: critical discard of next person
        next_discard = state.hands[next_p].cards[0]
        if self.is_critical(state, next_discard.color, next_discard.number) and state.hints > 0:
            print "Critical discard hint given."
            return self.warn_critical(state, next_p)'''

        # Case: there are playable cards in queue
        if len(self.play_queue) > 0:
            print "Play_queue: " + str(self.play_queue)
            print "Played the card at index: " + str(self.index_from_ID(state, self.play_queue[0], self.number))
            return Action("play", self.index_from_ID(state, self.play_queue.pop(0), self.number), None)

        """
        # Case: critical discard of person 2 seats ahead
        if not nplayers == 2 and state.hints > 0:
            p = (self.number + 2) % nplayers  # start from next player on
            next_discard = state.hands[p].cards[0]
            if self.is_critical(state, next_discard.color, next_discard.number):
                if state.hints <= 1:
                    print "Attempting to avoid critical discard"
                    return Action("discard", 0, None)
        """

        # Case: give hints to players
        # assuming select_hint returns a triple [player, ID, hint type]
        hint_triple = self.select_hint(state, self.all_queues)
        print hint_triple
        if hint_triple[1] != -1:
            # this print statement needs work...
            print "Hinted to " + str(hint_triple[0]) + " the card at " + str(state.players[hint_triple[0]].index_from_ID(state, hint_triple[1], hint_triple[0])) + "."
            if hint_triple[2] == "color":
                print "Color hinted."
            elif hint_triple[2] == "number":
                print "Number hinted."
            print state.players[hint_triple[0]].index_from_ID(state, hint_triple[1], hint_triple[0])
            return Action(hint_triple[2], state.players[hint_triple[0]].index_from_ID(state, hint_triple[1], hint_triple[0]), hint_triple[0])

        # Case: if nothing else can be done, discard
        print "Discarding."
        return Action("discard", 0, None)

    def analyze(self, state, nplayers):
        received_full = False  # checks if the player has received full information about any one card
        for i in xrange(len(state.hands[self.number].cards)):
            # Checks for full info cards
            i_duple = state.hands[self.number].info[i]
            if self.playable(i_duple[0], i_duple[1], state.stacks) and state.hands[self.number].cards[i].ID not in self.play_queue:
                self.play_queue.append(state.hands[self.number].cards[i].ID)
                received_full = True

        last_hint = state.action_list[-1]
        # Checks for number hint what was meant: Crit Disc or Ambi Hint
        if last_hint.type == "number" and last_hint.player == self.number:
            ''''if 0 in last_hint.cards and state.curplayer == (self.number - 1) % nplayers:
                # This is a Crit Disc.  Add it to the start of the hand.
                pass
            else:'''
            if not received_full:
                for i in xrange(len(last_hint.cards)):
                    if state.hands[self.number].cards[last_hint.cards[i]].ID not in self.play_queue:
                        self.play_queue.append(state.hands[self.number].cards[last_hint.cards[i]].ID)
        if last_hint.type == "color" and last_hint.player == self.number:
            ''''if 0 in last_hint.cards and state.curplayer == (self.number - 1) % nplayers:
                # This is a Crit Disc.  Add it to the start of the hand.
                pass
            el'''
            if not received_full:
                color_list = []
                for i in range(len(last_hint.cards)):
                    color_list.append(state.hands[self.number].cards[last_hint.cards[i]])
                self.play_queue.append(self.newest_card(color_list).ID)
            
    def rearrange(self, state):  # state: same as in move()
        # Rearrange your hand if you want to
        # takes the hand into two parts - moves older cards to the left (nearer to discard) and known cards to the right (or 5's)
        last = []
        play = []
        known = []
        other = []
        for i in xrange(state.hands[self.number].size):
            if self.is_last(state, state.hands[self.number].info[i][0], state.hands[self.number].info[i][1]):
                last.append(i)
            elif self.playable(state.hands[self.number].info[i][0], state.hands[self.number].info[i][1], state.stacks):
                play.append(i)
            elif (not state.hands[self.number].info[i][0] == -1) or (not state.hands[self.number].info[i][1]):
                known.append(i)
            else:
                other.append(i)
        return other + known + play + last

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
        return max(cards, key=attrgetter("ID"))

    def oldest_card(self, cards):
        return min(cards, key=attrgetter("ID"))

    def is_last(self, state, card_color, card_num):
        # function determines whether a card is the last of its kind
        # n is the index of the card.
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

    def index_from_ID(self, state, ID, player):
        # returns an index based on an ID of a card in your hand
        for i in xrange(len(state.hands[player].cards)):
            if state.hands[player].cards[i].ID == ID:
                return i
        return -1

    def imaginary_stacks(self, state, all_queues, nplayers):
        # returns an imaginary stack based on what people know and are going to play. Plays must be in numerical order (ie R1 R2 R3), otherwise bad things will happen.
        # CHANGE TO ALLOW ALL CARDS IN QUEUES TO BE PLAYED
        ext_stacks = state.stacks
        for i in xrange(len(state.stacks)):
            current_stack = state.stacks[i]
            p = (self.number + 1) % nplayers
            while p != self.number:
                index = self.index_from_ID(state, self.all_queues[p][0], self.number)
                if index == -1:
                    continue
                if state.hands[p].cards[index].number == current_stack:
                    current_stack += 1
                    ext_stacks[i] += 1
                p = (p + 1) % nplayers
        return ext_stacks

    def select_hint(self, state, all_queues):
        # primitive version prioritizes players nearest to current player in playing order above all else.
        if state.hints == 0:
            return [-1, -1, -1]
        p = (self.number + 1) % len(state.players)
        while p != self.number:
            relevant_cards = []  # to prevent duplicate hints, etc.
            for c in state.hands[p].cards:
                if c.ID not in all_queues[p]:
                    relevant_cards.append(c)

            number_ID = self.ambi_number(state, relevant_cards, p)
            color_ID = self.ambi_color(state, relevant_cards, p)
            number_ID_card = state.hands[p].cards[self.index_from_ID(state, number_ID, p)]
            number_playable = 1
            for c in state.hands[p].cards:
                if c.number == number_ID_card.number and not self.playable(c.color, c.number, state.stacks):
                    number_playable = 0
            if number_ID != -1 and number_playable == 1:
                for c in state.hands[p].cards:  # since we know they are all playable
                    if c.number == number_ID_card.number:
                        self.all_queues[p].append(c.ID)
                return [p, number_ID, "number"]
            elif color_ID != -1:
                color_list = []
                for c in state.hands[p].cards:
                    if c.color == state.hands[p].cards[self.index_from_ID(state, color_ID, p)].color:
                        color_list.append(c)
                self.all_queues[p].append(self.newest_card(color_list).ID)
                return [p, color_ID, "color"]
            else:  # basically just give full info about a card if you can't follow either convention.
                for i in xrange(len(state.hands[p].cards)):
                    # check whether they know at least one bit of info
                    print "Hint will attempt to reveal full info"
                    if self.playable(state.hands[p].cards[i].color, state.hands[p].cards[i].number, state.stacks):
                        if state.hands[p].info[i][0] != -1:
                            return [p, c.ID, "number"]
                        elif state.hands[p].info[i][1] != -1:
                            return [p, c.ID, "color"]
            p = (p + 1) % len(state.players)
        return [-1, -1, -1]
        # either must implement imaginary stacks in this function or in the convention functions.

    def is_critical(self, state, color, number):
        # checks if is_last or if is_playable
        if self.is_last(state, color, number):
            return True
        return False

    def warn_critical(self, state, player):
        # decides whether to warn with color or with number
        # player = index of player
        assert not player == self.number
        color = state.hands[player].cards[0].color
        number = state.hands[player].cards[0].number
        if len(self.attribute_list(state.hands[player].cards, "color", color)) == 1:
            return Action("color", 0, player)
        elif len(self.attribute_list(state.hands[player].cards, "number", number)) == 1:
            return Action("number", 0, player)
        else:
            return Action("color", 0, player)

    def attribute_list(self, clist, c_or_n, attr):
        # clist is a list of cards
        # returns a list of IDs of cards satsfying the attribute
        # DO NOT CALL ON YOURSELF
        out = []
        if c_or_n == "color":
            for i in xrange(len(clist)):
                if clist[i].color == attr:
                    out.append(clist[i].ID)
        elif c_or_n == "number":
            for i in xrange(len(clist)):
                if clist[i].number == attr:
                    out.append(clist[i].ID)
        return out

    def ambi_number(self, state, clist, player):
        # checks whether or not all cards can be played (for Ambiguous Number Tactic)
        # returns ID of card to hint, -1 if nothing
        # this still needs fixing
        numlists = [[] for i in range(5)]
        number = 0
        while number <= 4:
            for c in clist:
                if c.number == number:
                    numlists[number].append(c.ID)
            number += 1
        
        hintable_numbers_allplayable = []  # duples of numbers and the lengths of their corresponding numlists
        hintable_numbers_noneplayable = []  # meaning, the other player knows that they can't all be played
        for i in xrange(len(numlists)):
            all_playable = 1
            stack_number_size = 0
            if len(numlists[i]) == 0:
                all_playable = 0
            for j in xrange(len(numlists[i])):
                for k in xrange(len(numlists[i])):
                    if j == k:
                        continue
                    card1 = state.hands[player].cards[self.index_from_ID(state, numlists[i][j], player)]
                    card2 = state.hands[player].cards[self.index_from_ID(state, numlists[i][k], player)]
                    if card1.color == card2.color:
                        all_playable = 0
            for j in xrange(len(numlists[i])):
                curcard = state.hands[player].cards[self.index_from_ID(state, numlists[i][j], player)]
                if not self.playable(curcard.color, curcard.number, state.stacks):
                    all_playable = 0
            for j in xrange(len(state.stacks)):
                if state.stacks[j] == i:
                    stack_number_size += 1
                        
            if all_playable == 1:
                hintable_numbers_allplayable.append([i, len(numlists[i])])
            if stack_number_size < len(numlists[i]):
                hintable_numbers_noneplayable.append([i, len(numlists[i])])
                
        if hintable_numbers_allplayable != []:
            to_play = max(hintable_numbers_allplayable, key=lambda x: x[1])
        elif hintable_numbers_noneplayable != []:
            to_play = max(hintable_numbers_noneplayable, key=lambda x: x[1])
        else:
            return -1

        print "hintable_numbers_allplayable: " + str(hintable_numbers_allplayable)
        print "hintable_numbers_noneplayable: " + str(hintable_numbers_noneplayable)
        print "numlists: " + str(numlists)
        print "to_play: " + str(to_play)
        for c in clist:
            if c.number == to_play[0]:
                return c.ID
        """
        for i in xrange(len(clist)):
            ID_list = self.attribute_list(clist, "number", clist[i].number)
            number_list = [clist[self.index_from_ID(state, i)] for i in ID_list]
            duplicate_list = []
            for j in number_list:
                for k in number_list:
                    if j.number == k.number and j.color == k.color:
                        continue
                    if j.color == k.color:
                        duplicate_list.append(j)
                        duplicate_list.append(k)
            duplicate_check = []
            print "duplicate_list: " + str(duplicate_list)
            for j in number_list:
                if j not in duplicate_list:
                    duplicate_check.append(j)
            for c in duplicate_check:
                if self.playable(c.color, c.number, state.stacks):
                    return c.ID
        # put something in here regarding imaginary stacks in order to build higher
        return -1
        """

    def ambi_color(self, state, clist, p):
        # checks whether or not newest card can be played (for Ambiguous Color Tactic)
        # returns ID of card to hint, -1 if nothing
        for i in xrange(len(clist)):
            ID_list = self.attribute_list(clist, "color", clist[i].color)
            print ID_list
            color_list = []
            for j in clist:
                if j.ID in ID_list:
                    color_list.append(j)
            new_card = self.newest_card(color_list)
            if self.playable(new_card.color, new_card.number, state.stacks):
                return new_card.ID
        return -1
