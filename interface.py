from card import Card
from state import State
from deck import Deck
from game import Game
from player import Player
from hand import Hand
import deck_generator  # this is one of our own files
import sys

HAND_SIZE = 5
NUM_PLAYERS = 2


def game_end(game):
    # add more stuff later, this is a end game clean up function.
    print "Game Over: Results"
    print game.states[len(game.states) - 1].stacks

    print game.states[len(game.states) - 1].calc_score()

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
    players = [Player(phands[i]) for i in range(NUM_PLAYERS)]  # initialize players

    # if confused see the State constructor in state.py
    g_state = State(deck, discard_pile, lives, hints, card_stacks, hands, players, 0)
    state_list = [g_state]
    game = Game(state_list)
    return game


def main():
    game = setup()  # see setup function

    # merely print out all the cards of all the players
    for i in game.states[0].hands:
        print "----------P" + str(game.states[0].curplayer + 1) + "-----------"
        for j in i.cards:
            print j.to_string()
        game.states[0].curplayer += 1

    game.states[0].curplayer = 0  # setting back to 0
    curstate = 0  # the current turn (first turn is turn 0)
    final_countdown = NUM_PLAYERS  # this is for when all the cards run out
    while True:
        # idea: copy current state, make moves, put this modified state as the new state at end of states list of game.
        state = game.states[curstate]
        print "----------P" + str(state.curplayer + 1) + "-----------"
        curmove = state.players[state.curplayer].move(state.stacks)
        if curmove.type == "play":
            if not state.hands[state.curplayer].play(state, curmove.card):
                state.lives -= 1
        elif curmove.type == "discard":
            state.hands[state.curplayer].discard(state, curmove.card)
            if state.hints < 8:
                state.hints += 1
        for k in state.hands[state.curplayer].cards:
            print k.to_string()
        state.curplayer = (state.curplayer + 1) % NUM_PLAYERS
        curstate += 1

        # recreate g_state and add to list of states - WILL NEED TO BE CHANGED WHEN HINT IS ADDED
        game.states.append(state)

        if len(state.deck.cards) == 0:
            final_countdown -= 1
        if state.lives <= 0 or state.calc_score() == 25 or final_countdown == 0:
            game_end(game)
        # TODO: Players forage for information
main()
