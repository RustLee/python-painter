import pygame
import sys
from pygame.locals import *

def capture(screen):
    
    fname1 = input('Choose the image to capture:(remember to add suffix!!!)')
    openfile = pygame.image.load(fname1)
    print("file {} has been opened".format(fname1))
    
    clock = pygame.time.Clock()
    
    select = 0
    select_rect = pygame.Rect(0,0,0,0)
    drag = 0
    anwser1 = 'Y'
    anwser2 = 'N'
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if select == 0 and drag ==0:
                        pos_start = event.pos
                        select = 1
                        
                    elif select == 2 and drag ==0:
                        capture = screen.subsurface(select_rect).copy()
                        cap_rect = capture.get_rect()
                        drag = 1
                            
                    elif select == 2 and drag == 2:
                        select = 0
                        drag = 0
                        anwser1 = input('Do you want to go on:(Y/y or N/n)')
                        if anwser1 == 'Y' or anwser1 =='y':
                            anwser2 = input('Do you want to save it:(Y/y or N/n)')
                            if anwser2 == 'Y' or anwser2 == 'y':
                                fname3 = input("Save as:(remember to add suffix!!!)")
                                pygame.image.save(capture,fname3)
                                print("file {} has been saved".format(fname3))
                            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if select == 1 and drag == 0:
                        pos_stop = event.pos
                        select = 2
                    if select == 2 and drag == 1:
                        drag = 2
        
        screen.fill((255,255,255))
        screen.blit(openfile,(80,80))
            
        if select:
            mouse_pos = pygame.mouse.get_pos()
            if select == 1:
                pos_stop = mouse_pos
            select_rect.left,select_rect.top = pos_start
            select_rect.width,select_rect.height = pos_stop[0] - pos_start[0],pos_stop[1] - pos_start[1]			
            pygame.draw.rect(screen,(0,0,0),select_rect,1)
        
        if drag:
            if drag == 1:
                cap_rect.center = mouse_pos
            screen.blit(capture,cap_rect)
            
        pygame.display.flip()
        
     
        if anwser1 == 'N' or anwser1 == 'n':
            anwser3 = input('Do you want to save it:(Y/y or N/n)')
            if anwser3 == 'Y' or anwser3 == 'y':
                fname2 = input("Save as:(remember to add suffix!!!)")
                pygame.image.save(capture,fname2)
                print("file {} has been saved".format(fname2))
            break;


