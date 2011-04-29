import pygame
from engine import engine
from game import classes

class Rune_game (engine.Engine_v2):
    name = "Rune TD"
    
    fps = 40
    windowwidth = 1024
    windowheight = 768
    
    def __init__(self):
        super(Rune_game, self).__init__()
        
        self.resources = {
            "bg_image": pygame.image.load('media/full_bg.png')
        }
    
    def startup(self):
        """docstring for startup"""
        
        # self.enemies = pygame.sprite.Group()
        # self.enemies.add(classes.Enemy())
        
        super(Rune_game, self).startup()
    
    def get_background(self, x1, y1, x2, y2):
        """
        Return a picture of what to display as the background of the game. It also includes the X, Y offset
        """
        
        return "media/full_bg.png", 0, 0
    
    def get_entities(self, x1, y1, x2, y2):
        """
        Return a list of all entities if the user's screen is viewing the
        area enclosed by the coordinates given.
        """
        
        return [self.enemies]
