import pygame
import random

class Enemy (pygame.sprite.Sprite):
    def __init__(self, game, color, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([game.enemy_size, game.enemy_size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (-100, -100)# Start offscreen
        
        self.next_update_time = 0 # update() hasn't been called yet.
        
        self.position = list(position)
        self.target = tuple(position)
        
        self.offset = game.tile_size/2 - game.enemy_size/2
        
        self.move_speed = 1
        
    def update(self, current_time):
        # Update every 10 milliseconds = 1/100th of a second.
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
            
            self.next_update_time = current_time + 10

class Rune (pygame.sprite.Sprite):
    def __init__(self, game, position):
        pygame.sprite.Sprite.__init__(self)
        # Image is set by subclass
        self.image = pygame.Surface([game.rune_size, game.rune_size])
        self.rect = self.image.get_rect()
        self.rect.topleft = (-100, -100)# Start offscreen
        
        self.next_update_time = 0 # update() hasn't been called yet.
        
        self.position = list(position)
        
        self.offset = game.tile_size/2 - game.rune_size/2
        
        self.move_speed = 1
    
    def update(self, current_time):
        if self.next_update_time < current_time or True:
            self.rect.left = self.position[0] * 35 + self.offset
            self.rect.top = self.position[1] * 35 + self.offset
            
            self.next_update_time = current_time + 10

class Pink_rune (Rune):
    def __init__(self, game, position):
        super(Pink_rune, self).__init__(game, position)
        self.image = game.resources['pink_rune']
        
        