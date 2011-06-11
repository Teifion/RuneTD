import json
import math
import random
import time

import pygame

from engine import engine
from game import classes, enemies, runes, shots

class RuneGame (engine.EngineV2):
    name = "Rune TD"
    tile_size = 35
    
    fps = 40
    
    menu_width = 470
    
    window_width = 20 * tile_size + menu_width
    window_height = 20 * tile_size + 20
    
    enemy_size = 15
    rune_size = 30
    
    def __init__(self):
        super(RuneGame, self).__init__()
        
        self.resources = {
            # Use this to make a temporary bg image
            # it'll be ignore when we load a level
            "bg_image": pygame.image.load('media/wall.png'),
            "selector":     pygame.image.load('media/selector.png'),
            
            # Tiles
            "wall_image":       pygame.image.load('media/wall.png'),
            "walkway_image":    pygame.image.load('media/walkway.png'),
            
            "start_image":  pygame.image.load('media/start.png'),
            "end_image":    pygame.image.load('media/end.png'),
            
            # Enemies
            "Red triangle":     pygame.image.load('media/red_triangle.png'),
            "Blue circle":      pygame.image.load('media/blue_circle.png'),
            "Pink square":      pygame.image.load('media/pink_square.png'),
            "Orange octagon":   pygame.image.load('media/orange_octagon.png'),
            
            # Runes
            "Pink rune":    pygame.image.load('media/pink_rune.png'),
            "Blue rune":    pygame.image.load('media/blue_rune.png'),
            "Yellow rune":  pygame.image.load('media/yellow_rune.png'),
            "Green rune":   pygame.image.load('media/green_rune.png'),
            "Red rune":     pygame.image.load('media/red_rune.png'),
            "Teal rune":    pygame.image.load('media/teal_rune.png'),
            
            # Bullets
            "Pink bullet":      pygame.image.load('media/pink_bullet.png'),
            "Blue bullet":      pygame.image.load('media/blue_bullet.png'),
            "Yellow bullet":    pygame.image.load('media/yellow_bullet.png'),
            "Green bullet":     pygame.image.load('media/green_bullet.png'),
            "Red bullet":       pygame.image.load('media/red_bullet.png'),
            "Teal bullet":      pygame.image.load('media/teal_bullet.png'),
        }
        
        self.rune_types = {
            "Basic":    runes.BasicRune,
            "Slow":     runes.SlowRune,
            "Splash":   runes.SplashRune,
            "Poison":   runes.PoisonRune,
            "Critical": runes.CriticalRune,
            "Weaken":   runes.WeakenRune,
        }
        
        self.enemy_types = {
            "Red triangle":     enemies.RedTriangle,
            "Blue circle":      enemies.BlueCircle,
            "Pink square":      enemies.PinkSquare,
            "Orange octagon":   enemies.OrangeOctagon,
        }
        
        self.tiles = {}
        self.pathway = {}
        
        self.start_tile = (1,0)
        self.end_tile = (0,0)
        
        self.enemies = []
        self.runes = []
        self.shots = []
        
        # Level stuff
        self.level = 0
        self.level_data = {}
        self.wave = -1
        
        # Used to release enemies 1 at a time so that they don't all bunch up too much
        self.enemy_queue = []
        self.queue_pause_till = 0
        self.waiting_to_start = False
    
    def new_game(self):
        self.select_rune_type(rune="Basic")
        
        # Load new level
        self.load_level()
        
        self.kills = 0
        self.money = 100
        self.lives = 20
        
        for e in self.enemies[:]: self.remove_enemy(e)
        for r in self.runes[:]: self.remove_rune(r)
        for s in self.shots[:]: self.remove_shot(s)
        
        # Update based on money
        self.money_display.text = "%s gold" % len(self.runes)
        self.next_wave()
    
    def startup(self):
        super(RuneGame, self).startup()
        
        # Text displays
        self.enemies_on_screen = engine.Text_display((15, self.window_height-20), "0 enemies")
        self.runes_on_screen = engine.Text_display((150, self.window_height-20), "0 runes")
        self.money_display = engine.Text_display((250, self.window_height-20), "0 gold")
        self.kill_display = engine.Text_display((350, self.window_height-20), "0 kills")
        self.lives_display = engine.Text_display((450, self.window_height-20), "20 lives")
        
        self.status_display = engine.Text_display((800, self.window_height-20), "In progress")
        
        # Rune selection buttons
        self.basic_rune_button   = engine.Button((self.window_width - self.menu_width + 5, 15), self.resources['Pink rune'])
        self.basic_rune_button.button_up = self.select_rune_type
        self.basic_rune_button.button_up_kwargs = {"rune":"Basic"}
        self.add_button(self.basic_rune_button)
        self.basic_rune_text     = engine.Text_display((self.window_width - self.menu_width + 5, 50), "Basic rune", colour=(255,255,255))
        self.basic_rune_info     = engine.Text_display((self.window_width - self.menu_width + 5, 70),
            "Cost: %d, Effect: +1 damage" % runes.BasicRune.cost, font_size=14, colour=(255,255,255))
        
        self.slow_rune_button   = engine.Button((self.window_width - self.menu_width + 5, 95), self.resources['Blue rune'])
        self.slow_rune_button.button_up = self.select_rune_type
        self.slow_rune_button.button_up_kwargs = {"rune":"Slow"}
        self.add_button(self.slow_rune_button)
        self.slow_rune_text     = engine.Text_display((self.window_width - self.menu_width + 5, 130), "Slow rune", colour=(255,255,255))
        self.slow_rune_info     = engine.Text_display((self.window_width - self.menu_width + 5, 150),
            "Cost: %d, Effect: +1 range" % runes.SlowRune.cost, font_size=14, colour=(255,255,255))
        
        self.splash_rune_button = engine.Button((self.window_width - self.menu_width + 5, 175), self.resources['Yellow rune'])
        self.splash_rune_button.button_up = self.select_rune_type
        self.splash_rune_button.button_up_kwargs = {"rune":"Splash"}
        self.add_button(self.splash_rune_button)
        self.splash_rune_text   = engine.Text_display((self.window_width - self.menu_width + 5, 210), "Splash rune", colour=(255,255,255))
        self.splash_rune_info     = engine.Text_display((self.window_width - self.menu_width + 5, 230),
            "Cost: %d, Effect: +10%% rate of fire" % runes.SplashRune.cost, font_size=14, colour=(255,255,255))
        
        self.poison_rune_button  = engine.Button((self.window_width - self.menu_width + 5, 255), self.resources['Green rune'])
        self.poison_rune_button.button_up = self.select_rune_type
        self.poison_rune_button.button_up_kwargs = {"rune":"Poison"}
        self.add_button(self.poison_rune_button)
        self.poison_rune_text    = engine.Text_display((self.window_width - self.menu_width + 5, 290), "Poison rune", colour=(255,255,255))
        self.poison_rune_info     = engine.Text_display((self.window_width - self.menu_width + 5, 310),
            "Cost: %d, Effect: -1 Damage, +30%% rate of fire" % runes.PoisonRune.cost, font_size=14, colour=(255,255,255))
        
        self.critical_rune_button  = engine.Button((self.window_width - self.menu_width + 5, 335), self.resources['Red rune'])
        self.critical_rune_button.button_up = self.select_rune_type
        self.critical_rune_button.button_up_kwargs = {"rune":"Critical"}
        self.add_button(self.critical_rune_button)
        self.critical_rune_text    = engine.Text_display((self.window_width - self.menu_width + 5, 370), "Critical rune", colour=(255,255,255))
        self.critical_rune_info     = engine.Text_display((self.window_width - self.menu_width + 5, 390),
            "Cost: %d, Effect: +2 Damage, -10%% rate of fire" % runes.CriticalRune.cost, font_size=14, colour=(255,255,255))
        
        self.weaken_rune_button  = engine.Button((self.window_width - self.menu_width + 5, 415), self.resources['Teal rune'])
        self.weaken_rune_button.button_up = self.select_rune_type
        self.weaken_rune_button.button_up_kwargs = {"rune":"Weaken"}
        self.add_button(self.weaken_rune_button)
        self.weaken_rune_text    = engine.Text_display((self.window_width - self.menu_width + 5, 450), "Weaken rune", colour=(255,255,255))
        self.weaken_rune_info     = engine.Text_display((self.window_width - self.menu_width + 5, 470),
            "Cost: %d, Effect: +0.5 range" % runes.WeakenRune.cost, font_size=14, colour=(255,255,255))
        
        # Rune info text
        self.rune_info_text = []
        
        for i in range(3):
            t = engine.Text_display((self.window_width - self.menu_width + 5, self.window_height - 95 + (i * 25)), "", colour=(255,255,255))
            self.rune_info_text.append(t)
                
        # The 'button' that shows which rune we've selected
        self.rune_selector = engine.Button((100, 100), self.resources['selector'])
        self.sprites.add(self.rune_selector)
        
        # Text displays
        self.sprites.add(self.enemies_on_screen)
        self.sprites.add(self.runes_on_screen)
        self.sprites.add(self.money_display)
        self.sprites.add(self.kill_display)
        self.sprites.add(self.lives_display)
        self.sprites.add(self.status_display)
        
        for t in self.rune_info_text:
            self.sprites.add(t)
        
        # Rune menu at the right
        self.sprites.add(self.basic_rune_button)
        self.sprites.add(self.basic_rune_text)
        self.sprites.add(self.basic_rune_info)
        
        self.sprites.add(self.slow_rune_button)
        self.sprites.add(self.slow_rune_text)
        self.sprites.add(self.slow_rune_info)
        
        self.sprites.add(self.splash_rune_button)
        self.sprites.add(self.splash_rune_text)
        self.sprites.add(self.splash_rune_info)
        
        self.sprites.add(self.poison_rune_button)
        self.sprites.add(self.poison_rune_text)
        self.sprites.add(self.poison_rune_info)
        
        self.sprites.add(self.critical_rune_button)
        self.sprites.add(self.critical_rune_text)
        self.sprites.add(self.critical_rune_info)
        
        self.sprites.add(self.weaken_rune_button)
        self.sprites.add(self.weaken_rune_text)
        self.sprites.add(self.weaken_rune_info)
        
        # Information on the last x/y of the mouse
        self.last_mouse_pos = (-1, -1)
        
        # Start the new game
        self.new_game()
        
        self.enemies_on_screen.text = "%s %s" % (len(self.enemies), "enemy" if len(self.enemies) == 1 else "enemies")
        self.runes_on_screen.text = "%s runes" % len(self.runes)
        self.money_display.text = "%d gold" % self.money
        self.kill_display.text = "%s kill%s" % (self.kills, "" if self.kills == 1 else "s")
        self.lives_display.text = "%s %s" % (self.lives, "life" if self.lives == 1 else "lives")
    
    def select_rune_type(self, rune):
        self.selected_rune = rune
        
        if rune == "Basic":
            x, y = self.basic_rune_button.rect.left, self.basic_rune_button.rect.top
        elif rune == "Slow":
            x, y = self.slow_rune_button.rect.left, self.slow_rune_button.rect.top
        elif rune == "Poison":
            x, y = self.poison_rune_button.rect.left, self.poison_rune_button.rect.top
        elif rune == "Splash":
            x, y = self.splash_rune_button.rect.left, self.splash_rune_button.rect.top
        elif rune == "Critical":
            x, y = self.critical_rune_button.rect.left, self.critical_rune_button.rect.top
        elif rune == "Weaken":
            x, y = self.weaken_rune_button.rect.left, self.weaken_rune_button.rect.top
        
        self.rune_selector.rect.left = x-3
        self.rune_selector.rect.top = y-3
    
    def game_logic(self):
        # Waiting for wave to start
        if self.waiting_to_start:
            self.status_display.text = "%ss till wave start" % round(self.queue_pause_till - time.time(), 1)
        else:
            self.status_display.text = "%s %s in queue" % (len(self.enemy_queue), "enemy" if len(self.enemy_queue) == 1 else "enemies")
        
        # Release stuff?
        if time.time() > self.queue_pause_till:
            self.waiting_to_start = False
            if len(self.enemy_queue) > 0:
                e, delay_time = self.enemy_queue.pop(0)
                
                self.add_enemy(e)
                self.queue_pause_till = time.time() + delay_time
        
        for e in self.enemies:
            if tuple(e.position) == e.target:
                next = self.pathway[e.target]['next']
                
                if next == None:
                    self.enemy_reaches_end(e)
                else:
                    e.target = self.pathway[e.target]['next']
    
    def enemy_reaches_end(self, enemy):
        self.remove_enemy(enemy)
        self.lives -= 1
        self.lives_display.text = "%s %s" % (self.lives, "life" if self.lives == 1 else "lives")
        
        if self.lives <= 0:
            self.lose_game()
    
    def lose_game(self):
        for e in self.enemies: e.disabled = True
        for r in self.runes: r.disabled = True
        for s in self.shots: s.disabled = True
        
        self.status_display.text = "Game over"
    
    def add_enemy(self, enemy_name):
        enemy_type = self.enemy_types[enemy_name]
        e = enemy_type(self)
        
        self.enemies.append(e)
        self.sprites.add(e)
        self.enemies_on_screen.text = "%s enemies" % len(self.enemies)
    
    def remove_enemy(self, enemy):
        for r in self.runes:
            if r.target == enemy:
                r.target = None
        
        if enemy not in self.enemies:
            return
        
        # Give reward
        self.money += enemy.reward
        self.money_display.text = "%d gold" % self.money
        
        self.sprites.remove(enemy)
        self.enemies.remove(enemy)
        enemy.remove()
        self.enemies_on_screen.text = "%s enemies" % len(self.enemies)
        
        if len(self.enemies) < 1 and len(self.enemy_queue) < 1:
            self.next_wave()
    
    def remove_rune(self, rune):
        self.sprites.remove(rune)
        self.runes.remove(rune)
        
        rune.remove()
        self.runes_on_screen.text = "%s runes" % len(self.runes)
    
    def sell_rune(self, position):
        the_rune = None
        
        for r in self.runes:
            if r.position == list(position):
                the_rune = r
        
        if not the_rune:
            raise engine.Illegal_move("Cannot sell an empty tile")
        
        self.money += math.floor(the_rune.cost/2.0)
        self.money_display.text = "%d gold" % self.money
        
        self.remove_rune(the_rune)
    
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
        self.money_display.text = "%d gold" % self.money
        
        self.runes.append(new_rune)
        self.sprites.add(new_rune)
        self.runes_on_screen.text = "%s runes" % len(self.runes)
    
    def add_shot(self, shot):
        self.shots.append(shot)
        self.sprites.add(shot)
    
    def remove_shot(self, shot):
        try:
            self.shots.remove(shot)
            self.sprites.remove(shot)
            shot.remove()
        except Exception as e:
            pass
    
    def next_wave(self):
        if self.wave >= 0:
            self.money += self.level_data['reward']
            self.money_display.text = "%d gold" % self.money
        
        self.wave += 1
        
        # Feed the next wave into the queue
        if self.wave >= len(self.level_data['waves']):
            if not self.waiting_to_start:
                self.waiting_to_start = True
                
                self.complete_level()
                self.queue_pause_till = time.time() + 3
                
                current_wave = self.level_data['waves'][self.wave]
                
                for group in current_wave:
                    for i in range(group['count']):
                        self.enemy_queue.append((group['enemy'], group['delay']))
        
        else:
            self.waiting_to_start = True
            self.queue_pause_till = time.time() + 3
            
            # Give reward
            self.money += self.level_data['reward']
            self.money_display.text = "%d gold" % self.money
            
            current_wave = self.level_data['waves'][self.wave]
            
            for group in current_wave:
                for i in range(group['count']):
                    self.enemy_queue.append((group['enemy'], group['delay']))
    
    def complete_level(self):
        self.kills = 0
        self.money = 100
        self.lives = 20
        
        for e in self.enemies[:]: self.remove_enemy(e)
        for r in self.runes[:]: self.remove_rune(r)
        for s in self.shots[:]: self.remove_shot(s)
        
        # Load new level
        self.load_level()
    
    def victory(self):
        print("""
########
VICTORY!
########
""")
        self.quit()
    
    def handle_mouseup(self, event):
        x, y = event.pos
        x /= 35
        y /= 35
        
        if event.button == 1:
            try:
                self.add_rune(self.selected_rune, (x,y))
            except engine.Illegal_move as e:
                pass
            except KeyError as e:
                # Tried clicking outside of the tiles
                pass
            
        elif event.button == 3:
            try:
                self.sell_rune((x,y))
            except engine.Illegal_move as e:
                pass
            except KeyError as e:
                # Tried clicking outside of the tiles
                pass
    
    def handle_mousemotion(self, event):
        x, y = event.pos
        x /= 35
        y /= 35
        
        if (x,y) != self.last_mouse_pos:
            self.last_mouse_pos = (x,y)
            
            the_rune = None
            
            for r in self.runes:
                if r.position == [x,y]:
                    the_rune = r
                    break
            
            if the_rune == None:
                for t in self.rune_info_text:
                    t.text = ""
                return
            
            self.rune_info_text[0].text = str(the_rune.__class__)
            self.rune_info_text[1].text = str(the_rune.effects)
            
            
    
    def load_level(self):
        # Reset level counters
        self.level += 1
        self.wave = -1
        
        # Load terrain
        with open('game/levels.json') as f:
            try:
                json_data = json.load(f)
                self.level_data = json_data[str(self.level)]
            except KeyError as e:
                self.victory()
                return
            except Exception as e:
                raise
        
        self.background = pygame.display.get_surface()
        
        # Take them from data form and make them python objects
        for y, row in enumerate(self.level_data['floor']):
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
        
        self.screen.blit(self.background, pygame.Rect(0, 0, self.window_width, self.window_height))
        
        # Now to pathfind
        self.build_pathway()
    
    def build_pathway(self):
        """
        Builds a pathway through the maze so that enemies know where to go.
        It is very easy to trick the algorithm, some level designs may result
        in very stupid pathfinding
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
        
        
        # Next we run through the steps, we have a path but it may
        # be that the path loops around a little bit
        # we go through each step and if it is next to a step ahead
        # of itself then we cut straigth to that
        # thus generating the shortest path
        step_count = len(steps)
        i = -1
        
        while i < step_count-1:# Use while because we're re-ordering our steps list
            i += 1
            x1, y1 = steps[i][0]
            jumped = False
            
            for j in range(step_count-1, i+2, -1):
                if jumped: continue
                
                x2, y2 = steps[j][0]
                
                if abs(x1 - x2) > 1: continue
                if abs(y1 - y2) > 1: continue
                
                # It's next to another tile further on, we can jump it!
                for c in range(i+1, j):
                    del(steps[i+1])
                
                jumped = True
                step_count = len(steps)
        
        # We now have a list of steps taken
        self.pathway = {}
        last_step = None
        for tile, dist in steps:
            self.pathway[tile] = {"previous":last_step, "next":None}
            
            if last_step != None:
                self.pathway[last_step]["next"] = tile
            last_step = tile
    