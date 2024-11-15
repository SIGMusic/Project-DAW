#   very beginnery code for daw im not sure what im doing
#   created 11/10/24
#   emmett quan 👍

import pygame, sys
from pygame.locals import *

WHITE = (255, 255, 255)
WIDTH = 1200
HEIGHT = 800
BOXSIZE = 40
GAPSIZE = 10
XMARGIN = int((WIDTH - (WIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((HEIGHT - (HEIGHT * (BOXSIZE + GAPSIZE))) / 2)

def main():
    pygame.init()
    pygame.display.set_caption("pungi")

    #drawing guidelines for buttons
    DISPLAYSURF = pygame.display.set_mode((1200, 800))
    pygame.draw.line(DISPLAYSURF, WHITE, (0, 450), (950, 450))
    pygame.draw.line(DISPLAYSURF, WHITE, (0, 550), (950, 550))
    pygame.draw.line(DISPLAYSURF, WHITE, (950, 0), (950, 800))

    mouseX = 0
    mouseY = 0

    #main game loop
    while True:
        mouseClick = False

        boxX, boxY = getBox(mouseX, mouseY)

        for event in pygame.event.get():    
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

def getBox(x, y):
    for boxX in range(WIDTH):
        for boxY in range(HEIGHT):
            left = boxX * (BOXSIZE + GAPSIZE) + XMARGIN
            top = boxY * (BOXSIZE + GAPSIZE) + YMARGIN
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxX, boxY)
    return (None, None)

if __name__ == "__main__":
    main()