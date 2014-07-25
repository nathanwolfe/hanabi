from card import Card
from state import State
from deck import Deck
from game import Game
from player import Player
import deck_generator  # this is one of our own files
import sys

CPP = 5
NUM_PLAYERS = 2


def is_valid(c, cs):
    # c is the card that is being tested against cs, the currently played cards.
    if cs[c.color] is c.number:
        return True
    return False


def play(p, d, cs, disc, n):
    # d is the deck (should only be one), n is the index 0-4 of the card being played
    # cs is card stack to play on, disc is discard
    # returns True if is_valid() is true, False if not
    draw(p, d)  # this needs to go first since this function actually returns stuff
    if (is_valid(p.cards[n], cs)):
        cs[p.cards[n].color] += 1
        p.cards.pop(n)
        return True
    else:
        print "You lost a life"
        disc.append(p.cards.pop(n))
        return False


def discard(p, d, disc, n):
    # d is the deck, disc is the discard
    disc.append(p.cards.pop(n))
    draw(p, d)


def draw(p, d):
    # d is the deck
    if (len(d.cards) > 0):
        p.cards.append(d.pop_card())


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

    phands = [[deck.pop_card() for i in range(CPP)] for j in range(NUM_PLAYERS)]  # initialize hands
    players = [Player(phands[i]) for i in range(NUM_PLAYERS)]  # initialize players

    # if confused see the State constructor in state.py
    g_state = State(deck, discard_pile, lives, hints, card_stacks, players)
    state_list = [g_state]
    game = Game(state_list)
    return game


def main():
    # CPP = cards per player
    curplayer = 0

    game = setup()

    for i in game.states[0].players:
        print "----------P" + str(curplayer + 1) + "-----------"
        for j in game.states[0].players.cards:
            print j.to_string()
        curplayer += 1

    # while curplayer still has cards, make a move.
    curplayer = 0
    curstate = 1
    final_countdown = NUM_PLAYERS
    while (True):
        state = game.states[curstate]
        print "----------P" + str(curplayer + 1) + "-----------"
        curmove = state.players[curplayer].move(state.stacks)
        if (curmove.type == "play"):
            if not play(state.players[curplayer], state.deck, state.stacks, state.discards, curmove.card):
                state.lives -= 1
        elif (curmove.type == "discard"):
            discard(state.players[curplayer], state.deck, state.discards, 0)
        for k in state.players[curplayer].cards:
            print k.to_string()
        curplayer = (curplayer + 1) % NUM_PLAYERS
        curstate += 1

        # recreate g_state and add to list of states - WILL NEED TO BE CHANGED WHEN HINT IS ADDED
        game.states.append(state)

        if len(state.deck.cards) == 0:
            final_countdown -= 1
        if state.lives <= 0 or state.calc_score() == 25 or final_countdown == 0:
            game_end(game)
main()
