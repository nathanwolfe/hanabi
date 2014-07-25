# when the interface requests a move from the player, the player returns an Action


class Action:
	def __init__(self, t, c, p):
		self.type = t   # action type as string ("play", "discard", "number", or "color")
		self.card = c   # a single card position
		self.player = p   # hint recipient, if not hint None
