import abc

class Game_template (object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def startup(self):
        """Called when the engine is ready to roll"""
        pass
    
    @abc.abstractmethod
    def get_background(self, x1, y1, x2, y2):
        """
        Return a picture of what to display as the background of the game. It also includes the X, Y offset
        """
        return "", 0, 0
    
    @abc.abstractmethod
    def get_entities(self, x1, y1, x2, y2):
        """
        Return a list of all sprites that the engine has to update
        """
        return []
    