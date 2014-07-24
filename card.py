class Card:

    def __init__(self, c, n):
        # number and color should both be ints
		# number and color both range 0 through 4
        """
        Color: Red Yellow Green Blue White -> 0 1 2 3 4
        """
        self.number = n
        self.color = c
        
        # See TODO for important stuff to fill in here: trooleans
		## Unless player tracks that personally?

    def to_string(self): 
		#with the color first because that's how you say it
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
    
    
