from card import Card
from state import State
from deck import Deck
from game import Game
from player import Player
from hand import Hand
import copy
import deck_generator  # this is one of our own files
import sys

HAND_SIZE = 5
NUM_PLAYERS = 2


def game_end(game):
    # add more stuff later, this is a end game clean up function.
    final_state = game.states[len(game.states) - 1]
    f = open("game_results.txt", "w")
    print "Game Over: Results"
    print final_state.stacks
    stacks_as_string = ", ".join(str(i) for i in final_state.stacks)
    f.write(stacks_as_string + "\n")
    print final_state.calc_score()
    print "Hints:"
    f.write("Score: " + str(final_state.calc_score()))

    f.write("Discarded cards:\n")
    for i in final_state.discards:
        f.write(i.to_string() + str("\n"))
    sys.exit()  # just exits the program.


def setup():
    deck = deck_generator.generate()
    discard_pile = []
    lives = 3
    hints = 8
    card_stacks = [0 for i in range(5)]

    phands = [[deck.pop_card() for i in range(HAND_SIZE)] for j in range(NUM_PLAYERS)]  # initialize hands

    hands = []
    for i in phands:
        hands.append(Hand(i, HAND_SIZE))
    players = [Player(i, NUM_PLAYERS) for i in range(NUM_PLAYERS)]  # initialize players

    # if confused see the State constructor in state.py
    g_state = State(deck, discard_pile, lives, hints, card_stacks, hands, players, 0, 0)
    state_list = [g_state]
    game = Game(state_list)
    return game


def main():
    game = setup()  # see setup function

    # print out all the cards of all the players for debug
    for i in game.states[0].hands:
        print "----------P" + str(game.states[0].curplayer + 1) + "-----------"
        for j in i.cards:
            print j.to_string()
        game.states[0].curplayer += 1

    game.states[0].curplayer = 0  # setting back to 0
    curturn = 0  # the current turn (first turn is turn 0)
    final_countdown = NUM_PLAYERS  # this is for when all the cards run out
    while True:
        # idea: copy current state, make moves, put this modified state as the new state
        # at end of states list of game, let players rearrange hand, let players look around.
        state = game.states[curturn]
        print "----------P" + str(state.curplayer + 1) + "-----------"
        # Censor information of player's own hand + the deck and then pass to the player for a move
        censored = copy.deepcopy(state)
        for i in xrange(len(censored.hands[state.curplayer].cards)):
            censored.hands[state.curplayer].cards[i] = Card(-1, -1, state.hands[state.curplayer].cards[i].ID)
        for i in xrange(len(censored.deck.cards)):
            censored.deck.cards[i] = Card(-1, -1, censored.deck.cards[i].ID)
        curmove = state.players[state.curplayer].move(censored, NUM_PLAYERS)
        if curmove.type == "play":
            print "Card played: " + state.hands[state.curplayer].cards[curmove.cards].to_string()
            if not state.hands[state.curplayer].play(state, curmove.cards):
                state.lives -= 1
        elif curmove.type == "discard":
            print "Card destructioned: " + state.hands[state.curplayer].cards[curmove.cards].to_string()
            state.hands[state.curplayer].discard(state, curmove.cards)
            if state.hints < 8:
                state.hints += 1
        elif curmove.type == "color":
            hinted = state.hands[curmove.player].hint(curmove.cards, "color")
            assert state.hints > 0, "Tried to hint when out of hints: player " + str(state.curplayer + 1)
            state.hints -= 1
            curmove.cards = hinted  # Before attaching, correct the action to list all cards hinted
        else:
            assert curmove.type == "number", "invalid move string specified"
            hinted = state.hands[curmove.player].hint(curmove.cards, "number")
            assert state.hints > 0, "Tried to hint when out of hints: player " + str(state.curplayer + 1)
            state.hints -= 1
            curmove.cards = hinted
        state.attach_action(curmove)

        # recreate g_state and add to list of states
        print state.stacks
        for p in state.players:
            # censor hands + the deck then pass for lookaround
            visible = copy.deepcopy(state)
            for i in xrange(len(visible.hands[p.number].cards)):
                visible.hands[p.number].cards[i] = Card(-1, -1, visible.hands[p.number].cards[i].ID)
            for i in xrange(len(visible.deck.cards)):
                visible.deck.cards[i] = Card(-1, -1, visible.deck.cards[i].ID)
            p.analyze(visible, NUM_PLAYERS)

        # Andrew - now only rearranges once per thingy
        # censor each player's hands + the deck, then pass state for rearrangement
        visible = copy.deepcopy(state)
        for i in xrange(len(visible.hands[state.curplayer].cards)):
            visible.hands[state.curplayer].cards[i] = Card(-1, -1, visible.hands[state.curplayer].cards[i].ID)
        for i in xrange(len(visible.deck.cards)):
            visible.deck.cards[i] = Card(-1, -1, visible.deck.cards[i].ID)
        permutation = state.players[state.curplayer].rearrange(visible)
        state.hands[state.curplayer].rearrange(permutation)

        # debug
        for k in state.hands[state.curplayer].cards:
            print k.to_string()

        state.curplayer = (state.curplayer + 1) % NUM_PLAYERS
        curturn += 1
        state.turns = curturn

        game.states.append(state)
        if len(state.deck.cards) == 0:
            final_countdown -= 1
        if state.lives <= 0 or state.calc_score() == 25 or final_countdown == 0:
            if state.lives <= 0:
                print "btdubs you died"
            game_end(game)

main()
