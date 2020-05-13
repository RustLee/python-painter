import cv2
import pygame
from pygame.locals import *

def adjust(screen): 
    i = 0
    clock = pygame.time.Clock()
    print('Now you can process the pic!!!')
    while True:
        if i >= 1:
            answer1 = input('Do you want to save it:(Y/y or N/n)')
            if answer1 == 'Y' or answer1 == 'y':
                fname = input("Save as:(remember to add suffix!!!)")
                pygame.image.save(openfile,fname)
                print("file {} has been saved".format(fname))
            elif answer1 == 'N' or answer1 =='n':
                break
            answer2 = input('Do you want to process again:(Y/y or N/n)')
            if answer2 == 'N' or answer2 == 'n' :
                break
            elif answer2 =='Y' or answer2 =='y':
                print('Please process again!!!')
        
        
        else:
            fname1 = input('Please open the picture you want to process:(remember to add suffix!!!)')
            img = cv2.imread(fname1)
            rows,cols,channels=img.shape
            dst = img.copy()
 
            print('Please input the Parameter:')
            a=float(input('alpha:'))
            b=float(input('beta:'))
            for i in range(rows):
                for j in range(cols):
                    for c in range(3):
                        color=img[i,j][c]*a+b
                        if color>255:
                            dst[i,j][c]=255
                        elif color<0:
                            dst[i,j][c]=0
            cv2.imwrite('after.jpg',dst)
 
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            openfile = pygame.image.load('after.jpg')
            position = openfile.get_rect()
            screen.blit(openfile,position)
            pygame.display.update()
            i = i + 1
            
