class State:
	def __init__(self, deck, disc, l, h, s, hands, p, cp):
		# d = Deck, disc = list, l = int, hcount = int, s = list, hands = list of hand objects, hint = hint object, cp = current player
		self.deck = deck
		self.discards = disc
		self.lives = l
		self.hints = h  # hints left
		self.stacks = s
		self.hands = hands  # list of Hand objects
		self.players = p  # players
		self.curplayer = cp  # whoever's turn it is

	def calc_score(self):
		result = 0
		for i in range(len(self.stacks)):
			result += self.stacks[i]
		return result
