import json
import math

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
        
        self.tiles = {}
        self.pathway = {}
        
        self.start_tile = (1,0)
        self.end_tile = (0,0)
    
    def startup(self):
        """docstring for startup"""
        
        # self.enemies = pygame.sprite.Group()
        # self.enemies.add(classes.Enemy())
        
        super(RuneGame, self).startup()
        
        self.load_level(1)
        
        self.sprites.add(classes.Enemy((255,0,0), self.start_tile))
    
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
                    self.start_tile = x,y
                elif tile == "E":
                    self.background.blit(self.resources['end_image'], pos)
                    self.end_tile = x,y
                else:
                    raise KeyError("Key of '{0}' could not be handled".format(tile))
        
        
        # Now to pathfind
        self.build_pathway()
    
    def build_pathway(self):
        """
        Builds a pathway through the maze so that enemies know where to go.
        """
        def distance(pos1, pos2):
        	x = abs(pos1[0] - pos2[0])
        	y = abs(pos1[1] - pos2[1])
        	return math.sqrt(x*x + y*y)
        
        walked_tiles = set()
        dead_tiles = set()
        steps = []
        
        success = False
        
        # We start with the start_tile
        steps.append((self.start_tile, 9999))
        
        while not success:
            # Get our current position
            try:
                x, y = steps[-1][0]
            except Exception as e:
                # No steps? Means we've not got anywhere to go
                if steps == []:
                    raise Exception("No pathway found")
                raise
            
            view_dict = {
                "n":    (x, y-1),
                "e":    (x+1, y),
                "s":    (x, y+1),
                "w":    (x-1, y),
            }

            # Set the best_cost to something that any tile beats
            best_tile = [
                (-1,-1),# Tile
                9999999,# Distance
            ]
            
            for k, v in view_dict.items():
                if v == self.end_tile:
                    best_tile = [v, -1]
                    success = True
                    continue
                
                # We don't want to move back and forth all the time
                if v in walked_tiles: continue
                if v in dead_tiles: continue
                
                if v in self.tiles:
                    tile_type = self.tiles[v]
                else:
                    dead_tiles.add(v)
                    continue
                
                # If it's not a walkway we can't use it
                if tile_type != " ":
                    dead_tiles.add(v)
                    continue
                
                new_remaining = distance(v, self.end_tile)
                
                # Rank it
                if new_remaining < best_tile[1]:
                    best_tile = [v, new_remaining]
            
            # Dead end?
            if best_tile[0] == (-1,-1):
                # Lets jump back 1 step
                del(steps[-1])
                
            else:
                # We should now have a tile to move to
                s = tuple(best_tile)
                steps.append(s)
            
            # Ensure we don't go back over this one
            walked_tiles.add(best_tile[0])
        
        # We now have a list of steps taken
        self.pathway = {}
        last_step = None
        for tile, dist in steps:
            self.pathway[tile] = {"previous":last_step, "next":None}
            
            if last_step != None:
                self.pathway[last_step]["next"] = tile
            last_step = tile
    