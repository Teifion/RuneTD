"""
Making heavy use of: http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml
"""

import pygame, random, sys, time, math
from pygame.locals import *

class EngineV2 (object):
    def __init__(self):
        super(EngineV2, self).__init__()
        self.keys_down = {}
        self.mouse = [0,0]
        
        self.sprites = pygame.sprite.RenderUpdates()
    
    def game_logic(self):
        """
        This is called every execution loop to allow the game 
        """
        raise Exception("{0}.game_logic() is not implimented".format(self.__class__))
    
    def quit():
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
    #               return
    
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
    
    def handle_keydown(self, event):
        self.keys_down[event.key] = time.time()
        self.test_for_keyboard_commands()

    def handle_keyup(self, event):
        del(self.keys_down[event.key])

    def handle_mousedown(self, event):
        pass

    def handle_mouseup(self, event):
        x, y = event.pos
        tx = int(math.floor(x/TILE_SIZE))
        ty = int(math.floor(y/TILE_SIZE))
        
        try:
            self.game.player_move(tx, ty)
        except reversi.Illegal_move as e:
            print("Illegal move")
        except Exception as e:
            raise

    def handle_mousemotion(self, event):
        self.mouse = event.pos

    def test_for_keyboard_commands(self):
        # Cmd + Q
        if 113 in self.keys_down and 310 in self.keys_down:
            if self.keys_down[310] <= self.keys_down[113]:# Cmd has to be pushed first
                quit()
        
        # Cmd + N
        if 106 in self.keys_down and 310 in self.keys_down:
            if self.keys_down[310] <= self.keys_down[106]:# Cmd has to be pushed first
                self.new_game()
    
    def new_game(self):
        self.game.__init__()
    
    def start(self):
        self.startup()
        
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.handle_keydown(event)
                
                elif event.type == KEYUP:
                    self.handle_keyup(event)
                
                elif event.type == MOUSEBUTTONUP:
                    self.handle_mouseup(event)
                
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_mousedown(event)
                
                elif event.type == MOUSEMOTION:
                    self.handle_mousemotion(event)
                
                else:
                    print(event)
            
            self.game_logic()
            self.update_window()
            self.clock.tick(self.fps)
        
        quit()

