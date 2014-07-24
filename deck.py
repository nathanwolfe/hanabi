from card import Card


class Deck:
    def __init__(self, c):
        # c should be a list of Card objects
        self.cards = c

    def pop_card(self):
        # "drawing" a card (did not name "draw" cause that's probably going to be a player function)
        return self.cards.pop(0)

    def to_string(self):
        # merely prints out a list of the cards still in the deck
        s = ""
        for i in range(len(self.cards)):
            s += str(self.cards[i].number + 1) + self.cards[i].convert() + "\n"
        return s
