import json

import pygame

from engine import engine
from game import classes

class RuneGame (engine.EngineV2):
    name = "Rune TD"
    
    fps = 40
    windowwidth = 1024
    windowheight = 768
    
    def __init__(self):
        super(RuneGame, self).__init__()
        
        self.resources = {
            "bg_image": pygame.image.load('media/full_bg.png')
        }
        
        # Was used for testing some sprite stuff
        # self.sprites.add(classes.Enemy((255, 255, 255), [10,10]))
        # self.sprites.add(classes.Enemy((0, 255, 255), [10,10]))
        # self.sprites.add(classes.Enemy((255, 0, 255), [10,10]))
        # self.sprites.add(classes.Enemy((255, 255, 0), [10,10]))
        # self.sprites.add(classes.Enemy((0, 0, 255), [10,10]))
        # self.sprites.add(classes.Enemy((255, 0, 0), [10,10]))
        # self.sprites.add(classes.Enemy((0, 255, 0), [10,10]))
        # 
        # e = classes.Enemy((255, 255, 255), [10,10])
        # e.yeild = 0
        # self.sprites.add(e)
        
        # Testing the ability to load levels
        self.load_level(5)
    
    def startup(self):
        """docstring for startup"""
        
        # self.enemies = pygame.sprite.Group()
        # self.enemies.add(classes.Enemy())
        
        super(RuneGame, self).startup()
    
    def game_logic(self):
        for s in self.sprites:
            s.accelerate(self.mouse)
    
    def load_level(self, level):
        level = str(level)
        
        with open('game/levels.json') as f:
            try:
                json_data = json.load(f)
                level_data = json_data[level]
            except KeyError as e:
                print("Level '{0}' not found, level list: {1}".format(
                    level, list(json_data.keys())
                ))
                raise
            except Exception as e:
                raise
        
        self.quit()
