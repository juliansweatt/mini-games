import pygame

from arcade import plethoraAPI
from enum import IntFlag, auto, unique

from pygame.locals import (
    QUIT,
    K_SPACE,
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_q,
    KEYDOWN, KEYUP,
    MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN,
)

from typing import Tuple

@unique
class ArrowMask(IntFlag):
    """ Enum used to mask arrow keys (up, right, down, left) """
    up = auto()
    right = auto()
    down = auto()
    left = auto()


class Game(plethoraAPI.Game):
    class snake:
        def __init__(self, x, y, blockSize):
            self.coords=[(x,y)]
            self.gridCoords = [(x/10, y/10)]
            self.snakeBlock = pygame.image.load('snake.png')
            self.alive = True
            self.x_change = 0
            self.y_change = 1
            self.growX = False
            self.growY = False           
        def kill(self):
            self.alive = False
            self.coords = []
            self.gridCoords = []
    def __init__(self):
        super().__init__(size=(800, 600), fps=20)
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.arrows = 0b0000  # bitmask for arrow keys
        self.arrows_hidden = 0b0000  # bitmask for hiding opposite keys on key down while that key is down
        self.clock = pygame.time.Clock()
        self.spaceTaken = set()
        self.blockSize = 10
        self.render = False
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            buttons = joystick.get_numbuttons()
            for i in range(buttons):
                button = joystick.get_button(i)


        for i in range(int(self.rect.width/10)):
            self.spaceTaken[i] = {}
        self.players = []
        self.playerCount = 2
        
        self.x = (self.rect.width * 0.2)/10
        self.y = (self.rect.height * 0.2)/10
        for i in range(self.playerCount):
            if (i == 0):
                self.players.append(self.snake(self.rect.width * 0.2, self.rect.height * 0.2, 10))
            elif (i == 1):
                self.players.append(self.snake(self.rect.width * 0.8, self.rect.height * 0.2, 10))
            elif (i == 2):
                self.players.append(self.snake(self.rect.width * 0.2, self.rect.height * 0.8, 10))
            elif (i == 3):
                self.players.append(self.snake(self.rect.width * 0.8, self.rect.height * 0.8, 10))
            self.spaceTaken.add(self.players[-1].gridCoords[-1])
        


    
    def checkForCollision(self, x, y):
        if (x in self.spaceTaken.keys()):
            if (y in self.spaceTaken[x].keys()):
                return True
        return False
    def onevent(self, event):
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
                player.growX = True
                player.growY = True(player.y_change, self.display)
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


    def onrender(self):

        if(player.growX):
            if (xChange != 0 and self.alive):
                self.gridCoords.append((self.gridCoords[-1][0]+xChange, self.gridCoords[-1][1]))
                self.coords.append((self.coords[-1][0]+xChange*self.blockSize, self.coords[-1][1]))
                for x, y in self.coords:
                    gameDisplay.blit(self.snakeBlock, (x,y))
        if(player.growY):
            if (yChange != 0) and self.alive:
                self.gridCoords.append((self.gridCoords[-1][0], self.gridCoords[-1][1]+yChange))
                self.coords.append((self.coords[-1][0], self.coords[-1][1]+yChange*self.blockSize))
                for x, y in self.coords:
                    gameDisplay.blit(self.snakeBlock, (x,y))

    
 
if __name__ == "__main__" :
    game = multiSnake()
