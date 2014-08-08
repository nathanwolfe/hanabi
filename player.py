from card import Card
from deck import Deck
from action import Action
import copy
import random
from hand import Hand



class Player:
    def __init__(self, n):  # n = player number
        self.number = n
        self.curturn = 0
        self.hint_age = []  # List of lists for tracking age of card info

    def move(self, state):  # state = current state of the game which is has player's own hand as empty list and deck as list of dummy cards (red 1s)
        state.hands[self.number].cards = []  # Censor the hand entirely for ease of use later to tell if I can see the hand or not
        state.stacks.append(0)  # This will be used in act as a placeholder "extra points" predictor.
        self.initlives = state.lives
        self.initdecksize = state.deck.length()
        if self.hint_age == []:  # Init this if needed
            self.hint_age = [[[-1 for i in xrange(2)] for j in xrange(state.hands[0].size)] for k in xrange(len(state.players))]
        move = self.predict(state, 2)
        print move.type + " " + str(move.cards) + " " + str(move.player)
        return move
    
    def act(self, curmove, state, num):  # predict result of the action curmove with respect to state if I'm player [num]. state is modified.
        # Ideally, should be modified to be probabilistic / generate a bunch of possible result states with probabilities.
        # if num >= len(state.hands):
        #    print "num >= len(state.hands): " + str(num) + " " + str(len(state.hands))
        # if curmove.cards >= len(
        if curmove.type == "play":
            if len(state.hands[num].cards) == 0:  # i.e. I can't see the actual card
                if num >= len(state.hands): print str(len(state.hands)) + " " + str(num)
                if state.hands[num].info[curmove.cards][0] >= 0 and state.hands[num].info[curmove.cards][1] >= 0:  # if I know the card:
                    if state.stacks[state.hands[num].info[curmove.cards][0]] == state.hands[num].info[curmove.cards][1]:
                        state.stacks[state.hands[num].info[curmove.cards][0]] += 1
                        if state.stacks[state.hands[num].info[curmove.cards][0]] == 5 and state.hints < 8:
                            state.hints += 1
                        state.hands[num].info.pop(curmove.cards)
                        state.lives += 0.01  # a small point bonus
                    else:
                        state.lives -= 1
                        state.discards.append(Card(state.hands[num].info[curmove.cards][0], state.hands[num].info[curmove.cards][1]))
                        state.hands[num].info.pop(curmove.cards)
                elif state.hands[num].info[curmove.cards][0] == -1 and state.hands[num].info[curmove.cards][1] == -1:  # if I know nothing:
                    state.lives -= 1
                    state.discards.append(Card(5, 5))
                    state.hands[num].info.pop(curmove.cards)
                elif state.hands[num].info[curmove.cards][0] == -1:  # so I know the number but not the color
                    if self.hint_age[num][curmove.cards][1] > len(state.players):  # i.e. the info here is too old, so probably not a play hint
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
                    if self.hint_age[num][curmove.cards][0] > len(state.players):  # i.e. the info here is too old, so probably not a play hint
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
                # hinted = []
                for i in range(state.hands[curmove.player].size):
                    if state.hands[curmove.player].cards[i].color == state.hands[curmove.player].cards[curmove.cards].color:
                        state.hands[curmove.player].info[i][0] = state.hands[curmove.player].cards[curmove.cards].color
                        self.hint_age[curmove.player][i][0] = 0  # Update this.
                        # hinted.append(i)
                assert state.hints > 0, "Tried to hint when out of hints: player " + str(state.curplayer)
                state.hints -= 1
            else:  # well I can't really process this hint attempt since idk what the hand looks like, but maybe something is playable.
                state.hints -= 1
                state.stacks[5] += 1
        else:
            assert curmove.type == "number", "invalid move string specified"
            if len(state.hands[curmove.player].cards) > 0:  # If I can see the hand:
                # hinted = []
                for i in range(state.hands[curmove.player].size):
                    if state.hands[curmove.player].cards[i].number == state.hands[curmove.player].cards[curmove.cards].number:
                        state.hands[curmove.player].info[i][1] = state.hands[curmove.player].cards[curmove.cards].number
                        self.hint_age[curmove.player][i][1] = 0  # Update this.
                        # hinted.append(i)
                assert state.hints > 0, "Tried to hint when out of hints: player " + str(state.curplayer)
                state.hints -= 1
            else:  # well I can't really process this hint attempt since idk what the hand looks like
                state.hints -= 1
                state.stacks[5] += 1
        state.attach_action(curmove)
        return state
    
    def generate_moves(self, state):  # Generates list of possible moves.
        # Tiebreak by play - hint - discard in that order of preference
        possible_moves = []
        for i in range(state.hands[state.curplayer].size):
            possible_moves.append(Action("play", i, None))
        if state.hints >= 1:
            for j in range(len(state.players)):
                if j == state.curplayer:
                    continue
                if len(state.hands[j].cards) == 0:
                    possible_moves.append(Action("color", 0, j))  # Don't bother making multiple hint possibilities if you don't know the hand
                else:
                    for i in range(state.hands[j].size):
                        possible_moves.append(Action("number", i, j))
                        possible_moves.append(Action("color", i, j))
        for i in range(state.hands[state.curplayer].size):
            possible_moves.append(Action("discard", i, None))
        return possible_moves
    
    def predict(self, state, n):  # Evaluates a state recursively.
        # n is number of moves you look ahead from this point on.
        best_score = -999
        chosen_move = Action("discard", 0, None)
        # Copies the info array.
        init_info = [[[self.hint_age[i][j][k] for k in xrange(2)] for j in xrange(len(self.hint_age[i]))] for i in xrange(len(self.hint_age))]
        # init_info = copy.deepcopy(self.hint_age)
        if n == 2: best_act1 = 0
        for move in self.generate_moves(state):
            # print "move candidate: " + move.type + " " + str(move.cards) + " " + str(move.player)
            # make or restore backups as relevant
            backup = self.backup(state)
            self.hint_age = [[[init_info[i][j][k] for k in xrange(2)] for j in xrange(len(init_info[i]))] for i in xrange(len(init_info))]
            # self.hint_age = copy.deepcopy(init_info)
            acted = state
            acted.hands[acted.curplayer].cards = []  # censor your hand here before you do anything else (not earlier to avoid changing state)
            acted = self.act(move, acted, acted.curplayer)
            if acted.lives < self.initlives:
                self.restore(state, backup)
                continue
            acted.curplayer = (acted.curplayer + 1) % len(acted.players)
            self.scansim(acted)
            if n == 2: act1 = 0
            for i in xrange(n):
                next_move = self.predict(acted, n - i - 1)
                if n == 2 and i == 0: act1 = next_move
                #if self.curturn == 24 and move.type == "play" and move.cards == 2 and n == 2: print "predicted next move: " + next_move.type + " " + str(next_move.cards) + " " + str(next_move.player)
                acted = self.act(next_move, acted, acted.curplayer)
                #if self.curturn == 29 and move.type == "number" and move.cards == 3 and move.player == 0: print acted.lives
                acted.curplayer = (acted.curplayer + 1) % len(acted.players)
                self.scansim(acted)
            move_score = self.eval(acted)
            # if self.curturn == 24 and move.type == "play" and n == 2: print str(move.cards) + " " + str(move_score)
            #print "score: " + str(move_score)
            if move_score > best_score:
                chosen_move = move
                best_score = move_score
                if n == 2: best_act1 = act1
            self.restore(state, backup)
        self.hint_age = [[[init_info[i][j][k] for k in xrange(2)] for j in xrange(len(init_info[i]))] for i in xrange(len(init_info))]
        #self.hint_age = copy.deepcopy(init_info)
        #if n == 2: print "predicted next move: " + best_act1.type + " " + str(best_act1.cards) + " " + str(best_act1.player)
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
    
    def rearrange(self, state):  # state: same as in move()
        # Rearrange your hand if you want to
        # This is the default permutation.
        return [i for i in range(state.hands[self.number].size)]

    def scan(self, state):  # state: same as in move()
        # Look around if you want
        self.curturn += 1
        if self.hint_age == []:  # Init this if needed
            self.hint_age = [[[-1 for i in xrange(2)] for j in xrange(state.hands[0].size)] for k in xrange(len(state.players))]
        # Update hint ages
        # Set hint age to 0 for new hints
        if state.action.type == "color":
            for card in state.action.cards:
                self.hint_age[state.action.player][card][0] = 0
        if state.action.type == "number":
            for card in state.action.cards:
                self.hint_age[state.action.player][card][1] = 0
        # Assume no rearrangements.
        # If card is played or discarded, move the hint ages around.
        if state.action.type == "play" or state.action.type == "discard":
            self.hint_age[(state.curplayer + len(state.players) - 1) % len(state.players)].pop(state.action.cards)
            self.hint_age[(state.curplayer + len(state.players) - 1) % len(state.players)].append([-1 for i in xrange(2)])
            # So this can cause hint_age to be larger than it should be but whatever.
        # Increment all nonnegative ages.
        for i in xrange(len(self.hint_age)):
            for j in xrange(len(self.hint_age[i])):
                for k in xrange(len(self.hint_age[i][j])):
                    if self.hint_age[i][j][k] >= 0:
                        self.hint_age[i][j][k] += 1
    
    def scansim(self, state):  # Scanning for internal simulations. Same as scan, but doesn't update for new hints.
        if self.hint_age == []:  # Init this if needed
            self.hint_age = [[[-1 for i in xrange(2)] for j in xrange(state.hands[0].size)] for k in xrange(len(state.players))]
        # Update hint ages
        # Assume no rearrangements.
        # If card is played or discarded, move the hint ages around.
        if state.action.type == "play" or state.action.type == "discard":
            self.hint_age[(state.curplayer + len(state.players) - 1) % len(state.players)].pop(state.action.cards)
            self.hint_age[(state.curplayer + len(state.players) - 1) % len(state.players)].append([-1 for i in xrange(2)])
            # So this can cause hint_age to be larger than it should be but whatever.
        # Increment all nonnegative ages.
        for i in xrange(len(self.hint_age)):
            for j in xrange(len(self.hint_age[i])):
                for k in xrange(len(self.hint_age[i][j])):
                    if self.hint_age[i][j][k] >= 0:
                        self.hint_age[i][j][k] += 1
    
    
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
        # Give a small bonus to playing smaller-valued cards so you can build stacks earlier.
        score = 1.04 * state.stacks[0] + 1.03 * state.stacks[1] + state.stacks[2] + state.stacks[3] + state.stacks[4]
        if self.initdecksize > 1:
            score += state.hints * 0.35  # because a hint is worth less than a played card
            # This is lower than it might otherwise be to make the benefit of hinting and playing
            # greater than the benefit of discarding.
            if state.hints == 0: 
                score -= 0.7  # leave a hint for contingencies
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
            for i in xrange(len(state.players)):
                if len(state.hands[i].cards) > 0:
                    for j in xrange(state.hands[i].size):
                        if self.playable(state.hands[i].cards[j].color, state.hands[i].cards[j].number, state.stacks):
                            if (state.hands[i].info[j][0] > -1 and self.hint_age[i][j][0] < len(state.players) - 1) or (state.hands[i].info[j][1] > -1 and self.hint_age[i][j][1] < len(state.players) - 1) or (state.hands[i].info[j][0] > -1 and state.hands[i].info[j][1] > -1):
                                score += 0.7  # If card is playable and has young info or is fully known, that's good.
                                break  # Give only one such bonus per player.
            score += state.stacks[5] * 0.3  # A reasonable chance that something good was hinted.
        else:  # different end of game strat
            score += state.hints * 0.1  # because a hint is worth much less than a played card
            score += state.lives * 0.5
            # Don't even worry about bad discards..
        for i in range(len(state.players)):
            for j in range(state.hands[i].size):
                for k in range(2):
                    if state.hands[i].info[j][k] >= 0:
                        score += 0.02  # because it's good to have information
        for card in state.discards:
            score -= 0.11  # discourage extensive discarding
            if card.number < 5 and state.stacks[card.color] > card.number:
                # encourage discarding of unplayable cards
                score += 0.1
        if state.lives <= 0:  # dont die yo
                score -= 100
        return score
