class State:
    def __init__(self, deck, disc, l, h, s, hands, p, cp, t):
        # d = Deck, disc = list, l = int, hcount = int, s = list, hands = list of hand objects, p = list of players, cp = current player, t = turns passed
        self.deck = deck
        self.discards = disc
        self.lives = l
        self.hints = h  # hints left
        self.stacks = s
        self.hands = hands  # list of Hand objects
        self.players = p  # players
        self.curplayer = cp  # whoever's turn it is
        self.turns = t  # how many turns have passed?
        self.action_list = []  # list of all past actions

    def attach_action(self, a):  # Attaches an action to this state. For interface use only.
        self.action_list.append(a)

    def calc_score(self):
        result = 0
        for i in range(len(self.stacks)):
            result += self.stacks[i]
        return result
