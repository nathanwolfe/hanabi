from card import Card
from deck import Deck
from action import Action
import copy
import random
from hand import Hand

"""
This is an example player file. AI developers should be able to specify their own players later.
"""


class Player:
    def __init__(self, n):  # n = player number
        self.number = n
        # queue is card to be played (may be obsolete now)
        self.queue = []

    def move(self, state):  # state = current state of the game which is has player's own hand as empty list and deck as list of dummy cards (red 1s)
        state.hands[self.number].cards = []  # Censor the hand entirely for ease of use later to tell if I can see the hand or not
        move = self.predict(state, 2)
        print move.type + " " + str(move.cards) + " " + str(move.player)
        return move
    
    def act(self, curmove, state, num):  # predict result of the action curmove with respect to state if I'm player [num]. state is modified.
        # Ideally, should be modified to be probabilistic / generate a bunch of possible result states with probabilities.
        if curmove.type == "play":
            if len(state.hands[num].cards) == 0:  # i.e. I can't see the actual card
                if num >= len(state.hands): print str(len(state.hands)) + " " + str(num)
                if state.hands[num].info[curmove.cards][0] >= 0 and state.hands[num].info[curmove.cards][1] >= 0:  # if I know the card:
                    if state.stacks[state.hands[num].info[curmove.cards][0]] == state.hands[num].info[curmove.cards][1]:
                        state.stacks[state.hands[num].info[curmove.cards][0]] += 1
                        if state.stacks[state.hands[num].info[curmove.cards][0]] == 5 and state.hints < 8:
                            state.hints += 1
                        state.hands[num].info.pop(curmove.cards)
                    else:
                        state.lives -= 1
                        state.discards.append(Card(state.hands[num].info[curmove.cards][0], state.hands[num].info[curmove.cards][1]))
                        state.hands[num].info.pop(curmove.cards)
                elif state.hands[num].info[curmove.cards][0] == -1 and state.hands[num].info[curmove.cards][1] == -1:  # if I know nothing:
                    state.lives -= 1
                    state.discards.append(Card(5, 5))
                    state.hands[num].info.pop(curmove.cards)
                elif state.hands[num].info[curmove.cards][0] == -1:  # so I know the number but not the color
                    num_equal = 0
                    for info in state.hands[num].info:
                        if info[1] == state.hands[num].info[curmove.cards][1]:
                            num_equal += 1
                    if num_equal > 1:  # i.e. this card isn't the only one with that number, assume it's not playable
                        state.lives -= 1
                        state.discards.append(Card(5, 5))
                        state.hands[num].info.pop(curmove.cards)
                    else:
                        pile = -1
                        for stack in range(len(state.stacks)):
                            if state.stacks[stack] == state.hands[num].info[curmove.cards][1]:
                                pile = stack
                        if pile == -1:  # i.e. didn't find a matching stack, obviously unplayable
                            state.lives -= 1
                            state.discards.append(Card(5, 5))
                            state.hands[num].info.pop(curmove.cards)
                        else:  # Assume it's playable on the [pile]th stack.
                            state.stacks[pile] += 1
                            if state.stacks[pile] == 5 and state.hints < 8:
                                state.hints += 1
                            state.hands[num].info.pop(curmove.cards)
                else:  # I know the color and not the number
                    num_equal = 0
                    for info in state.hands[num].info:
                        if info[0] == state.hands[num].info[curmove.cards][0]:
                            num_equal += 1
                    if num_equal > 1:  # i.e. this card isn't the only one with that number, assume it's not playable
                        state.lives -= 1
                        state.discards.append(Card(5, 5))
                        state.hands[num].info.pop(curmove.cards)
                    else:
                        if state.stacks[state.hands[num].info[curmove.cards][0]] == 5:  # the stack is full, can't be played
                            state.lives -= 1
                            state.discards.append(Card(5, 5))
                            state.hands[num].info.pop(curmove.cards)
                        else:
                            state.stacks[state.hands[num].info[curmove.cards][0]] += 1
                            if state.stacks[state.hands[num].info[curmove.cards][0]] == 5 and state.hints < 8:
                                state.hands[num].info.pop(curmove.cards)
            else:  # i.e. I can see the card
                if state.stacks[state.hands[num].cards[curmove.cards].color] == state.hands[num].cards[curmove.cards].number:
                    state.stacks[state.hands[num].cards[curmove.cards].color] += 1
                    if state.stacks[state.hands[num].cards[curmove.cards].color] == 5 and state.hints < 8:
                        state.hints += 1
                    state.hands[num].cards.pop(curmove.cards)
                    state.hands[num].info.pop(curmove.cards)
                else:
                    state.lives -= 1
                    state.discards.append(state.hands[num].cards.pop(curmove.cards))
                    state.hands[num].info.pop(curmove.cards)
            state.hands[num].size -= 1  # not going to append anything since idk the deck
            if state.deck.length() > 0:
                state.deck.pop_card()  # still need to account for this though
        elif curmove.type == "discard":
            state.hands[num].size -= 1
            state.hands[num].info.pop(curmove.cards)
            if len(state.hands[num].cards) > 0:  # append if you know what the card is
                state.discards.append(state.hands[num].cards.pop(curmove.cards))
            else:
                state.discards.append(Card(5, 5))
            if state.hints < 8:
                state.hints += 1
            if state.deck.length() > 0:
                state.deck.pop_card()
        elif curmove.type == "color":
            if len(state.hands[curmove.player].cards) > 0:  # If I can see the hand:
                hinted = []
                for i in range(state.hands[curmove.player].size):
                    if state.hands[curmove.player].cards[i].color == state.hands[curmove.player].cards[curmove.cards].color:
                        state.hands[curmove.player].info[i][0] = state.hands[curmove.player].cards[curmove.cards].color
                        hinted.append(i)
                assert state.hints > 0, "Tried to hint when out of hints: player " + str(state.curplayer)
                state.hints -= 1
            else:  # well I can't really process this hint attempt since idk what the hand looks like
                state.hints -= 1
        else:
            assert curmove.type == "number", "invalid move string specified"
            if len(state.hands[curmove.player].cards) > 0:  # If I can see the hand:
                hinted = []
                for i in range(state.hands[curmove.player].size):
                    if state.hands[curmove.player].cards[i].number == state.hands[curmove.player].cards[curmove.cards].number:
                        state.hands[curmove.player].info[i][1] = state.hands[curmove.player].cards[curmove.cards].number
                        hinted.append(i)
                assert state.hints > 0, "Tried to hint when out of hints: player " + str(state.curplayer)
                state.hints -= 1
            else:  # well I can't really process this hint attempt since idk what the hand looks like
                state.hints -= 1
        state.attach_action(curmove)
        return state
    
    def generate_moves(self, state):  # Generates list of possible moves.
        # Tiebreak by play - hint - discard in that order of preference
        possible_moves = []
        for i in range(state.hands[0].size):
            possible_moves.append(Action("play", i, None))
        if state.hints >= 1:
            for j in range(len(state.players)):
                if j == self.number:
                    continue
                for i in range(state.hands[j].size):
                    possible_moves.append(Action("color", i, j))
                    possible_moves.append(Action("number", i, j))
        for i in range(state.hands[0].size):
            possible_moves.append(Action("discard", i, None))
        return possible_moves
    
    def predict(self, state, n):  # Evaluates a state recursively.
        # n is number of moves you look ahead from this point on.
        best_score = -999
        chosen_move = Action("discard", 0, None)
        for move in self.generate_moves(state):
            #print "move candidate: " + move.type + " " + str(move.cards) + " " + str(move.player)
            backup = self.backup(state)
            acted = state
            acted.hands[acted.curplayer].cards = []  # censor your hand here before you do anything else (not earlier to avoid changing state)
            acted = self.act(move, acted, acted.curplayer)
            acted.curplayer = (acted.curplayer + 1) % len(acted.players)
            for i in range(n):
                next_move = self.predict(acted, n - i - 1)
                #print "predicted next move: " + next_move.type + " " + str(next_move.cards) + " " + str(next_move.player)
                acted = self.act(next_move, acted, acted.curplayer)
                acted.curplayer = (acted.curplayer + 1) % len(acted.players)
            move_score = self.eval(acted)
            #print "score: " + str(move_score)
            if move_score > best_score:
                chosen_move = move
                best_score = move_score
            self.restore(state, backup)
        return chosen_move
    
    # Backs up the state to an array so it can be restored. Used in lieu of an actual copy operation.
    def backup(self, state):
        out = []
        out.append(copy.copy(state.deck))
        out.append(copy.copy(state.discards))
        out.append(state.lives)
        out.append(state.hints)
        out.append(copy.copy(state.stacks))
        out.append([Hand(copy.copy(hand.cards), hand.size) for hand in state.hands])
        for i in xrange(len(state.hands)):
            out[5][i].info = [copy.copy(info) for info in state.hands[i].info]
        out.append(state.players)
        out.append(state.curplayer)
        return out
    
    # Restores the state from the backup.
    def restore(self, state, backup):
        state.deck = backup[0]
        state.discards = backup[1]
        state.lives = backup[2]
        state.hints = backup[3]
        state.stacks = backup[4]
        state.hands = backup[5]
        state.players = backup[6]
        state.curplayer = backup[7]
    
    def obsolete(self, state, n):
        # If you know what a card is and it's playable, play it.
        for i in range(state.hands[self.number].size):
            if self.playable(state.hands[self.number].info[i][0], state.hands[self.number].info[i][1], state.stacks) == True:
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
        # If someone has something playable that can be hinted unambiguously, hint that.
        for i in range(len(state.players)):
            if i == self.number: 
                continue
            for j in range(state.hands[i].size):
                #print "size: " + str(len(state.hands[i].cards)) + "; " + str(j)
                if self.playable(state.hands[i].cards[j].color, state.hands[i].cards[j].number, state.stacks):
                    if state.hands[i].info[j][0] == -1 and self.unique(state.hands[i].cards[j].color, state.hands[i].cards, 0):
                        print "Hinting color: " + str(j) + " of P" + str(i)
                        return Action("color", j, i)
                    if state.hands[i].info[j][1] == -1 and self.unique(state.hands[i].cards[j].number, state.hands[i].cards, 1):
                        print "Hinting number: " + str(j) + " of P" + str(i)
                        return Action("number", j, i)
        # If someone has something playable, hint that.
        for i in range(len(state.players)):
            if i == self.number: 
                continue
            for j in range(state.hands[i].size):
                #print "size: " + str(len(state.hands[i].cards)) + "; " + str(j)
                if self.playable(state.hands[i].cards[j].color, state.hands[i].cards[j].number, state.stacks):
                    if state.hands[i].info[j][0] == -1:
                        print "Hinting color: " + str(j) + " of P" + str(i)
                        return Action("color", j, i)
                    if state.hands[i].info[j][1] == -1:
                        print "Hinting number: " + str(j) + " of P" + str(i)
                        return Action("number", j, i)
        print "Nothing hintable, discarding."
        # Can't do anything immediately helpful, so let's just discard cards we don't have info about. If we already have max hints, whatever.        
        for i in range(state.hands[self.number].size):
            if state.hands[self.number].info[i][0] == -1 and state.hands[self.number].info[i][1] == -1:
                return Action("discard", i, None)
        for i in range(state.hands[self.number].size):
            if state.hands[self.number].info[i][0] == -1 or state.hands[self.number].info[i][1] == -1:
                return Action("discard", i, None)
        return Action("discard", 0, None)

    def rearrange(self, state):  # state: same as in move()
        # Rearrange your hand if you want to
        # This is the default permutation.
        return [i for i in range(state.hands[self.number].size)]

    def scan(self, state):  # state: same as in move()
        # Look around if you want
        # If someone hinted this player unambiguously, add that to a queue.
        if (state.action.type == "number" or state.action.type == "color") and state.action.player == self.number and len(state.action.cards) == 1:
            self.queue.append(state.action.cards[0])
        # If someone played a card, clear the queue since it might not be playable. (This could be optimized but w/e.)
        if state.action.type == "play":
            self.queue = []
        
    
    # This function isn't required; I'm implementing this to make things easier
    def playable(self, color, number, stacks):  # Is the card guaranteed playable on stacks (list)?
        # color and number should be -1 if unknown
        # print str(color) + " " + str(number) + " -> " + str(stacks[color]) + " " + str(number)
        if color == -1 or number == -1:
            return False
        if stacks[color] == number:
            return True
        else:
            return False
    
    def unique(self, value, cards, type):  # Checks uniqueness of a value in a hand.
        #type = 0 -> color, type = 1 -> number
        num = 0
        for card in cards:
            if (type == 0 and value == card.color) or (type == 1 and value == card.number):
                num += 1
        if num == 1:
            return True
        return False
    
    def eval(self, state):  # Evaluates a given state.
        score = state.stacks[0] + state.stacks[1] + state.stacks[2] + state.stacks[3] + state.stacks[4]
        if state.deck.length > 0:
            score += state.hints * 0.7  # because a hint is worth less than a played card
            if state.hints < 2: 
                score -= 0.5  # leave a hint for contingencies
            score += state.lives * 3  # because lives yo
            # Penalize if things are "locked out" (values are kinda arbitrary)
            self.discarded = [[0 for i in range(6)] for j in range(6)]  # [5][5] is unknown card
            for card in state.discards:
                self.discarded[card.color][card.number] += 1
            for i in range(5):
                if self.discarded[i][0] == 3:
                    score -= 4
                if self.discarded[i][1] == 2:
                    score -= 3
                if self.discarded[i][2] == 2:
                    score -= 3
                if self.discarded[i][3] == 2:
                    score -= 2
                if self.discarded[i][4] == 1:
                    score -= 2
        else:  # different end of game strat
            score += state.hints * 0.4  # because a hint is worth much than a played card
            score += state.lives * 0.5
            score += 1  # to somewhat offset the score decrease when the deck runs out
            if state.lives <= 0:  # dont die yo
                score -= 100
            for i in range(5):  # I can't decrease these penalties too much or the bot might try to end the game.
                if self.discarded[i][0] == 3:
                    score -= 3
                if self.discarded[i][1] == 2:
                    score -= 2
                if self.discarded[i][2] == 2:
                    score -= 2
                if self.discarded[i][3] == 2:
                    score -= 1
                if self.discarded[i][4] == 1:
                    score -= 1
        for i in range(len(state.players)):
            for j in range(state.hands[i].size):
                for k in range(2):
                    if state.hands[i].info[j][k] >= 0:
                        score += 0.1  # because it's good to have information
        for card in state.discards:
            score -= 0.11  # discourage extensive discarding
            if card.number < 5 and state.stacks[card.color] > card.number:
                # encourage discarding of unplayable cards
                score += 0.1
        return score
