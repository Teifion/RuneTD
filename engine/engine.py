"""
Making heavy use of: http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml
"""

import sys
import time

import pygame
from pygame.locals import *

class EngineV2 (object):
    def __init__(self):
        super(EngineV2, self).__init__()
        self.keys_down = {}
        self.mouse = [0,0]
        
        self.mouse_is_down = False
        
        self.sprites = pygame.sprite.RenderUpdates()
    
    def game_logic(self):
        """
        This is called every execution loop to allow the game to do 'stuff'
        """
        raise Exception("{0}.game_logic() is not implimented".format(self.__class__))
    
    def quit(self):
        pygame.quit()
        sys.exit()
    
    # def _waitForPlayerToPressKey():
    #   while True:
    #       for event in pygame.event.get():
    #           if event.type == QUIT:
    #               quit()
    #           if event.type == KEYDOWN:
    #               if event.key == K_ESCAPE: # pressing escape quits
    #                   quit()
    #               return]
    
    def startup(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((self.windowwidth, self.windowheight))
        pygame.display.set_caption(self.name)
        
        self.draw_window()
    
    def draw_text(self, text, font, surface, x, y):
        textobj = font.render(text, 1, (0,0,0))
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    def draw_window(self):
        self.screen.blit(self.resources["bg_image"], [0, 0])
        pygame.display.update()
    
    def update_window(self):
        self.sprites.update(pygame.time.get_ticks())
        rectlist = self.sprites.draw(self.screen)
        pygame.display.update(rectlist)
        pygame.time.delay(10)
        self.sprites.clear(self.screen, self.resources["bg_image"])
    
    # Event handlers
    def handle_active(self, event):
        pass
    
    def handle_keydown(self, event):
        self.keys_down[event.key] = time.time()
        self.test_for_keyboard_commands()
    
    def handle_keyup(self, event):
        del(self.keys_down[event.key])
    
    def handle_mousedown(self, event):
        self.mouse_is_down = True
    
    def handle_mouseup(self, event):
        self.mouse_is_down = False
    
    def handle_mousemotion(self, event):
        self.mouse = event.pos
    
    def test_for_keyboard_commands(self):
        # Cmd + Q
        if 113 in self.keys_down and 310 in self.keys_down:
            if self.keys_down[310] <= self.keys_down[113]:# Cmd has to be pushed first
                quit()
        
        # Cmd + N
        # if 106 in self.keys_down and 310 in self.keys_down:
        #     if self.keys_down[310] <= self.keys_down[106]:# Cmd has to be pushed first
        #         self.new_game()
    
    def start(self):
        self.startup()
        
        # Dictionary lookup is faster than an if-statement
        # We're going to iterate over this loop so much it's well worth it
        func_dict = {
            ACTIVEEVENT:        self.handle_active,
            KEYDOWN:            self.handle_keydown,
            KEYUP:              self.handle_keyup,
            MOUSEBUTTONUP:      self.handle_mouseup,
            MOUSEBUTTONDOWN:    self.handle_mousedown,
            MOUSEMOTION:        self.handle_mousemotion,
        }
        
        while True:
            for event in pygame.event.get():
                if event.type in func_dict:
                    func_dict[event.type](event)
                else:
                    # print("Unhanded event {0}".format(event))
                    pass
            
            self.game_logic()
            self.update_window()
            self.clock.tick(self.fps)
        
        self.quit()

