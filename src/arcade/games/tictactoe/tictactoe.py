import pygame as pg
import math
from arcade import plethoraAPI

class Board(plethoraAPI.Game):
    def __init__(self):
        super().__init__(size=(800,800), fps=20)
        self.moveCount=0;
        self.box=-1
        self.turn = 'X'
        self.moves=['-'] *9              #array to track spaces
        self.win='-'
        self.inendgame = False

        self.clock=pg.time.Clock()
        self.dim=800                    #size of screen
        self.sqDim= 200
        self.square=(self.sqDim,self.sqDim)
    #    self.size= (self.dim, self.dim) #dimension for entire screen
        self.pad=100                    #all sides have 100 buffer
        self.center=(self.dim//2, self.pad//2)

        self.white= (255,255,255)
        self.black= (0,0,0)
        self.blue= (0,0,128)
        self.red=(255,0,0)
        self.gray=(80,80,80)

        self.font = pg.font.Font('freesansbold.ttf', 16)
        self.message="Welcome to Tic-Tac-Toe, X goes first. Select a space"
        self.text = self.font.render(self.message, True, self.black, self.white)
        # pg.display.set_caption("Tic-Tac-Toe")
        self.rects = [
        pg.Rect((self.pad,self.pad),(self.square)),                  #1 2 3
        pg.Rect((self.pad+self.sqDim,self.pad),(self.square)),
        pg.Rect((self.pad+self.sqDim*2,self.pad),(self.square)),

        pg.Rect((self.pad,self.pad+self.sqDim),(self.square)),      #4 5 6
        pg.Rect((self.pad+self.sqDim,self.pad+self.sqDim),(self.square)),
        pg.Rect((self.pad+self.sqDim*2,self.pad+self.sqDim),(self.square)),

        pg.Rect((self.pad,self.pad+self.sqDim*2),(self.square)),       #7 8 9
        pg.Rect((self.pad+self.sqDim,self.pad+self.sqDim*2),(self.square)),
        pg.Rect((self.pad+self.sqDim*2,self.pad+self.sqDim*2),(self.square))
        ]

    def onrender(self):
        if self.inendgame:
            return False
        if self.box != -1:
            self.drawTurn(self.moveCount)
            self.box=-1
        self.CheckWin()             #after every move check for a win
        if self.win=='X' or self.win=='O':
            self.message=self.win+" IS THE WINNER!"
            self.endGame()
            return True

        elif self.moveCount==9:
            self.message="It's a tie!"
            self.endGame()
            return True

        p1=self.pad + self.sqDim
        p2=self.pad
        self.display.fill(self.white)

        pg.draw.line(self.display,self.black,(p1, p2), (p1, self.dim - p2),10) #left vertical line
        pg.draw.line(self.display,self.black,(p1+self.sqDim,p2),(p1+self.sqDim,self.dim-p2),10) #right vertical
        pg.draw.line(self.display,self.black,(p2, p1), (self.dim-p2,p1),10)  #upper horizontal
        pg.draw.line(self.display,self.black,(p2, p1+self.sqDim), (self.dim-p2,p1+self.sqDim),10)  #lower horizontal

        self.text = self.font.render(self.message, True, self.black, self.white)
        self.textRect= self.text.get_rect() #different message=different rect
        self.textRect.center = (self.center) #different center
        self.display.blit(self.text,self.textRect)   #draw
        for x in range(len(self.moves)):
            if self.moves[x]=='X':
                X=pg.Surface((self.sqDim-10,self.sqDim-10)) #do this so surface is not over boundary line
                X.fill(self.white)
                pg.draw.line(X,self.red, (0,0),(self.sqDim-10,self.sqDim-10),20)
                pg.draw.line(X,self.red, (0,self.sqDim-10),(self.sqDim-10,0),20)
                self.rects[x]=self.rects[x].move(5,5)
                self.display.blit(X,self.rects[x])
                self.rects[x]=self.rects[x].move(-5,-5)
            elif self.moves[x]=="O":
                pg.draw.arc(self.display, self.blue, self.rects[x],0,2*math.pi,20)
        return False

    def CheckWin(self):
        #Chech rows for win
        if self.moves[0] == self.moves[1] and self.moves[1]==self.moves[2]:
            if self.moves[0] =='X':
                self.win='X'
            elif self.moves[0]=='O':
                self.win='O'
        if self.moves[3] == self.moves[4] and self.moves[4]==self.moves[5]:
            if self.moves[3] =='X':
                self.win='X'
            elif self.moves[3]=='O':
                self.win='O'
        if self.moves[6] == self.moves[7] and self.moves[7]==self.moves[8]:
            if self.moves[6] =='X':
                self.win='X'
            elif self.moves[6]=='O':
                self.win='O'
        #check columns for win
        if self.moves[0] == self.moves[3] and self.moves[3]==self.moves[6]:
            if self.moves[0] =='X':
                self.win='X'
            elif self.moves[0]=='O':
                self.win='O'
        if self.moves[1] == self.moves[4] and self.moves[4]==self.moves[7]:
            if self.moves[1] =='X':
                self.win='X'
            elif self.moves[1]=='O':
                self.win='O'
        if self.moves[2] == self.moves[5] and self.moves[5]==self.moves[8]:
            if self.moves[2] =='X':
                self.win='X'
            elif self.moves[2]=='O':
                self.win='O'
        #check Diagonals for win
        if self.moves[0] == self.moves[4] and self.moves[4]==self.moves[8]:
            if self.moves[0] =='X':
                self.win='X'
            elif self.moves[0]=='O':
                self.win='O'
        if self.moves[6] == self.moves[4] and self.moves[4]==self.moves[2]:
            if self.moves[6] =='X':
                self.win='X'
            elif self.moves[6]=='O':
                self.win='O'

    def endGame(self):
        if self.win == 'X':
            self.message="X is the winner! Play Again?"
        elif self.win == 'O':
            self.message="O is the winner! Play Again?"
        elif self.win == '-':
            self.message="It's a tie! Play Again?"

        self.inendgame = True

        # endWindow=pg.display.set_mode((400,200))
        #pg.display.set_caption("End Game")
        self.display.fill(self.gray)

        self.text = self.font.render(self.message, True, self.black, self.gray)
        self.textRect= self.text.get_rect() #different message=different rect
        self.textRect.center = (400//2,20) #different center
        self.display.blit(self.text,self.textRect)   #draw
        buttonSize=(150,50)
        fontYes=self.font.render("Yes",True,self.black)
        fontNo=self.font.render("No",True,self.black)

        backYes=pg.Surface(buttonSize)
        backYes.fill(self.white)
        backNo=pg.Surface(buttonSize)
        backNo.fill(self.red)
        backNo.blit(fontNo,((backNo.get_width()-fontNo.get_width())//2,
            (backNo.get_height()-fontNo.get_height())//2))
        backYes.blit(fontYes,((backYes.get_width()-fontYes.get_width())//2,
            (backYes.get_height()-fontYes.get_height())//2))
        self.yes= pg.Rect((50,100),buttonSize)
        self.no= pg.Rect((200,100),buttonSize)
        self.display.blit(backYes,self.yes)
        self.display.blit(backNo,self.no)

    def onevent(self,event):
        dirty = False
        if event.type==pg.QUIT:
            self.onexit()
            return False
        if self.inendgame:
            # select=False
            # option=""
            option=self.endEvent(event)
            if option=="yes":
                for x in range(len(self.moves)):
                    self.moves[x]="-"
                self.win='-'
                self.box=-1
                self.turn='X'
                self.moveCount=0
                self.inendgame = False
                dirty = True
            if option=="no":
                self.onexit()
                return False
        else:
            if event.type==pg.MOUSEBUTTONDOWN:
                for x in range (0,9):
                    if self.rects[x].collidepoint(event.pos):
                        dirty=True
                        self.box=int(x)
        return dirty

    def endEvent(self,event):    #called by endGame
        if event.type==pg.MOUSEBUTTONDOWN:
            if self.yes.collidepoint(event.pos):
                return "yes"
            if self.no.collidepoint(event.pos):
                return "no"

    def drawTurn(self,moveCount):
        if self.turn == 'X':
            if self.moves[self.box]!='-':
                self.message="Invalid move! Select a different space"
            else:
                self.moves[self.box]='X'
                self.message="O's turn. Select a space"
                self.turn='O'
                self.moveCount+=1

        elif self.turn == 'O':
            if self.moves[self.box]!='-':
                self.message="Invalid move! Select a different space"
            else:
                self.moves[self.box]='O'
                self.message="X's turn. Select a space"
                self.turn='X'
                self.moveCount+=1
