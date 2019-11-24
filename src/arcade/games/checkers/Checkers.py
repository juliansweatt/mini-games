import pygame as pg
from arcade import plethoraAPI


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

        self.spaces['B','B','B','B',
                    'B','B','B','B',
                    'B','B','B','B',
                    '-','-','-','-',
                    '-','-','-','-',
                    'R','R','R','R',
                    'R','R','R','R',
                    'R','R','R','R'] #background array of valid spaces for pieces to move
                    #kings represented by KR and KB
        self.moves=0
        self.turn="R" #or 'B'
        self.win='tie'
        self.countR=12
        self.countB=12

    def onevent(self,event):
        dirty = False
        if event.type==pg.QUIT:
            self.onexit()
            return False
        else
            if event.type==pg.MOUSEBUTTONDOWN:
                if self.selected==-1:
                    for x in range(0,32):
                        if self.rects[x].collidepoint(event.pos):
                                if self.spaces[x]==self.turn:   #correct piece selected
                                    self.selected=x
                                elif self.spaces[x]=="KR" and self.turn=='R':
                                    self.selected=x
                                elif self.spaces[x]=="KB" and self.turn=='B':
                                    self.selected=x
                                else:
                                    break
                if self.selected>=0:
                    for x in range(0,32):
                        if self.rects[x].collidepoint(event.pos)
                            if validMove(x):
                                break

    def validMove(self,x):
        if self.turn=="B":
            if self.selected==3 or self.selected==11 or self.selected==19 or self.selected==27:
                if self.selected==x-4:
                    return True
            elif self.selected==4 or self.selected==12 or self.selected==20:
                if self.selected==x-4:
                    return True
            else:
                if self.selected+4==x or self.selected+5==x:
                    return True
                    
        elif self.turn=="R":
            if self.selected==11 or self.selected==19 or self.selected==27:
                if self.selected==x+4:
                    return True
            elif self.selected==4 or self.selected==12 or self.selected==20 or self.selected==28:
                if self.selected==x+4:
                    return True
            else:
                if self.selected-4==x or self.selected-5==x:
                    return True

        return False

    #def move(self):    #only allows diagnol moves and checks if piece is kinged to go backwards

    #def jumpPiece(self): #checks a valid jump and forces mulitple jumps if possible

    def checkWin(self): #checks if either side has lost all pieces (moves>=80 means tie)
        if moves==80:
            self.win="Tie"
        elif countB==0:
            self.win="Red"
        elif countR==0:
            self.win="Black"
        else:
            self.win="tie"
