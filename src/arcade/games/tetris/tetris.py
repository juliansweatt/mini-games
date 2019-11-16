import pygame
import random
import copy
from arcade import plethoraAPI

#class for color, a color is chosen at random for each object
class Color():
    def __init__(self):
        num = random.randint(1, 7)
        self.color_name = "Black"
        self.dec = (0, 0, 0)
        if (num == 1):
            self.color_name = "RED"
            self.dec = (255, 0, 0)
        elif (num == 2):
            self.color_name = "BLUE"
            self.dec = (0, 0, 255)
        elif (num == 3):
            self.color_name = "YELLOW"
            self.dec = (255, 255, 0)
        elif (num == 4):
            self.color_name = "GREEN"
            self.dec = (0, 255, 0)
        elif (num == 5):
            self.color_name = "ORANGE"
            self.dec = (255, 165, 0)
        elif (num == 6):
            self.color_name = "PURPLE"
            self.dec = (255, 0, 255)
        elif (num == 7):
            self.color_name = "WHITE"
            self.dec = (255, 255, 255)

#class for the tetris pieces
class Piece():
    def __init__(self):
        self.color = Color()
        self.shape = [[False for i in range(4)] for j in range(4)]
        #the shape is determined by the color, positions equal to true get color
        if (self.color.color_name == "RED"):
            self.shape = [[False, False, False, False], 
                          [False, False, False, False], 
                          [False, True, False, False], 
                          [True, True, True, False]]
        elif (self.color.color_name == "BLUE"):
            self.shape = [[False, False, False, False], 
                          [False, False, True, False], 
                          [False, False, True, False], 
                          [False, True, True, False]]
        elif (self.color.color_name == "YELLOW"):
            self.shape = [[False, False, False,False],
                          [False, True, False, False], 
                          [False, True, False, False], 
                          [False, True, True, False]]
        elif (self.color.color_name == "GREEN"): 
            self.shape = [[False, False, False, False], 
                          [False, False, False, False], 
                          [True, True, False, False], 
                          [True, True, False, False]]
        elif (self.color.color_name == "ORANGE"):
            self.shape = [[False, False, False, False], 
                          [False, False, True, False], 
                          [False, True, True, False], 
                          [False, True, False, False]]
        elif (self.color.color_name == "PURPLE"):
            self.shape = [[False, False, False, False], 
                          [True, False, False, False], 
                          [True, True, False, False], 
                          [False, True, False, False]]
        elif (self.color.color_name == "WHITE"):
            self.shape = [[False, True, False, False], 
                          [False, True, False, False],
                          [False, True, False, False],
                          [False, True, False, False]]
        #starting position is defined
        self.cpos = [[[250, 0], [275, 0], [300, 0], [325, 0]],
                     [[250,25], [275,25], [300,25], [325,25]],
                     [[250,50], [275,50], [300,50], [325,50]],
                     [[250,75], [275,75], [300,75], [325,75]]]
        self.start_pos = copy.deepcopy(self.cpos)
        #create a list of surfaces and color them accordingly
        self.piece_surface = [[pygame.Surface((25, 25)) for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                if (self.shape[i][j] == True):
                    self.piece_surface[i][j].fill(self.color.dec)
                elif (self.shape[i][j] == False):
                    self.piece_surface[i][j].fill((0, 0, 0))
    
    #get the lowest tile with the value true
    def get_lowest(self):
        lowest = 0
        for i in range(4):
            for j in range(4):
                if (self.shape[i][j] == True):
                    if (self.cpos[i][j][1] > lowest):
                        lowest = self.cpos[i][j][1]
        return int(lowest)

    #updates the position's y coordinate
    def update(self):
        for i in range(4):
            for j in range(4):
                self.cpos[i][j][1] += 25

    #move down by 100 pixels, needs to handle more edge case
    def jump(self):
        for i in range(4):
            for j in range(4):
                if self.get_lowest() <= 625:
                   self.cpos[i][j][1] += 100

#game class that inherits from the API
class Tetris(plethoraAPI.Game):
    def __init__(self):
        super().__init__(size = (550, 750), fps = 40)
        self.square_w = 22
        self.square_h = 30
        self.screen = [] #list of used pieces
        self.gravity = 1 / 40
        self.state = 0
        self.bg = (0, 0, 0)
        self.next_piece = Piece()
        self.current_piece = Piece()
        self.npos = [[[ 0, 0], [ 0,25], [ 0,50], [ 0,75]],
                     [[25, 0], [25,25], [25,50], [25,75]],
                     [[50, 0], [50,25], [50,50], [50,75]],
                     [[75, 0], [75,25], [75,50], [75,75]]]
    
    #returns the highest piece saved to the screen
    def get_highest(self):
        temp = 1000
        if self.screen != []:
            for i in range(len(self.screen)):
                if self.screen[i][1][1] < temp:
                    temp = self.screen[i][1][1]
        return int(temp)

    #checks if motion to the left is possible
    def check_left(self):
        for i in range(len(self.screen)):
            x = self.screen[i][1][0] - 25
            y = self.screen[i][1][1] 
            for j in range(4):
                for k in range(4):
                    if self.current_piece.shape[j][k] == True:
                        if [x, y] == self.current_piece.cpos[j][k]:
                            return True
        return False

    #moves piece to left after checking if possible
    def move_left(self):
        if self.check_left() == True:
            return
        for i in range(4):
            for j in range(4):
                c = self.current_piece.cpos[i][j]
                if (c[0] > 0):
                    self.current_piece.cpos[i][j][0] -= 25
                else:
                    return

    #checks if motion to the right is possible
    def check_right(self):
        for i in range(len(self.screen)):
            x = self.screen[i][1][0] + 25
            y = self.screen[i][1][1] 
            for j in range(4):
                for k in range(4):
                    if self.current_piece.shape[j][k] == True:
                        if [x, y] == self.current_piece.cpos[j][k]:
                            return True
        return False

    #moves to the right
    def move_right(self):
        if self.check_right() == True:
            return
        for i in range(4):
            for j in range(4):
                c = self.current_piece.cpos[i][j]
                if (c[0] < 550):
                    self.current_piece.cpos[i][j][0] += 25
                else:
                    return
    
    #rotates a piece by taking transpose and exchnaging rows for columns
    def rotate(self):
        for i in range(4): 
            j = 0
            k = 3
            while j < k: 
                t = self.current_piece.cpos[j][i] 
                self.current_piece.cpos[j][i] = self.current_piece.cpos[k][i] 
                self.current_piece.cpos[k][i] = t 
                j += 1
                k -= 1
        for i in range(4): 
            for j in range(i, 4): 
                t = self.current_piece.cpos[i][j]
                self.current_piece.cpos[i][j] = self.current_piece.cpos[j][i] 
                self.current_piece.cpos[j][i] = t 

    #check if a piece can be updated
    def check_below(self):
        if self.current_piece.get_lowest() == 725:
            return True
        for i in range(len(self.screen)):
            x = self.screen[i][1][0]
            y = self.screen[i][1][1] - 25
            for j in range(4):
                for k in range(4):
                    if self.current_piece.shape[j][k] == True:
                        if [x, y] == self.current_piece.cpos[j][k]:
                            return True
        return False
    
    #check when the pieces get to the top
    def check_if_lose(self):
        if self.screen == []:
            return
        for i in range(len(self.screen)):
            for j in range(4):
                for k in range(4):
                    if self.current_piece.shape[j][k] == True:
                        if self.screen[i][1] == self.current_piece.start_pos[j][k]:
                            return True
        return False

    #event loop
    def onevent(self, e):
        if e.type == pygame.QUIT:
            return False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_DOWN:
                #if (self.get_highest() - self.current_piece.get_lowest()) >= 100:
                #    self.current_piece.jump()
                pass
            elif e.key == pygame.K_UP:
                self.rotate()
            elif e.key == pygame.K_LEFT:
                self.move_left()
            elif e.key == pygame.K_RIGHT:
                self.move_right()
            elif e.key == pygame.K_n:
                self.screen.clear()
        elif e.type == pygame .KEYUP:
            if e.key == pygame.K_DOWN:
                pass
            elif e.key == pygame.K_UP:
                pass
            elif e.key == pygame.K_LEFT:
                pass
            elif e.key == pygame.K_RIGHT:
                pass
            elif e.key == pygame.K_n:
                pass
        return False

    #blits every piece to the display
    def ondraw(self):
        self.display.fill(self.bg)
        self.display.blit(self.display, (550, 750))
        for i in range(len(self.screen)):
            self.display.blit(self.screen[i][0], self.screen[i][1])
        for i in range(4):
            for j in range(4):
                if (self.current_piece.shape[i][j] == True):
                    cx = self.current_piece.cpos[i][j][0]
                    cy = self.current_piece.cpos[i][j][1]
                    self.display.blit(self.current_piece.piece_surface[i][j], [cx, cy])
        for i in range(4):
            for j in range(4):
                nx = self.npos[i][j][0]
                ny = self.npos[i][j][1]
                self.display.blit(self.next_piece.piece_surface[i][j], [nx, ny])

    #saves a piece 
    def save_piece(self):
        for i in range(4):
            for j in range(4):
                if (self.current_piece.shape[i][j] == True):
                    x = self.current_piece.cpos[i][j]
                    col = self.current_piece.color.dec
                    surf = pygame.Surface((25, 25))
                    surf.fill(col)
                    z = (surf,  x)
                    self.screen.append(z)

    #interface function for the API's event loop
    def onrender(self):
        self.ondraw()
        if int(self.gravity * self.state) == 1:
            self.state = 0
            self.current_piece.update()
            if self.check_below() == True:
                self.save_piece()
                self.current_piece = self.next_piece
                self.current_piece.cpos = self.current_piece.start_pos
                self.next_piece = Piece()
            if self.check_if_lose() == True:
                return False
            #self.check_if_win()
        self.state += 1
        return True

