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
            if (xChange != 0 and self.alive):
                self.gridCoords.append((self.gridCoords[-1][0]+xChange, self.gridCoords[-1][1]))
                self.coords.append((self.coords[-1][0]+xChange*self.blockSize, self.coords[-1][1]))
                for x, y in self.coords:
                    gameDisplay.blit(self.snakeBlock, (x,y))
        def growY(self, yChange, gameDisplay):
            if (yChange != 0) and self.alive:
                self.gridCoords.append((self.gridCoords[-1][0], self.gridCoords[-1][1]+yChange))
                self.coords.append((self.coords[-1][0], self.coords[-1][1]+yChange*self.blockSize))
                for x, y in self.coords:
                    gameDisplay.blit(self.snakeBlock, (x,y))
        def kill(self):
            self.alive = False
            self.coords = []
            self.gridCoords = []
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
        for i in range(int(self.displayWidth/10)):
            self.spaceTaken[i] = {}
        self.players = []
        self.playerCount = 2
        
        self.x = (self.displayWidth * 0.2)/10
        self.y = (self.displayHeight * 0.2)/10
        for i in range(self.playerCount):
            if (i == 0):
                self.players.append(self.snake(self.displayWidth * 0.2, self.displayHeight * 0.2, self.gameDisplay, 10))
            elif (i == 1):
                self.players.append(self.snake(self.displayWidth * 0.8, self.displayHeight * 0.2, self.gameDisplay, 10))
            elif (i == 2):
                self.players.append(self.snake(self.displayWidth * 0.2, self.displayHeight * 0.8, self.gameDisplay, 10))
            elif (i == 3):
                self.players.append(self.snake(self.displayWidth * 0.8, self.displayHeight * 0.8, self.gameDisplay, 10))
        

        self.game_loop()
        pygame.quit()
        quit()

    
    def checkForCollision(self, x, y):
        if (x in self.spaceTaken.keys()):
            if (y in self.spaceTaken[x].keys()):
                return True
        return False
        



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
