import pygame
import random

import math

# Update every 10 milliseconds = 1/100th of a second
update_speed = 10

class Enemy (pygame.sprite.Sprite):
    reward = 0
    move_speed = 1
    
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = game.resources[self.image_name].copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (-100, -100)# Start offscreen
        
        self.next_update_time = 0 # update() hasn't been called yet.
        
        self.position = list(game.start_tile)
        self.target = tuple(game.start_tile)
        
        self.offset = game.tile_size/2 - game.enemy_size/2
        
        self.chasers = []
        self.disabled = False
        
        # This has to be set by the sub_class
        self.hp = self.max_hp
    
    def update(self, current_time):
        if self.disabled: return
        
        if self.next_update_time < current_time or True:
            if self.position[0] < self.target[0]:
                self.position[0] = min(self.position[0] + self.move_speed, self.target[0])
            elif self.position[0] > self.target[0]:
                self.position[0] = max(self.position[0] - self.move_speed, self.target[0])
            
            if self.position[1] < self.target[1]:
                self.position[1] = min(self.position[1] + self.move_speed, self.target[1])
            elif self.position[1] > self.target[1]:
                self.position[1] = max(self.position[1] - self.move_speed, self.target[1])
            
            self.rect.left = self.position[0] * 35 + self.offset
            self.rect.top = self.position[1] * 35 + self.offset
            
            self.next_update_time = current_time + update_speed

class Rune (pygame.sprite.Sprite):
    cost = 1
    shot_range = 1
    fire_speed = 100
    
    def __init__(self, game, position):
        pygame.sprite.Sprite.__init__(self)
        
        # Image is set by subclass
        # self.image = game.resources[self.image_name].copy()
        self.image = game.resources[self.image_name].copy()
        #pygame.Surface([game.rune_size, game.rune_size])
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (-100, -100)# Start offscreen
        
        self.next_update_time = 0 # update() hasn't been called yet.
        self.last_shot = 0
        
        self.position = list(position)
        
        self.offset = game.tile_size/2 - game.rune_size/2
        
        self.target = None
        self.game = game
        self.disabled = False
    
    def update(self, current_time):
        if self.disabled: return
        
        if self.next_update_time < current_time or True:
            self.rect.left = self.position[0] * 35 + self.offset
            self.rect.top = self.position[1] * 35 + self.offset
            
            if current_time > self.last_shot + self.fire_speed:
                self.shoot()
                self.last_shot = current_time
            
            self.next_update_time = current_time + update_speed
        
    def shoot(self):
        # Lose target if it goes out of range
        if self.target != None and self.distance(self.target) > self.shot_range:
            self.target = None
        
        # Pick a target from the enemies in the list
        if self.target == None:
            for e in self.game.enemies:
                if self.distance(e) <= self.shot_range:
                    self.target = e
                    break
        
        if self.target != None:
            s = self.shot_type(self.game, self.position, self.target)
            self.game.add_shot(s)
        else:
            pass
    
    def distance(self, enemy):
        x = abs(self.position[0] - enemy.position[0])
        y = abs(self.position[1] - enemy.position[1])
        return math.sqrt(x*x + y*y)

def angle_to_target(pos1, pos2):
    """
    pos1 and pos2 are both length 2 lists/tuples
    returned is the angle from pos1 to pos2
    returns in degrees
    """
    # SOH CAH TOA
    # We have the opposite and adjacent
    x = abs(pos1[0] - pos2[0])
    y = abs(pos1[1] - pos2[1])
    
    # Exacts, because in these cases we get a divide by 0 error
    if x == 0:
        if pos1[1] >= pos2[1]:# Up
            xy = 0
        elif pos1[1] < pos2[1]:# Down
            xy = 180
    elif y == 0:
        if pos1[0] <= pos2[0]:# Right
            xy = 90
        elif pos1[0] > pos2[0]:# Left
            xy = 270
    else:
        # Using trig
        if pos1[1] > pos2[1]:# Up
            if pos1[0] < pos2[0]:# Right
                xy = math.degrees(math.atan(x/y))
            else:# Left
                xy = math.degrees(math.atan(y/x)) + 270
        else:# Down
            if pos1[0] < pos2[0]:# Right
                xy = math.degrees(math.atan(y/x)) + 90
            else:# Left
                xy = math.degrees(math.atan(x/y)) + 180
    
    return xy

def make_vector(angle, distance):
    """
    distance is the 2D line going from origin at "angle"
    """
    
    if angle == 0:      return 0, -distance
    if angle == 90:     return distance, 0
    if angle == 180:    return 0, distance
    if angle == 270:    return -distance, 0
    
    opp = math.sin(math.radians(angle)) * distance
    adj = math.cos(math.radians(angle)) * distance
    
    return opp, -adj

def distance(pos1, pos2):
    x = abs(pos1[0] - pos2[0])
    y = abs(pos1[1] - pos2[1])
    
    d = math.sqrt(x*x + y*y)
    
    return d

class Bullet (pygame.sprite.Sprite):
    damage = 0
    move_speed = 0
    
    def __init__(self, game, position, target):
        pygame.sprite.Sprite.__init__(self)
        # Image is set by subclass
        self.image = pygame.Surface([8, 8])
        self.rect = self.image.get_rect()
        self.rect.topleft = (-100, -100)# Start offscreen
        
        self.next_update_time = 0 # update() hasn't been called yet.
        
        self.position = list(position)
        
        self.offset = game.tile_size/2 - self.rect.width/2
        
        self.game = game
        self.seeking = False
        
        if type(target) == list or type(target) == tuple:
            self.sprite_target = None
            self.target = target
        else:
            target.chasers.append(self)
            self.sprite_target = target
            self.target = target.position
    
    def update(self, current_time):
        if self.next_update_time < current_time or True:
            
            if self.sprite_target != None:
                self.target = self.sprite_target.position
            
            x,y = make_vector(
                angle_to_target(self.position, self.target),
                min(self.move_speed, distance(self.position, self.target))
            )
            
            self.position[0] += x
            self.position[1] += y
            
            if self.distance() < 0.2:
                self.hit()
            
            self.rect.left = self.position[0] * 35 + self.offset
            self.rect.top = self.position[1] * 35 + self.offset
            
            self.next_update_time = current_time + update_speed
    
    def distance(self):
        x = abs(self.position[0] - self.target[0])
        y = abs(self.position[1] - self.target[1])
        return math.sqrt(x*x + y*y)    
    
    def hit(self):
        if self.sprite_target != None:
            self.sprite_target.hp -= self.damage
            
            if self.sprite_target.hp <= 0:
                self.game.remove_enemy(self.sprite_target)
                self.game.kills += 1
                self.game.kill_display.text = "%s kill%s" % (self.game.kills, "" if self.game.kills == 1 else "s")
        
        self.game.remove_shot(self)
