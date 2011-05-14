"""
Making heavy use of: http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml
"""

import sys
import time

import pygame
from pygame.locals import *

class Game_error(Exception):
    """Errors related to the game in general"""
    pass

class Illegal_move(Game_error):
    """Errors from illegal moves"""
    pass

class Game_rule_error(Game_error):
    """Errors that arise from rule issues"""
    pass


class EngineV2 (object):
    fps = 40
    windowwidth = 800
    windowheight = 600
    
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
        
        # Default background
        self.background = self.resources['bg_image'].copy()
    
    def draw_text(self, text, font, surface, x, y):
        textobj = font.render(text, 1, (0,0,0))
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    def update_window(self):
        self.sprites.update(pygame.time.get_ticks())
        rectlist = self.sprites.draw(self.screen)
        pygame.display.update(rectlist)
        pygame.time.delay(10)
        
        # This method doesn't refresh correctly
        self.sprites.clear(self.screen, self.background)
        
        # This one does
        # self.sprites.clear(self.screen, self.resources['bg_image'])

    
    # Event handlers
    # Internal version allows us to sub-class without requiring a super call
    # makes the subclass cleaner
    def _handle_active(self, event):
        self.handle_active(event)
    
    def handle_active(self, event):
        pass
    
    def _handle_keydown(self, event):
        self.keys_down[event.key] = time.time()
        self.test_for_keyboard_commands()
        self.handle_keydown(event)
    
    def handle_keydown(self, event):
        pass
    
    def _handle_keyup(self, event):
        del(self.keys_down[event.key])
        self.handle_keyup(event)
    
    def handle_keyup(self, event):
        pass
    
    def _handle_mousedown(self, event):
        self.mouse_is_down = True
        self.handle_mousedown(event)
    
    def handle_mousedown(self, event):
        pass
    
    def _handle_mouseup(self, event):
        self.mouse_is_down = False
        self.handle_mouseup(event)
    
    def handle_mouseup(self, event):
        pass
    
    def _handle_mousemotion(self, event):
        self.mouse = event.pos
        self.handle_mousemotion(event)
        
        if self.mouse_is_down:
            self._handle_mousedrag(event)
        
    def handle_mousemotion(self, event):
        pass
    
    def _handle_mousedrag(self, event):
        self.handle_mousedrag(event)
    
    def handle_mousedrag(self, event):
        pass
    
    def test_for_keyboard_commands(self):
        # Cmd + Q
        if 113 in self.keys_down and 310 in self.keys_down:
            if self.keys_down[310] <= self.keys_down[113]:# Cmd has to be pushed first
                self.quit()
        
        # Cmd + N
        # if 106 in self.keys_down and 310 in self.keys_down:
        #     if self.keys_down[310] <= self.keys_down[106]:# Cmd has to be pushed first
        #         self.new_game()
    
    def start(self):
        self.startup()
        
        func_dict = {
            ACTIVEEVENT:        self._handle_active,
            KEYDOWN:            self._handle_keydown,
            KEYUP:              self._handle_keyup,
            MOUSEBUTTONUP:      self._handle_mouseup,
            MOUSEBUTTONDOWN:    self._handle_mousedown,
            MOUSEMOTION:        self._handle_mousemotion,
            QUIT:               self.quit,
        }
        
        while True:
            for event in pygame.event.get():
                if event.type in func_dict:
                    func_dict[event.type](event)
                else:
                    # raise Exception("Unhanded event {0}".format(event))
                    pass
            
            self.game_logic()
            self.update_window()
            self.clock.tick(self.fps)
        
        self.quit()

class Text_display (pygame.sprite.Sprite):
    def __init__(self, position, text, font_name="Helvetica", font_size=20):
        pygame.sprite.Sprite.__init__(self)
        
        self.font = pygame.font.SysFont(font_name, font_size)
        
        self.position = position
        
        self.text = text
        self._last_text = ""
        
    def update(self, *args, **kwargs):
        if self._last_text != self.text:
            self._last_text = self.text
            
            self.image = pygame.Surface(self.font.size(self.text))
            self.rect = self.image.get_rect()
            self.rect.topleft = self.position
            
            textobj = self.font.render(self.text, 1, (255,0,0))
            textrect = textobj.get_rect()
            textrect.topleft = (0, 0)
            self.image.blit(textobj, textrect)
    

class Button (pygame.sprite.Sprite):
    def __init__(self, position, text, font_name="Helvetica", font_size=20):
        pygame.sprite.Sprite.__init__(self)
        
        self.font = pygame.font.SysFont(font_name, font_size)
        
        self.position = position
        
        self.text = text
        self._last_text = ""
        
    def update(self, *args, **kwargs):
        if self._last_text != self.text:
            self._last_text = self.text
            
            self.image = pygame.Surface(self.font.size(self.text))
            self.rect = self.image.get_rect()
            self.rect.topleft = self.position
            
            textobj = self.font.render(self.text, 1, (255,0,0))
            textrect = textobj.get_rect()
            textrect.topleft = (0, 0)
            self.image.blit(textobj, textrect)
        