"""
Project Advisor: Mira Bernstein
Project Members: Andrew Li, Nathan Wolfe, Jerry Wu, Patrick Revilla, Alvin Kao, Cristina ________, Alex Chen, hope I didn't forget anyone
"""
from card import Card
from state import State
from deck import Deck
from game import Game
from player import Player
import deck_generator  # this is one of our own files


def is_valid(c, cs):
    # c is the card that is being tested against cs, the currently played cards.
    if cs[c.color] is c.number - 1:
        return True
    return False


def play(p, d, cs, n):
    # d is the deck (should only be one), n is the index 0-4 of the card being played
    # cs is card stack to play on.
    cs[p.cards[n].color] += 1
    p.cards.pop(n)
    draw(p, d)


def discard(p, d, disc, n):
    # d is the deck, disc is the discard
    disc.append(p.cards.pop(n))
    draw(p, d)


def draw(p, d):
    # d is the deck
    if (len(d.cards) > 0):
        p.cards.append(d.pop_card())


def main():
    deck_list = deck_generator.generate()
    deck = Deck(deck_list)
    # print deck.to_string()

    discard_pile = []
    lives = 3
    hints = 8
    card_stacks = [0 for i in range(5)]

    # cpp = cards per player
    numplayers = 2
    cpp = 5
    curplayer = 0

    phands = [[deck.pop_card() for i in range(cpp)] for j in range(numplayers)]  # initialize hands
    players = [Player(phands[i]) for i in range(numplayers)]  # initialize players

    for i in players:
        print "----------P" + str(curplayer + 1) + "-----------"
        for j in i.cards:
            print j.to_string()
        curplayer += 1

    # while curplayer still has cards, make a move.
    curplayer = 0
    while (len(players[curplayer].cards) > 0):
        print "----------P" + str(curplayer + 1) + "-----------"
        curmove = players[curplayer].move()
        if (curmove.type == "play"):
            play(players[curplayer], deck, card_stacks, 0)
        for k in players[curplayer].cards:
            print k.to_string()
        curplayer = (curplayer + 1) % numplayers

main()
