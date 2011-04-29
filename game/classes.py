import pygame

class Enemy (pygame.sprite.Sprite):
    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        
        self.next_update_time = 0 # update() hasn't been called yet.
        
        self.velocity = [0,0]
        
        self.has_changed = False

    def update(self, current_time):
        # Update every 10 milliseconds = 1/100th of a second.
        if self.next_update_time < current_time:
            self.rect.top += self.velocity[0]
            self.rect.left += self.velocity[1]
            
            self.next_update_time = current_time + 10