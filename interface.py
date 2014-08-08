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
NUM_PLAYERS = 3


def game_end(game):
    # add more stuff later, this is a end game clean up function.
    f = open("game_results.txt", "w")
    print "Game Over: Results"
    print game.states[len(game.states) - 1].stacks
    stacks_as_string = ", ".join(str(i) for i in game.states[len(game.states) - 1].stacks)
    f.write(stacks_as_string + "\n")
    print game.states[len(game.states) - 1].calc_score()
    print game.states[len(game.states) - 1].lives
    f.write("Score: " + str(game.states[len(game.states) - 1].calc_score()))
    
    # sys.exit()  # just exits the program.
    return game.states[len(game.states) - 1].calc_score()


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
    players = [Player(i) for i in range(NUM_PLAYERS)]  # initialize players

    # if confused see the State constructor in state.py
    g_state = State(deck, discard_pile, lives, hints, card_stacks, hands, players, 0)
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
        censored.hands[state.curplayer].cards = []
        censored.players = []
        for i in xrange(len(censored.deck.cards)):
            censored.deck.cards[i] = Card(0, 0)
        curmove = state.players[state.curplayer].move(censored)
        if curmove.type == "play":
            if not state.hands[state.curplayer].play(state, curmove.cards):
                state.lives -= 1
        elif curmove.type == "discard":
            state.hands[state.curplayer].discard(state, curmove.cards)
            if state.hints < 8:
                state.hints += 1
        elif curmove.type == "color":
            hinted = state.hands[curmove.player].hint(curmove.cards, "color")
            assert state.hints > 0, "Tried to hint when out of hints: player " + str(state.curplayer)
            state.hints -= 1
            curmove.cards = hinted  # Before attaching, correct the action to list all cards hinted
        else:
            assert curmove.type == "number", "invalid move string specified"
            hinted = state.hands[curmove.player].hint(curmove.cards, "number")
            assert state.hints > 0, "Tried to hint when out of hints: player " + str(state.curplayer)
            state.hints -= 1
            curmove.cards = hinted
        state.attach_action(curmove)
        # debug
        for k in state.hands[state.curplayer].cards:
            print k.to_string()

        # recreate g_state and add to list of states - WILL NEED TO BE CHANGED WHEN HINT IS ADDED
        # Why does this need to be changed? --Jerry
        game.states.append(state)
        visible = [None] * NUM_PLAYERS
        for i in range(NUM_PLAYERS):
            visible[i] = copy.deepcopy(state)

        for p in state.players:
            # censor each player's hands + the deck, then pass state for rearrangement
            visible[p.number].hands[p.number].cards = []
            for i in xrange(len(visible[p.number].deck.cards)):
                visible[p.number].deck.cards[i] = Card(0, 0)
            permutation = p.rearrange(visible[p.number])
            state.hands[p.number].rearrange(permutation)

        for p in state.players:
            # censor hands + the deck then pass for lookaround
            visible = copy.deepcopy(state)
            visible.hands[p.number].cards = []
            for i in xrange(len(visible.deck.cards)):
                visible.deck.cards[i] = Card(0, 0)
            p.scan(visible)

        assert state.players[0].playable == state.players[1].playable == state.players[2].playable
        
        state.curplayer = (state.curplayer + 1) % NUM_PLAYERS
        curturn += 1
        
        if len(state.deck.cards) == 0:
            final_countdown -= 1
        if state.lives <= 0 or state.calc_score() == 25 or final_countdown == 0:
            if state.lives <= 0:
                print "Game lost."
            return game_end(game)
main()
