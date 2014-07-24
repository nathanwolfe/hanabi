class State:
    def __init__(self, deck, disc, l, h, s, p):
        # d = list, disc = list, l = int, hcount = int, s = list of lists, p = list
        self.deck = deck
        self.discards = disc
        self.lives = l
        self.hcount = h
        self.stacks = s  # 5x5 array, 1 if played in 0 if not
        self.players = p  # leave this for now I guess...
