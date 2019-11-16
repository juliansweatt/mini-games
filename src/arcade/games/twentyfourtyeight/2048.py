import pygame
import random
from copy import deepcopy
from enum import Enum

#TODO: needs to be integrated with API and finished

#enumeration for directions
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 3
    RIGHT = 4

#enumeration for all possible positions
class Pos(Enum):
    NIL = [0,0]
    A = [10, 10]
    B = [120, 10]
    C = [230, 10]
    D = [340, 10]
    E = [10, 120]
    F = [120, 120]
    G = [230, 120]
    H = [340, 120]
    I = [10, 230]
    J = [120, 230]
    K = [230, 230]
    L = [340, 230]
    M = [10, 340]
    N = [120, 340]
    O = [230, 340]
    P = [340, 340]

    def val(self):
        return self.value

#tile class
class Tile():
    def __init__(self, coord=Pos.NIL):
        self.num = 0
        self.color = pygame.Color(255, 255, 255)
        self.text = str(2 ^ self.num)
        self.font = pygame.font.SysFont('Arial', 40)
        self.surface = pygame.Surface((100, 100))
        self.enum = coord
        self.pos = coord.val()

    #updates the number and color
    def update(self):
        self.num += 1
        self.color.r -= 23
        self.color.g -= 23
        self.color.b -= 23
        self.text = str(2 ^ self.num)

#game class
class Game():
    def __init__(self, display):
        self.display = display
        self.cont = True
        self.bg = (255, 0, 255)
        self.tiles = [[Tile(Pos.A), Tile(Pos.B), Tile(Pos.C), Tile(Pos.D)],
                      [Tile(Pos.E), Tile(Pos.F), Tile(Pos.G), Tile(Pos.H)],
                      [Tile(Pos.I), Tile(Pos.J), Tile(Pos.K), Tile(Pos.L)],
                      [Tile(Pos.M), Tile(Pos.N), Tile(Pos.O), Tile(Pos.P)]]

    #returns a random position from the available positions
    def find_spot(self):
        available = []
        for i in range(4):
            for j in range(4):
                if self.tiles[i][j].num == 0:
                    available.append(self.tiles[i][j])
        return random.choice(available)

    #updates the tile in the corresponding position from find_spot
    def spawn_new(self):
        spot = self.find_spot()
        for i in range(4):
            for j in range(4):
                if self.tiles[i][j] == spot:
                    self.tiles[i][j].update()   

    #algorithm that shifts all tiles until they can't move anymore
    def move(self, direction):
        if direction == Direction.UP:
            for i in range(1, 4):
                for j in range(0, 4):
                    if self.tiles[i][j].num != 0 and self.tiles[i-1][j].num == 0:
                        temp = self.tiles[i][j]
                        self.tiles[i][j] = self.tiles[i-1][j]
                        self.tiles[i-1][j] = temp                    
        elif direction == Direction.DOWN:
            pass
        elif direction == Direction.LEFT:
            pass
        elif direction == Direction.RIGHT:
            pass

    #blits surfaces 
    def ondraw(self):
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].surface.fill(self.tiles[i][j].color)
                self.display.blit(self.tiles[i][j].surface, self.tiles[i][j].pos)

    #event loop
    def onevent(self, e):
        if e.type == pygame.QUIT:
            self.cont = False
            return
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_DOWN:
                self.move(Direction.DOWN)
            elif e.key == pygame.K_UP:
                self.move(Direction.UP)
            elif e.key == pygame.K_LEFT:
                self.move(Direction.LEFT)
            elif e.key == pygame.K_RIGHT:
                self.move(Direction.RIGHT)
            elif e.key == pygame.K_DOWN:
                self.move(Direction.DOWN)

    #mainloop, needs to be removed in favor of API's onrender 
    def mainloop(self):
        self.display.fill(self.bg)
        while self.cont:
            for e in pygame.event.get():
                self.onevent(e)
            self.ondraw()
            #self.spawn_new()
            pygame.display.flip()

#main driver program
if __name__=="__main__":
    pygame.init()
    pygame.font.init()
    display = pygame.display.set_mode((450, 450))
    game = Game(display)
    game.mainloop()
    pygame.quit

            

