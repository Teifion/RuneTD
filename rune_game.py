class Rune_game (object):
    name = "Rune TD"
    
    def __init__(self):
        super(Rune_game, self).__init__()
        
        self.resources = []
    
    def get_background(self, x1, y1, x2, y2):
        """
        Return a picture of what to display as the background of the game.
        """
        
        return "media/background.png"
    
    def get_entities(self, x1, y1, x2, y2):
        """
        Return a list of all entities if the user's screen is viewing the
        area enclosed by the coordinates given.
        """
        
        return []