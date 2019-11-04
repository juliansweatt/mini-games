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
            self.x_change = 0
            self.y_change = 1
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
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.displayWidth = 1200
        self.displayHeight = 900
        self.gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        pygame.display.set_caption('MultiSnake')
        self.clock = pygame.time.Clock()
        self.spaceTaken = {}
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            buttons = joystick.get_numbuttons()
            for i in range(buttons):
                button = joystick.get_button(i)


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
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            playerEvent = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    player = self.players[0]
                    if event.key == pygame.K_LEFT:
                        player.x_change = -1
                        player.y_change = 0
                    if event.key == pygame.K_RIGHT:
                        player.x_change = 1
                        player.y_change = 0
                        name = pygame.joystick.Joystick(0).get_name()
                    if event.key == pygame.K_DOWN:
                        player.x_change = 0
                        player.y_change = 1
                    if event.key == pygame.K_UP:
                        player.x_change = 0
                        player.y_change = -1
                elif event.type == pygame.JOYBUTTONDOWN:
                    player = self.players[1]
                    if event.button == 2:
                        player.x_change = -1
                        player.y_change = 0
                    if event.button == 1:
                        player.x_change = 1
                        player.y_change = 0
                        name = pygame.joystick.Joystick(0).get_name()
                    if event.button == 0:
                        player.x_change = 0
                        player.y_change = 1
                    if event.button == 3:
                        player.x_change = 0
                        player.y_change = -1
            for player in self.players:
                self.x = int(player.gridCoords[-1][0] + player.x_change)
                self.y = int(player.gridCoords[-1][1] + player.y_change)
                if(self.checkForCollision(self.x, self.y)):
                    for x, y in player.gridCoords:
                        del self.spaceTaken[x][y]
                    player.kill()
                    print("COLLISION: ", self.x, self.y)
                player.growX(player.x_change, self.gameDisplay)
                player.growY(player.y_change, self.gameDisplay)
                try:
                    self.spaceTaken[self.x][self.y] = 1
                except KeyError:
                    print("Dead")
                    for x in self.spaceTaken:
                        for y in self.spaceTaken[x]:
                            print(x, y)
                    quit()
            
            
            pygame.display.update()
            self.clock.tick(20)



    
 
if __name__ == "__main__" :
    game = multiSnake()
