class State:
    def __init__(self, deck, disc, l, h, s, p):
        # d = Deck, disc = list, l = int, hcount = int, s = list, p = list
        self.deck = deck
        self.discards = disc
        self.lives = l
        self.hcount = h #hints
        self.stacks = s  # 5-array, one per color; entry is the # of cards played of that color
        self.players = p  # leave this for now I guess...
		
		#TODO: hands, hints given on this turn
