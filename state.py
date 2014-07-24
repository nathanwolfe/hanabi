class State:
    def __init__(self, deck, disc, l, h, s, p):
        # d = Deck, disc = list, l = int, hcount = int, s = list, p = list
        self.deck = deck
        self.discards = disc
        self.lives = l
        self.hcount = h  # hints
        self.stacks = s
        self.players = p
        #TODO: hands, hints given on this turn
