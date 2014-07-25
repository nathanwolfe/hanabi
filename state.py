class State:
    def __init__(self, deck, disc, l, h, s, hands):
        # d = Deck, disc = list, l = int, hcount = int, s = list, hands = list of hand objects, hint = hint object
        self.deck = deck
        self.discards = disc
        self.lives = l
        self.hcount = h  # hints left
        self.stacks = s
        self.hands = hands # list of lists

    def calc_score(self):
        result = 0
        for i in range(len(self.stacks)):
            result += self.stacks[i]
        return result
