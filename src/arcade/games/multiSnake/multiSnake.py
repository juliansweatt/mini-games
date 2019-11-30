import pygame

from arcade import plethoraAPI
from enum import IntFlag, auto, unique
import time

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
            self.startX = x
            self.name = name
            self.startY = y
            self.alive = True
            self.wins = 0
            self.x_change = 0
            self.y_change = 1
            self.growX = False
            self.growY = False           
        def kill(self):
            self.alive = False
            self.coords = []
            self.gridCoords = []
        def newRound(self):
            self.coords = [(self.startX,self.startY)]
            self.gridCoords = [(self.startX/10, self.startY/10)]
            self.x_change = 0
            self.y_change = 1
            self.alive = True
    def __init__(self):
        super().__init__(size=(800, 600), fps=20)
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.arrows = 0b0000  # bitmask for arrow keys
        self.arrows_hidden = 0b0000  # bitmask for hiding opposite keys on key down while that key is down
        self.selected = 0
        self.playerSelectBox = [(50,370,200,75), (300,370,200,75), (550,370,200,75)]
        self.clock = pygame.time.Clock()
        self.spaceTaken = set()
        self.blockSize = 10
        self.playersLeft = 0
        self.render = False
        self.startMenu = True
        self.roundCount = 0
        self.reset = False
        self.biggerFont = pygame.font.SysFont('Arial', 30)
        self.smallFont = pygame.font.SysFont('Arial', 20)
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            buttons = joystick.get_numbuttons()
            for i in range(buttons):
                button = joystick.get_button(i)
        self.players = [self.snake(self.rect.width * 0.2, self.rect.height * 0.2, 10)]
        self.players[0].y_change = 0
        self.playerCount = 2
        
        self.x = (self.rect.width * 0.2)/10
        self.y = (self.rect.height * 0.2)/10


        
    def initializePlayers(self, playerCount):
        self.playerCount = playerCount
        self.playersLeft = playerCount
        self.players = []
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
        if ((x,y) in self.spaceTaken):
            return True
        return False
    
    def onevent(self, event: pygame.event):
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
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
            self.render = True
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
            self.render = True
        
        if (self.render):
            return True
        else:
            return False
        
        


    def onrender(self):
        self.render = False
        if (self.startMenu):
            self.selected += self.players[0].x_change
            self.selected = 0 if self.selected > 2 else self.selected
            self.selected = 2 if self.selected < 0 else self.selected
            for i in range(len(self.playerSelectBox)):
                pygame.draw.rect(self.display, (205, 205, 210) if self.selected == i else (50, 50, 50), self.playerSelectBox[i])
                self.display.blit(self.biggerFont.render((str(i+2)+' Players'), True, (50,205,50)), (self.playerSelectBox[i][0]+39, self.playerSelectBox[i][1]+19))
            if (self.players[0].y_change != 0):
                self.initializePlayers(self.selected+2)
                self.startMenu = False
                self.display.fill((0,0,0))
                return True
            return False
        if (self.reset):
            self.reset = False
            self.roundCount += 1
            time.sleep(3)
            self.playersLeft = self.playerCount
            self.spaceTaken = set()
            for player in self.players:
                player.newRound()
                self.spaceTaken.add(player.gridCoords[-1])

            self.display.fill((0,0,0))
            if (self.roundCount == 5):
                self.onexit()

        for player in self.players:
            if (player.alive):
                self.x = int(player.gridCoords[-1][0] + player.x_change)
                self.y = int(player.gridCoords[-1][1] + player.y_change)
                if(self.checkForCollision(self.x, self.y)):
                    for x, y in player.gridCoords:
                        self.spaceTaken.remove((x,y))
                    player.kill()
                    self.playersLeft -= 1
                    print("COLLISION: ", self.x, self.y)
                    self.display.fill((0,0,0))
            if (player.x_change != 0 and player.alive):
                player.gridCoords.append((player.gridCoords[-1][0]+player.x_change, player.gridCoords[-1][1]))
                player.coords.append((player.coords[-1][0]+player.x_change*self.blockSize, player.coords[-1][1]))
                self.spaceTaken.add(player.gridCoords[-1])
                for x, y in player.coords:
                    self.display.blit(player.snakeBlock, (x,y))
            if (player.y_change != 0 and player.alive):
                player.gridCoords.append((player.gridCoords[-1][0], player.gridCoords[-1][1]+player.y_change))
                player.coords.append((player.coords[-1][0], player.coords[-1][1]+player.y_change*self.blockSize))
                self.spaceTaken.add(player.gridCoords[-1])
            for x, y in player.coords:
                self.display.blit(player.snakeBlock, (x,y))
        if (self.playersLeft == 1):
            displayName = filter(lambda x: x.alive, self.players)
            displayName = list(displayName)[0]
            winner = self.players.index(displayName)
            self.players[winner].wins += 1
            pygame.draw.rect(self.display, (15, 15, 15),(self.rect.width/2 - 150,40,300,500))
            self.display.blit(self.biggerFont.render((displayName.name+' Won'), True, displayName.color), (self.rect.width/2 - 85, 100))
            for i, player in enumerate(self.players):
                self.display.blit(self.biggerFont.render((player.name+'    '+str(player.wins)), True, player.color), (self.rect.width/2 - 75, 200+(i*100)))

            self.reset = True

        return True

 