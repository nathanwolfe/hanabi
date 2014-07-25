class Hand:

    # Color: Red Yellow Green Blue White -> 0 1 2 3 4
    #-1 means no info; 0 - 4 is for the value
    #info[i][0] = color, ...[1] = number

    def __init__(self, cards, s):
        self.cards = cards  # list of cards in the hand
        self.size = s
        self.info = [[-1 for j in range(2)] for i in range(self.size)]  # hint info you know

    def play(self, state, n):
        # returns True if is_valid() is true, False if not
        self.draw(state)  # this needs to go first since this function actually returns stuff
        if self.is_valid(n, state):
            state.stacks[self.cards[n].color] += 1
            self.cards.pop(n)
            return True
        else:
            print "You lost a life"
            state.discards.append(self.cards.pop(n))
            return False

    def is_valid(self, c, state):
        # c is the card index that is being tested against cs, the currently played cards.
        if state.stacks[self.cards[c].color] is self.cards[c].number:
            return True
        return False

    def discard(self, state, n):
        # d is the deck, disc is the discard
        state.discards.append(self.cards.pop(n))
        self.draw(state)

    def hint(self, pos, type):  # for when someone hints this hand
		# pos = card to hint, type = "color" or "number", val = 0 - 4
		# TODO: test this?
        for i in self.cards:
            if type == "color":
				if self.cards[i].color = self.cards[pos].color:
					self.info[i][0] = self.cards[pos].color
            else:
				assert type == "number", "invalid hint function call"
				if self.cards[i].number = self.cards[pos].number:
					self.info[i][1] = self.cards[pos].number
			

    def draw(self, state):
        # d is the deck
        if len(state.deck.cards) > 0:
            self.cards.append(state.deck.pop_card())

