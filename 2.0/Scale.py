import pygame
from pygame.locals import *

def scale (screen):

    i = 0
    clock = pygame.time.Clock()
    print('Now you can scale the pic!!!')
    while True:
        if i >= 1:
            answer1 = input('Do you want to save it:(Y/y or N/n)')
            if answer1 == 'Y' or answer1 == 'y':
                fname = input("Save as:(remember to add suffix!!!)")
                pygame.image.save(surface,fname)
                print("file {} has been saved".format(fname))
            elif answer1 == 'N' or answer1 =='n':
                break 
            answer2 = input('Do you want to scale again:(Y/y or N/n)')
            if answer2 == 'N' or answer2 == 'n' :
                break
            elif answer2 =='Y' or answer2 =='y':
                print('Please scale again!!!')
        else:
            width = int(input('Change of width:'))
            height = int(input('Change of height:'))
            surface = pygame.transform.scale(screen,(width,height))
            screen.fill((255,255,255))
            screen.blit(surface,(width,height))
            pygame.display.update()
            i = i + 1
        clock.tick(1)


