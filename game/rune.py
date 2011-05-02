import json

import pygame

from engine import engine
from game import classes

class RuneGame (engine.EngineV2):
    name = "Rune TD"
    tile_size = 35
    
    fps = 40
    windowwidth = 30*tile_size
    windowheight = 20*tile_size
    
    def __init__(self):
        super(RuneGame, self).__init__()
        
        self.resources = {
            "bg_image": pygame.image.load('media/full_bg.png'),
            
            "wall_image": pygame.image.load('media/wall.png'),
            "walkway_image": pygame.image.load('media/walkway.png'),
            
            "start_image": pygame.image.load('media/start.png'),
            "end_image": pygame.image.load('media/end.png'),
        }
        
        self.sprites.add(classes.Enemy((255,0,0), (50,50)))
        
        self.tiles = {}
        
        self.start_tile = (1,0)
        self.end_tile = (0,0)
    
    def startup(self):
        """docstring for startup"""
        
        # self.enemies = pygame.sprite.Group()
        # self.enemies.add(classes.Enemy())
        
        super(RuneGame, self).startup()
        
        self.load_level(1)
    
    def game_logic(self):
        pass
        # for s in self.sprites:
        #     s.accelerate(self.mouse)
    
    def load_level(self, level):
        # Wipeout all the existing level terrain
        # for k, s in self.walls.items(): s.kill()
        # for k, s in self.walkways.items(): s.kill()
        
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
        
        # the_board = pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT)
        # self.surface.blit(self.resources['board'], the_board)
        
        self.background = pygame.display.get_surface()
        
        # Take them from data form and make them python objects
        for y, row in enumerate(level_data['floor']):
            for x, tile in enumerate(row):
                self.tiles[(x,y)] = tile
                pos = [x * self.tile_size, y * self.tile_size]
                
                if tile == " ":
                    # self.walkways[(x, y)] = classes.Tile(self.resources['walkway_image'], pos)
                    self.background.blit(self.resources['walkway_image'], pos)
                elif tile == "0":
                    self.background.blit(self.resources['wall_image'], pos)
                elif tile == "S":
                    self.background.blit(self.resources['start_image'], pos)
                    self.end_tile = pos
                elif tile == "E":
                    self.background.blit(self.resources['end_image'], pos)
                    self.start_tile = pos
                else:
                    raise KeyError("Key of '{0}' could not be handled".format(tile))
        #             
        # 
        # # Add them to our sprite group
        # for k, w in self.walls.items(): self.sprites.add(w)
        # for k, w in self.walkways.items(): self.sprites.add(w)
        # 
        # if self.start_tile != None: self.sprites.add(self.start_tile)
        # if self.end_tile != None: self.sprites.add(self.end_tile)

