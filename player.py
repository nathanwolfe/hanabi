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

