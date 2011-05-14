import json
import math
import random

import pygame

from engine import engine
from game import classes, enemies, runes, shots

class RuneGame (engine.EngineV2):
    name = "Rune TD"
    tile_size = 35
    
    fps = 40
    windowwidth = 30*tile_size
    windowheight = 20*tile_size + 20
    
    enemy_size = 15
    rune_size = 30
    
    def __init__(self):
        super(RuneGame, self).__init__()
        
        self.resources = {
            "bg_image": pygame.image.load('media/full_bg.png'),
            
            # Tiles
            "wall_image": pygame.image.load('media/wall.png'),
            "walkway_image": pygame.image.load('media/walkway.png'),
            
            "start_image": pygame.image.load('media/start.png'),
            "end_image": pygame.image.load('media/end.png'),
            
            # Enemies
            
            # Runes
            "PinkRune": pygame.image.load('media/rune.png'),
            
            # Bullets
            "PinkBullet": pygame.image.load('media/bullet.png'),
        }
        
        self.rune_types = {
            "Pink": runes.PinkRune,
        }
        
        self.tiles = {}
        self.pathway = {}
        
        self.start_tile = (1,0)
        self.end_tile = (0,0)
        
        self.enemies = []
        self.runes = []
        self.shots = []
    
    def new_game(self):
        # Load new level
        self.load_level(1)
        
        self.kills = 0
        self.money = 100
        self.lives = 20
        
        for e in self.enemies: self.remove_enemy(e)
        for r in self.runes: self.remove_rune(r)
        for s in self.shots: self.remove_shot(s)
        
        # Update based on money
        self.money_display.text = "%s gold" % len(self.runes)
    
    def startup(self):
        super(RuneGame, self).startup()
        
        # Text displays
        self.enemies_on_screen = engine.Text_display((15, self.windowheight-20), "0 enemies")
        self.runes_on_screen = engine.Text_display((150, self.windowheight-20), "0 runes")
        self.money_display = engine.Text_display((250, self.windowheight-20), "0 gold")
        self.kill_display = engine.Text_display((350, self.windowheight-20), "0 kills")
        self.lives_display = engine.Text_display((450, self.windowheight-20), "20 lives")
        
        self.status_display = engine.Text_display((900, self.windowheight-20), "In progress")
        
        self.sprites.add(self.enemies_on_screen)
        self.sprites.add(self.runes_on_screen)
        self.sprites.add(self.money_display)
        self.sprites.add(self.kill_display)
        self.sprites.add(self.lives_display)
        self.sprites.add(self.status_display)
        
        # Start the new game
        self.new_game()
        
        for i in range(0,50):
            e = enemies.Goblin(self, (255,0,0), self.start_tile)
            e.move_speed = min(random.random(), 0.75) + 0.25
            self.add_enemy(e)
        
        self.enemies_on_screen.text = "%s %s" % (len(self.enemies), "enemy" if len(self.enemies) == 1 else "enemies")
        self.runes_on_screen.text = "%s runes" % len(self.runes)
        self.money_display.text = "%s gold" % self.money
        self.kill_display.text = "%s kill%s" % (self.kills, "" if self.kills == 1 else "s")
        self.lives_display.text = "%s %s" % (self.lives, "life" if self.lives == 1 else "lives")
        
    def game_logic(self):
        for e in self.enemies:
            if tuple(e.position) == e.target:
                next = self.pathway[e.target]['next']
                
                if next == None:
                    self.enemy_reaches_end(e)
                else:
                    e.target = self.pathway[e.target]['next']
    
    def enemy_reaches_end(self, enemy):
        for i in range(0,5):
            e = enemies.Goblin(self, (255,0,0), self.start_tile)
            e.move_speed = max(random.random(), 0.6) - 0.5
            
            self.add_enemy(e)
        
        self.remove_enemy(enemy)
        self.lives -= 1
        self.lives_display.text = "%s %s" % (self.lives, "life" if self.lives == 1 else "lives")
        
        if self.lives <= 0:
            self.lose_game()
    
    def lose_game(self):
        for e in self.enemies: e.disabled = True
        for r in self.runes: r.disabled = True
        for s in self.shots: s.disabled = True
        
        print("\nGAME OVER\n")
    
    def add_enemy(self, enemy):
        self.enemies.append(enemy)
        self.sprites.add(enemy)
        self.enemies_on_screen.text = "%s enemies" % len(self.enemies)
    
    def remove_enemy(self, enemy):
        for r in self.runes:
            if r.target == enemy:
                r.target = None
        
        if enemy not in self.enemies:
            return
        
        self.sprites.remove(enemy)
        self.enemies.remove(enemy)
        enemy.remove()
        self.enemies_on_screen.text = "%s enemies" % len(self.enemies)
    
    def remove_rune(self, rune):
        self.sprites.remove(enemy)
        self.runes.remove(enemy)
        self.runes_on_screen.text = "%s runes" % len(self.runes)
    
    def add_rune(self, rune_name, position):
        rune_type = self.rune_types[rune_name]
        new_rune = rune_type(self, position)
        
        if self.tiles[position] != "0":
            raise engine.Illegal_move("Can only place a rune on a wall")
        
        if self.money < rune_type.cost:
            raise engine.Illegal_move("No money")
        
        for r in self.runes:
            if r.position == list(position):
                raise engine.Illegal_move("Can only place a rune on top of another rune")
        
        self.money -= new_rune.cost
        self.money_display.text = "%s gold" % self.money
        
        self.runes.append(new_rune)
        self.sprites.add(new_rune)
        self.runes_on_screen.text = "%s runes" % len(self.runes)
    
    def add_shot(self, shot):
        self.shots.append(shot)
        self.sprites.add(shot)
    
    def remove_shot(self, shot):
        self.shots.remove(shot)
        self.sprites.remove(shot)
    
    def handle_mouseup(self, event):
        x, y = event.pos
        x /= 35
        y /= 35
        
        try:
            self.add_rune("Pink", (x,y))
        except engine.Illegal_move as e:
            pass
    
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
        
        # Sets the background in such a way the sprites refresh correctly
        self.background = self.background.copy()
        
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
    