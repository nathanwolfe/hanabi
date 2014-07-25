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
        self.draw(state.deck)  # this needs to go first since this function actually returns stuff
        if self.is_valid(n, state):
            state.stacks[self.cards.color] += 1
            self.cards.pop(n)
            return True
        else:
            print "You lost a life"
            state.discards.append(self.cards.pop(n))
            return False

    def is_valid(c, state):
        # c is the card that is being tested against cs, the currently played cards.
        if state.stacks[c.color] is c.number:
            return True
        return False

    def discard(self, state, n):
        # d is the deck, disc is the discard
        state.discards.append(self.cards.pop(n))
        self.draw(state)

    def hint(self, positions, type, val):  # for when someone hints this hand
        # positions = cards hinted, type = "color" or "number", val = 0 - 4
        for i in positions:
            if (type == "color"):
                self.info[i][0] = val
            elif (type == "number"):
                self.info[i][1] = val

    def draw(self, state):
        # d is the deck
        if len(state.deck.cards) > 0:
            self.cards.append(state.deck.pop_card())


    # TODO - SWAPPING POSITIONS IN HAND.
