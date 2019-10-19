from pygame.locals import *
from random import randint
import pygame
import time
class multiSnake:
    class snake:
        def __init__(self, x, y, gameDisplay, blockSize):
            self.coords=[(x,y)]
            self.gridCoords = [(x/10, y/10)]
            self.blockSize = blockSize
            self.snakeBlock = pygame.image.load('snake.png')
            self.alive = True
        def growX(self, xChange, gameDisplay):
        def growY(self, yChange, gameDisplay):
    def __init__(self):
        pygame.init()
        print("start")
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.displayWidth = 1200
        self.displayHeight = 900
        self.gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        pygame.display.set_caption('MultiSnake')
        self.clock = pygame.time.Clock()
        self.spaceTaken = {}
    def game_loop(self):
        

        x_change = 0
        y_change = 1

        gameExit = False


        while not gameExit:
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -1
                        y_change = 0
                    if event.key == pygame.K_RIGHT:
                        x_change = 1
                        y_change = 0
                    if event.key == pygame.K_DOWN:
                        x_change = 0
                        y_change = 1
                    if event.key == pygame.K_UP:
                        x_change = 0
                        y_change = -1
if __name__ == "__main__" :
    print("FIRST")
    game = multiSnake()
