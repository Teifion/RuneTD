import pygame, random, sys, time, math
from pygame.locals import *

class Engine_v2 (object):
    def __init__(self):
        super(Engine_v2, self).__init__()
        self.keys_down = {}
        
        self.sprite_groups = []
    
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
        
        self.scroll_x = 0
        self.scroll_y = 0
        
        self.surface = pygame.display.set_mode((self.windowwidth, self.windowheight))
        pygame.display.set_caption(self.name)
        
        self.draw_window()
    
    def draw_text(self, text, font, surface, x, y):
        textobj = font.render(text, 1, (0,0,0))
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    def draw_window(self):
        # First the board
        background = pygame.Rect(0, 0, self.windowwidth, self.windowheight)
        
        bg_image, offset_x, offset_y = self.get_background(
            x1 = self.scroll_x, y1 = self.scroll_y,
            x2 = self.windowwidth, y2 = self.windowheight
        )
        
        self.surface.blit(self.resources["bg_image"], background)
        
        # Now the tiles
        # for x in range(0, 8):
        #     for y in range(0, 8):
        #         player = self.game.board[x][y]
        #         counter = pygame.Rect(x * TILE_SIZE + COUNTER_PADDING, y * TILE_SIZE + COUNTER_PADDING, COUNTER_SIZE, COUNTER_SIZE)
        #         
        #         if player == 1:
        #             self.surface.blit(self.resources['white'], counter)
        #         elif player == 2:
        #             self.surface.blit(self.resources['black'], counter)
        
        # Has a victory occurred?
        # font = pygame.font.SysFont("Helvetica", 48)
        # if self.game.victory == -1:
        #     self.drawText("Stalemate", font, self.surface, 95, 10)
        # if self.game.victory == 1:
        #     self.drawText("Victory to White", font, self.surface, 38, 10)
        # if self.game.victory == 2:
        #     self.drawText("Victory to Black", font, self.surface, 39, 10)
        
        pygame.display.update()
    
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

    def handle_mousemove(self, event):
        pass

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
                    self.handle_mousemove(event)
                
                else:
                    print(event)
            
            self.clock.tick(self.fps)
        
        quit()

