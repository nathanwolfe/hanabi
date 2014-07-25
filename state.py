class State:
    def __init__(self, deck, disc, l, h, s, p, hands):
        # d = Deck, disc = list, l = int, hcount = int, s = list, p = list
        self.deck = deck
        self.discards = disc
        self.lives = l
        self.hcount = h  # hints
        self.stacks = s
        self.players = p
        self.hands = hands

    def calc_score(self):
        result = 0
        for i in range(len(self.stacks)):
            result += self.stacks[i]
        return result
