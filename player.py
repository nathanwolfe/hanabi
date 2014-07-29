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
        self.play_queue = None  # list of cards to be played
        self.all_queues = None

    def move(self, state, nplayers):
        # assume we've figured out all of our variables and rearranged all of our cards.
        """
        Order of Cases:
        critical discard of next person
        there are playable cards in queue
        critical discard of person later one
        if nothing else can be done, discard
        """

        # Case: critical discard of next person
        next_discard = state.hands[(self.number + 1) % nplayers].cards[0]
        if self.is_last(state, next_discard.color, next_discard.number):
            return Action("hint", 0, (self.number + 1) % nplayers)

        # Case: there are playable cards in queue
        if len(self.play_queue) > 0:
            return Action("play", self.index_from_ID(self.play_queue[0]), None)

        # Case: critical discard of person later on
        
        # Case: give hints to players
        possible_hints = []  # LIST OF IDS OF CARDS THAT CAN BE HINTED
        for i in nplayers:
            if i == self.number:
                continue
            else:
                for j in xrange(len(state.hands[i].cards)):
                    if self.playable(state.hands[i].cards[j].color, state.hands[i].cards[j].number, state.stacks):
                        possible_hints.append(state.hands[i].cards[j].ID)
        return self.select_hint(self, state, possible_hints, self.all_queues)

        # Case: if nothing else can be done, discard
        return Action("discard", 0, None)

    def analyze(self, state):
        for i in range(len(state.hands[self.number].cards)):
            i_duple = state.hands[self.number].info[i]
            if self.playable(i_duple[0], i_duple[1], state.stacks):
                self.play_queue.append(state.hands[self.number].cards[i].ID)

    def rearrange(self, state):  # state: same as in move()
        # Rearrange your hand if you want to
        # takes the hand into two parts - moves older cards to the left (nearer to discard) and known cards to the right (or 5's)
        last = []
        play = []
        known = []
        other = []
        for i in range(state.hands[self.number].size):
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

    def index_from_ID(self, state, ID):
        # returns an index based on an ID of a card in your hand
        for i in xrange(len(state.hands[self.number].cards)):
            if state.hands[self.number].cards[i].ID == ID:
                return i
        return -1
