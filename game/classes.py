import pygame
import random

class Enemy (pygame.sprite.Sprite):
    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        
        self.next_update_time = 0 # update() hasn't been called yet.
        
        self.velocity = [0, 0]
        
        self.yeild = random.random()/3
        self.acceleration = 1

    def update(self, current_time):
        # Update every 10 milliseconds = 1/100th of a second.
        if self.next_update_time < current_time:
            self.rect.left += self.velocity[0]
            self.rect.top += self.velocity[1]
            
            self.next_update_time = current_time + 10
    
    def accelerate(self, target):
        x, y = self.rect.topleft
        tx, ty = target
        
        # X
        if random.random() > self.yeild:
            if x < tx:
                self.velocity[0] += self.acceleration
            else:
                self.velocity[0] -= self.acceleration
        
        # Y
        if random.random() > self.yeild:
            if y < ty:
                self.velocity[1] += self.acceleration
            else:
                self.velocity[1] -= self.acceleration
        
        
        self.velocity[0] = min(max(self.velocity[0], -8), 8)
        self.velocity[1] = min(max(self.velocity[1], -8), 8)


class Wall (pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([35, 35])
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    
    def update(self, current_time):
        pass

class Walkway (pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([35, 35])
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    
    def update(self, current_time):
        pass
