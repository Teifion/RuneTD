import pygame
import random

class Enemy (pygame.sprite.Sprite):
    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (-100, -100)# Start offscreen
        self.rect.topleft = (10,10)
        
        self.next_update_time = 0 # update() hasn't been called yet.
        
        self.position = list(initial_position)
        self.target = tuple(initial_position)
        
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
            
            self.rect.left = self.position[0] * 35 + 18 - self.rect.width/2
            self.rect.top = self.position[1] * 35 + 18 - self.rect.height/2
            
            self.next_update_time = current_time + 10