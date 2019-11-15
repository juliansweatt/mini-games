import pygame as pg
from arcade import plethoraAPI

class Piece():
    def __init__(self):
        self.color="black" #or red
        self.king=False

    def setColor(self,col):
        if col=="red":
            self.color="red"
        elif col=="black":
            self.color="black"

    def makeKing(self):
        self.king=True

class Checkers():
    def __init__(self):
        self.surfaceDim=420
        self.sqDim=60
        self.Board=pg.display.set_mode(self.surfaceDim,self.surfaceDim)
        self.selected=-1    #selected square

        self.white= (255,255,255)
        self.black= (0,0,0)
        self.red=(255,0,0)

        self.Board.fill(self.white)

        self.spaces[16] #background array of valid spaces for pieces to move
        self.moves=0
        self.turn='R' #or 'B'

    def onevent(self,event):
        dirty = False
        if event.type==pg.QUIT:
            self.onexit()
            return False
        else
            if event.type==pg.MOUSEBUTTONDOWN:
                for x in range(0,16):
                    if self.rects[x].collidepoint(event.pos):
                            if self.spaces[x]==self.turn:   #correct piece selected
                                self.selected=x
                            else:
                                break


    #def move(self):    #only allows diagnol moves and checks if piece is kinged to go backwards

    #def jumpPiece(self): #checks a valid jump and forces mulitple jumps if possible

    #def checkWin(self): #checks if either side has lost all pieces (moves>=80 means tie)
