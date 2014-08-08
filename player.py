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
        critical discard of person later one [REMOVED]
        prioritize hints
        give hints to players
        if nothing else can be done, discard
        """
        hint_triples = []
        next_p = (self.number + 1) % nplayers  # generally helpful index
        discard_flag = 1
        for p in range(nplayers):
            if p == self.number:
                continue
            hint_triples.append(self.select_hint(state, p))
        hint_triple = [-1, -1, -1]
        for h in hint_triples:
            if h != [-1, -1, -1]:
                hint_triple = h
                break
        if (len(self.play_queue) == 0 and hint_triple[0] == next_p) or (len(self.play_queue) > 0 and hint_triple != [-1, -1, -1]):
            discard_flag = 0
        
        next_discard = state.hands[next_p].cards[0]
        a_hint = self.select_hint(state, next_p)
        a_card = state.hands[next_p].cards[self.index_from_ID(state, a_hint[1], a_hint[0])]  # the card that may be hinted instead of crit discard
        # Case: critical discard of next person
        if self.is_critical(state, next_discard.color, next_discard.number) and state.hints > 0 and discard_flag == 1:
            if not self.playable(a_card.color, a_card.number, state.stacks):
                if state.hints == 1 or not a_hint[2] == "color":
                    print "Critical discard hint given:" + str(next_discard.ID)
                    return self.warn_critical(state, next_p)

        # Case: there are playable cards in queue
        if len(self.play_queue) > 0:
            # print "Play_queue: " + str(self.play_queue)
            print "Played the card at index: " + str(self.index_from_ID(state, self.play_queue[0], self.number))
            return Action("play", self.index_from_ID(state, self.play_queue.pop(0), self.number), None)

        # Prioritize hints to players
        # assuming select_hint returns a triple [player, ID, hint type]
        cur_p = (self.number + 1) % nplayers
        poss_hints = []  # possible hint for each player
        # print hint_triple
        hint_card = state.hands[cur_p].cards[self.index_from_ID(state, hint_triple[1], cur_p)]
        if hint_triple[1] != -1 and (self.playable(hint_card.color, hint_card.number, state.stacks) or hint_triple[2] == "color"):
            print "Hinted to " + str(hint_triple[0]) + " the card at " + str(state.players[hint_triple[0]].index_from_ID(state, hint_triple[1], hint_triple[0])) + "."
            if hint_triple[2] == "color":
                print "Color hinted."
            elif hint_triple[2] == "number":
                print "Number hinted."
            return Action(hint_triple[2], state.players[hint_triple[0]].index_from_ID(state, hint_triple[1], hint_triple[0]), hint_triple[0])
        elif hint_triple[1] != -1:
            poss_hints.append(hint_triple)
        cur_p = (cur_p + 1) % nplayers

        # Case: if nothing else can be done, discard
        print "Discarding."
        return Action("discard", 0, None)

    def analyze(self, state, nplayers):
        received_full = False  # checks if the player has received full information about any one card
        last_hint = state.action_list[-1]
        if last_hint.player is not None:
            for i in xrange(len(state.hands[last_hint.player].cards)):
                # Checks for full info cards
                i_duple = state.hands[last_hint.player].info[i]
                if self.playable(i_duple[0], i_duple[1], state.stacks):
                    if self.number == last_hint.player and state.hands[last_hint.player].cards[i].ID not in self.play_queue:
                        self.play_queue.append(state.hands[self.number].cards[i].ID)
                    if state.hands[last_hint.player].cards[i].ID not in self.all_queues[last_hint.player]:
                        self.all_queues[last_hint.player].append(state.hands[last_hint.player].cards[i].ID)
                    received_full = True

        # Checks for number hint what was meant: Crit Disc or Ambi Hint
        if not received_full:
            if last_hint.type == "number":
                if 0 not in last_hint.cards:
                    # first check to see if all the cards are playable!
                    num_stacks_playable = 0
                    for i in xrange(len(state.stacks)):
                        if state.stacks[i] == state.hands[last_hint.player].info[last_hint.cards[0]][1]:  # if the ith stack's value is equal to the number that was hinted
                            num_stacks_playable += 1
                    if num_stacks_playable >= len(last_hint.cards):
                        for i in xrange(len(last_hint.cards)):
                            if state.hands[last_hint.player].cards[last_hint.cards[i]].ID not in self.play_queue:
                                if self.number == last_hint.player:
                                    self.play_queue.append(state.hands[self.number].cards[last_hint.cards[i]].ID)
                                self.all_queues[last_hint.player].append(state.hands[last_hint.player].cards[last_hint.cards[i]].ID)
            if last_hint.type == "color":
                color_list = []
                for i in range(len(last_hint.cards)):
                    color_list.append(state.hands[last_hint.player].cards[last_hint.cards[i]])
                if last_hint.player == self.number:
                    self.play_queue.append(self.newest_card(color_list).ID)
                self.all_queues[last_hint.player].append(self.newest_card(color_list).ID)

        if last_hint.type == "play":
            self.all_queues[state.curplayer].pop(0)

    def rearrange(self, state):  # state: same as in move()
        # Rearrange your hand if you want to
        # takes the hand into two parts - moves older cards to the left (nearer to discard) and known cards to the right (or 5's)
        last = []
        play = []
        known = []
        other = []
        for i in xrange(state.hands[self.number].size):
            if self.might_be_last(state, state.hands[self.number].info[i][1]):
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

        if card_num == 4:
            return True
        if card_color == -1 or card_num == -1:
            return False
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

    def select_hint(self, state, p):
        if state.hints == 0:
            return [-1, -1, -1]
        relevant_cards = []
        for c in state.hands[p].cards:
            relevant = 1
            for q in xrange(len(self.all_queues)):
                if q == self.number:
                    continue
                for r in xrange(len(self.all_queues[q])):
                    queue_card = state.hands[q].cards[self.index_from_ID(state, self.all_queues[q][r], q)]
                    if queue_card.color == c.color and queue_card.number == c.number:
                        relevant = 0
            if relevant == 1 and c.ID not in self.all_queues[p]:
                relevant_cards.append(c)

        number_ID = self.ambi_number(state, relevant_cards, p)
        color_ID = self.ambi_color(state, relevant_cards, p)
        number_ID_card = state.hands[p].cards[self.index_from_ID(state, number_ID, p)]
        number_playable = 1
        for c in state.hands[p].cards:
            if c.number == number_ID_card.number and not self.playable(c.color, c.number, state.stacks):
                number_playable = 0
        if number_ID != -1 and number_playable == 1:
            return [p, number_ID, "number"]
        elif color_ID != -1:
            color_list = []
            for c in state.hands[p].cards:
                if c.color == state.hands[p].cards[self.index_from_ID(state, number_ID, p)].color:
                    color_list.append(c)
            return [p, color_ID, "color"]
        else:
            # print "Hint wil attempt to reveal full info"
            for i in xrange(len(state.hands[p].cards)):
                if self.playable(state.hands[p].cards[i].color, state.hands[p].cards[i].number, state.stacks) and state.hands[p].cards[i].ID not in self.all_queues[p]:
                    if state.hands[p].info[i][0] != -1:
                        return [p, state.hands[p].cards[i].ID, "number"]
                    elif state.hands[p].info[i][1] != -1:
                        return [p, state.hands[p].cards[i].ID, "color"]
        return [-1, -1, -1]

    def might_be_last(self, state, number):
        # assumes color is not known
        discard_sizes = [0 for i in range(5)]

        for c in state.discards:
            if state.stacks[c.color] >= c.number and c.number == number:
                discard_sizes[c.color] += 1

        if number == 0 and max(discard_sizes) >= 2:
            return True
        elif number == 4:
            return True
        elif max(discard_sizes) >= 1:
            return True

        return False

    def select_hint_old(self, state):
        # primitive version prioritizes players nearest to current player in playing order above all else.
        if state.hints == 0:
            return [-1, -1, -1]
        p = (self.number + 1) % len(state.players)
        while p != self.number:
            relevant_cards = []  # to prevent duplicate hints, etc.
            for c in state.hands[p].cards:
                if c.ID not in self.all_queues[p]:
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
                # print "Hint will attempt to reveal full info"
                for i in xrange(len(state.hands[p].cards)):
                    # check whether they know at least one bit of info
                    if self.playable(state.hands[p].cards[i].color, state.hands[p].cards[i].number, state.stacks) and state.hands[p].cards[i].ID not in self.all_queues[p]:
                        if state.hands[p].info[i][0] != -1:
                            # print [p, state.hands[p].cards[i].ID, "number"]
                            return [p, state.hands[p].cards[i].ID, "number"]
                        elif state.hands[p].info[i][1] != -1:
                            # print [p, state.hands[p].cards[i].ID, "color"]
                            return [p, state.hands[p].cards[i].ID, "color"]
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
        return Action("number", 0, player)

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

        unplayable = [0 for i in xrange(len(hintable_numbers_allplayable))]
        for i in xrange(len(hintable_numbers_allplayable)):
            for j in xrange(len(hintable_numbers_allplayable[i])):
                if state.hands[player].cards[0].ID == j:
                    unplayable[i] = 1
                    break

        hintable_numbers_really_allplayable = [hintable_numbers_allplayable[i] for i in xrange(len(hintable_numbers_allplayable)) if unplayable[i] == 0]

        if hintable_numbers_really_allplayable != []:
            to_play = max(hintable_numbers_really_allplayable, key=lambda x: x[1])
        # elif hintable_numbers_noneplayable != []:
            # to_play = max(hintable_numbers_noneplayable, key=lambda x: x[1])
        else:
            return -1

        """
        print "hintable_numbers_allplayable: " + str(hintable_numbers_allplayable)
        print "hintable_numbers_noneplayable: " + str(hintable_numbers_noneplayable)
        print "numlists: " + str(numlists)
        print "to_play: " + str(to_play)
        """
        for c in clist:
            if c.number == to_play[0]:
                return c.ID

    def ambi_color(self, state, clist, p):
        # checks whether or not newest card can be played (for Ambiguous Color Tactic)
        # returns ID of card to hint, -1 if nothing
        for i in xrange(len(clist)):
            ID_list = self.attribute_list(clist, "color", clist[i].color)
            # print ID_list
            color_list = []
            for j in clist:
                if j.ID in ID_list:
                    color_list.append(j)
            new_card = self.newest_card(color_list)
            if self.playable(new_card.color, new_card.number, state.stacks):
                return new_card.ID
        return -1
