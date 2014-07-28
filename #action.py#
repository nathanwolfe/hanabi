# when the interface requests a move from the player, the player returns an Action


class Action:
    def __init__(self, t, c, p):
        self.type = t   # action type as string ("play", "discard", "number", or "color")
        self.cards = c   # a single card position unless this action is attached to a state and it's a hint, in which case it's a list of card positions.
        self.player = p   # hint recipient, if not hint None
