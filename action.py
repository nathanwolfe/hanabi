# when the interface requests a move from the player, the player returns an Action


class Action:
    def __init__(self, t, c, p, i):
        self.type = t   # action type as string ("play", "discard", or "hint")
        self.card = c   # list of card positions in hand ([0] through [4], or list with multiple for hint)
        self.info = i   # card information (color string or number for hint, otherwise None)
        self.player = p   # hint recipient, if not hint None
