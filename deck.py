from card import Card


class Deck:
    def _init_(self, c):
        # c should be a list of Card objects
        self.cards = c

    def pop_card(self):
        return self.cards.pop()
