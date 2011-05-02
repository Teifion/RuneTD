import json

import pygame

from engine import engine
from game import classes

class RuneGame (engine.EngineV2):
    name = "Rune TD"
    tile_size = 35
    
    fps = 40
    windowwidth = 40*tile_size
    windowheight = 22*tile_size
    
    def __init__(self):
        super(RuneGame, self).__init__()
        
        self.resources = {
            "bg_image": pygame.image.load('media/full_bg.png'),
            "wall_image": pygame.image.load('media/wall.png'),
            "walkway_image": pygame.image.load('media/walkway.png'),
        }
        
        self.walls = {}
        self.walkways = {}
        
        # Testing the ability to load levels
        self.load_level(1)
    
    def startup(self):
        """docstring for startup"""
        
        # self.enemies = pygame.sprite.Group()
        # self.enemies.add(classes.Enemy())
        
        super(RuneGame, self).startup()
    
    def game_logic(self):
        pass
        # for s in self.sprites:
        #     s.accelerate(self.mouse)
    
    def load_level(self, level):
        # Wipeout all the existing level terrain
        for k, s in self.walls.items(): s.kill()
        for k, s in self.walkways.items(): s.kill()
        
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
        
        # Take them from data form and make them python objects
        for y, row in enumerate(level_data['floor']):
            for x, tile in enumerate(row):
                pos = [x*self.tile_size, y*self.tile_size]
                
                if tile == "1":
                    self.walls[(x, y)] = classes.Wall(self.resources['wall_image'], pos)
                else:
                    self.walkways[(x, y)] = classes.Walkway(self.resources['walkway_image'], pos)
        
        # Add them to our sprite group
        for k, w in self.walls.items(): self.sprites.add(w)
        for k, w in self.walkways.items(): self.sprites.add(w)
        
        

