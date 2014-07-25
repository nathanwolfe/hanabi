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

    def rearrange(self, permute): # example: [3, 0, 1, 2, 4]: move the card currently #3 to be the leftmost card in hand
        assert len(permute) == len(cards)
        for i in range(len(cards)):
            assert i in permute
        tempcards = [None for i in range(len(cards))]
        tempinfo = [None for i in range(len(cards))]
        for i in range(len(cards)):
            tempcards[i] = self.cards[permute[i]]
            tempinfo[i] = self.info[permute[i]]
        self.cards = tempcards
        self.info = tempinfo


    # TODO - SWAPPING POSITIONS IN HAND.
