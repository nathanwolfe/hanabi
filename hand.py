class Hand:
	
	# Color: Red Yellow Green Blue White -> 0 1 2 3 4
	info = [[-1 for j in range(2)] for i in range(4)]  # hint info you know
	#-1 means no info; 0 - 4 is for the value
	#info[i][0] = color, ...[1] = number

	def __init__(self, cards):
		self.cards = cards  # list of cards in the hand
		
	def play(self, pos):  # play the card in position pos
		# TODO: play and draw
		pass
		
	def discards(self, pos):  # discard the card in position pos
		# TODO: discard and draw
		pass
	
	def hint(self, positions, type, val):  # for when someone hints this hand
		# positions = cards hinted, type = "color" or "number", val = 0 - 4
		for i in positions:
			if (type == "color"):
				info[i][0] = val
			elif (type == "number"):
				info[i][1] = val
