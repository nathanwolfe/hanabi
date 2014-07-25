class Card:

    def __init__(self, c, n, i=[[0 for i in range(5)] for j in range(5)]):
        # number and color should both be ints
        # number and color both range 0 through 4
        """
        Color: Red Yellow Green Blue White -> 0 1 2 3 4
        """
        self.number = n
        self.color = c
        # this is the info that a player knows about the card - 0 if ?, 1 if yes, -1 if no
        # also keep in mind that info[i][j] will refer to whether the player knows if this is a card with color i and/or number j.
        self.info = i

    def to_string(self):
        # with the color first because that's how you say it
        return self.convert() + " " + str(self.number + 1)

    def convert(self):
        # lowercase lettering should be the convention..
        # this may be relatively ugly, but there are only five options anyway
        if self.color == 0:
            return "r"
        elif self.color == 1:
            return "y"
        elif self.color == 2:
            return "g"
        elif self.color == 3:
            return "b"
        elif self.color == 4:
            return "w"
