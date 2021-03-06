import sys
import pygame
import math
import cv2
import numpy as np
import Capture as cp
import Scale as sc
import Lightless as lt
from pygame.locals import *
#Introduction:
#	Capture:'c'
#	Save:'s'
#	Open:'o'
#	Scale:'f'
#	Adjust lightness:'l'
#Warning:1.Maybe there are still some bugs!!!
#		 2.Please remember to save one image before you capture or open an image
#		 3.Sometimes it will be stuck(And I don't know why)
class Brush():
    def __init__(self, screen):
        
        self.screen = screen
        self.drawing = False
        
        self.color = (0, 0, 0)
        self.size = 1
        self.last_pos = None
        self.space = 1
       
        self.style = 0
        self.brush = pygame.image.load("images/brush.png")
      
        self.brush_now = self.brush.subsurface((0, 0), (1, 1))
 
    def start_draw(self, pos):
        self.drawing = True
       
        self.last_pos = pos
    def end_draw(self):
        self.drawing = False
    
    def set_brush_style(self,style):
        print("* set brush style to", style)
        self.style = style
    def get_brush_style(self):
        return self.style
 
    def get_current_brush(self):
        return self.brush_now
 
    def set_size(self, size):
        
        if size < 1: size = 1
        elif size > 50: size = 50
        print("* set brush size to", size)
        self.size = size
        
        self.brush_now = self.brush.subsurface((0, 0), (size*2, size*2))
    
    def get_size(self):
        return self.size
    
    def set_color(self, color):
        self.color = color
        for i in range(self.brush.get_width()):
            for j in range(self.brush.get_height()):
                self.brush.set_at((i, j), color + (self.brush.get_at((i, j)).a,))
    def get_color(self):
        return self.color
 
    def draw(self, pos):  
        
    
        if self.drawing:
             for p in self._get_points(pos):
             
                if self.style == 0:
                    pygame.draw.circle(self.screen, self.color, p, self.size)
                 
                
                elif self.style == 1:
               
                    self.screen.blit(self.brush_now, p)
                     
                else:
                    
                    pygame.draw.circle(self.screen, (0xff, 0xff, 0xff), p, self.size)
             self.last_pos = pos
 
    def _get_points(self, pos):

        points = [(self.last_pos[0], self.last_pos[1])]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]

        length = math.sqrt(len_x ** 2 + len_y ** 2)

        step_x = len_x / length
        step_y = len_y / length
        for i in range(int(length)):

            points.append((points[-1][0] + step_x, points[-1][1] + step_y))

        points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)

        return list(set(points))

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.brush = None
        self.colors = [
            (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
            (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
            (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
            (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
            (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
            (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
            (0xc0, 0xc0, 0xc0),
            (0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
        ]

        self.colors_rect = []

        for (i, rgb) in enumerate(self.colors):
            rect = pygame.Rect(10 + i % 2 * 32, 264 + 64 + i / 2 * 32, 32, 32)
            self.colors_rect.append(rect)
 
        self.pens = [
                pygame.image.load("images/pen1.png").convert_alpha(),
                pygame.image.load("images/pen2.png").convert_alpha(),
                pygame.image.load("images/eraser.jpg").convert_alpha()
        ]
      
        self.pens_rect = []
        for (i, img) in enumerate(self.pens):
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)
 
        self.sizes = [
                pygame.image.load("images/big.png").convert_alpha(),
                pygame.image.load("images/small.png").convert_alpha()
        ]
       
        self.sizes_rect = []
        for (i, img) in enumerate(self.sizes):
            rect = pygame.Rect(10 + i * 32, 148 + 64, 32, 32)
            self.sizes_rect.append(rect)
 
    def set_brush(self, brush):
        self.brush = brush
    
    def draw(self):
        for (i, img) in enumerate(self.pens):
            self.screen.blit(img, self.pens_rect[i].topleft)
        for (i, img) in enumerate(self.sizes):
            self.screen.blit(img, self.sizes_rect[i].topleft)
          
        self.screen.fill((255, 255, 255), (10, 254, 64, 64))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 254, 64, 64), 1)
        size = self.brush.get_size()
        x = 10 + 32
        y = 254 + 32
        if self.brush.get_brush_style():
            x = x - size
            y = y - size
            self.screen.blit(self.brush.get_current_brush(), (x, y))
        else:
            pygame.draw.circle(self.screen, self.brush.get_color(), (x, y), size)
 
        for (i, rgb) in enumerate(self.colors):
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])
   
    def click_button(self, pos):
     
        for (i, rect) in enumerate(self.pens_rect):
           
            if rect.collidepoint(pos):

                self.brush.set_brush_style(i)
                return True
 
        for (i, rect) in enumerate(self.sizes_rect):
            if rect.collidepoint(pos):
                
                if i: 
                    self.brush.set_size(self.brush.get_size() - 1)
                else:
                    self.brush.set_size(self.brush.get_size() + 1)
                return True
        
        for (i, rect) in enumerate(self.colors_rect):
           
            if rect.collidepoint(pos):
            
                self.brush.set_color(self.colors[i])
                return True
        return False
 
class Painter():
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Our Little Painter")
        self.clock = pygame.time.Clock()
        self.brush = Brush(self.screen)
        self.menu = Menu(self.screen)
        self.menu.set_brush(self.brush)
 
    def run(self):
        self.screen.fill((255, 255, 255))
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.screen.fill((255, 255, 255))
                    elif event.key == pygame.K_s:
                        fname1 = input("Save as:(remember to add suffix!!!)")
                        pygame.image.save(self.screen,fname1)
                        print("file {} has been saved".format(fname1))
                     
                    elif event.key == pygame.K_o:
                        fname2 = input("Open as:(remember to add suffix!!!)")
                        openfile = pygame.image.load(fname2)
                        print("file {} has been opened".format(fname2))
                        self.screen.blit(openfile,(80,80))
                        pygame.display.update()
                        
                             
                    elif event.key == pygame.K_c:
                        cp.capture(self.screen)
                    
                    elif event.key == pygame.K_f:
                        sc.scale(self.screen)
                        self.screen.fill((255,255,255))
                    
                    elif event.key == pygame.K_l:
                        lt.adjust(self.screen)
                        self.screen.fill((255,255,255))
                    
                    elif event.key == pygame.K_q:
                        sys.exit()

    
                elif event.type == MOUSEBUTTONDOWN:
                   
                    if ((event.pos)[0] <= 74 and self.menu.click_button(event.pos)):
                       
                        pass
                    else:
                        self.brush.start_draw(event.pos)
 
                elif event.type == MOUSEMOTION:
                    self.brush.draw(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    self.brush.end_draw()
              
                   
            self.menu.draw()
            pygame.display.update()

 
if __name__ == '__main__':
    app = Painter()
    app.run()

