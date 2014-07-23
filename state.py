class State:
    def __init__(self, deck, disc, l, h, s):
        # d = list, disc = list, l = int, hcount = int, s = list of lists
        # this is not complete - we need to implement hands and stuff
        self.deck = deck
        self.discards = disc
        self.lives = l
        self.hcount = h
        self.stacks = s
        
