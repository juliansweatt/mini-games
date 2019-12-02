import pygame as pg
from arcade import plethoraAPI


class Checkers(plethoraAPI.Game):
    def __init__(self):
        self.surfaceDim=480
        super().__init__(size=(self.surfaceDim,self.surfaceDim), fps=20)
        self.sqDim=60
        self.square=(60,60)
        #self.Board=pg.display.set_mode(self.surfaceDim,self.surfaceDim)
        self.selected=-1    #selected square
        self.clock=pg.time.Clock()

        self.white= (255,255,255)
        self.black= (0,0,0)
        self.red=(255,0,0)
        self.gray=(80,80,80)

        self.empty=pg.Surface(self.square)
        self.empty.fill(self.white)

        self.redPiece=pg.Surface(self.square)
        self.redPiece.fill(self.white)
        pg.draw.circle(self.redPiece,self.red,(self.sqDim//2,self.sqDim//2),self.sqDim//2)

        self.blackPiece=pg.Surface(self.square)
        self.blackPiece.fill(self.white)
        pg.draw.circle(self.blackPiece,self.black,(self.sqDim//2,self.sqDim//2),self.sqDim//2)

        self.rects = [
        pg.Rect((0,0),(self.square)), # row 1 column 1
        pg.Rect((2*self.sqDim,0),(self.square)), # r1 c3
        pg.Rect((4*self.sqDim,0),(self.square)), # r1 c5
        pg.Rect((6*self.sqDim,0),(self.square)), # r1 c7

        pg.Rect((self.square),(self.square)), # r2 c2
        pg.Rect((3*self.sqDim,self.sqDim),(self.square)), # r2 c4
        pg.Rect((5*self.sqDim,self.sqDim),(self.square)), # r2 c6
        pg.Rect((7*self.sqDim,self.sqDim),(self.square)), # r2 c8

        pg.Rect((0,self.sqDim*2),(self.square)), # r3 c1
        pg.Rect((2*self.sqDim,self.sqDim*2),(self.square)), # r3 c3
        pg.Rect((4*self.sqDim,self.sqDim*2),(self.square)), # r3 c5
        pg.Rect((6*self.sqDim,self.sqDim*2),(self.square)), # r3 c7

        pg.Rect((self.sqDim,self.sqDim*3),(self.square)), # r4 c2
        pg.Rect((3*self.sqDim,self.sqDim*3),(self.square)), # r4 c4
        pg.Rect((5*self.sqDim,self.sqDim*3),(self.square)), # r4 c6
        pg.Rect((7*self.sqDim,self.sqDim*3),(self.square)), # r4 c8

        pg.Rect((0,self.sqDim*4),(self.square)), # r5 c1
        pg.Rect((2*self.sqDim,self.sqDim*4),(self.square)), # r5 c3
        pg.Rect((4*self.sqDim,self.sqDim*4),(self.square)), # r5 c5
        pg.Rect((6*self.sqDim,self.sqDim*4),(self.square)), # r5 c7

        pg.Rect((self.sqDim,self.sqDim*5),(self.square)), # r6 c2
        pg.Rect((3*self.sqDim,self.sqDim*5),(self.square)), # r6 c4
        pg.Rect((5*self.sqDim,self.sqDim*5),(self.square)), # r6 c6
        pg.Rect((7*self.sqDim,self.sqDim*5),(self.square)), # r6 c8

        pg.Rect((0,self.sqDim*6),(self.square)), #r7 c1
        pg.Rect((2*self.sqDim,self.sqDim*6),(self.square)), #r7 c3
        pg.Rect((4*self.sqDim,self.sqDim*6),(self.square)), #r7 c5
        pg.Rect((6*self.sqDim,self.sqDim*6),(self.square)), #r7 c7

        pg.Rect((self.sqDim,self.sqDim*7),(self.square)), #r8 c2
        pg.Rect((3*self.sqDim,self.sqDim*7),(self.square)), #r8 c4
        pg.Rect((5*self.sqDim,self.sqDim*7),(self.square)), #r8 c6
        pg.Rect((7*self.sqDim,self.sqDim*7),(self.square)) #r8 c8
        ]

        self.spaces = [
        "B","B","B","B",
        "B","B","B","B",
        "B","B","B","B",
        "-","-","-","-",
        "-","-","-","-",
        "R","R","R","R",
        "R","R","R","R",
        "R","R","R","R"
        ] #background array of valid spaces for pieces to move
                    #kings represented by KR and KB
        self.moves=0
        self.turn="R" #or "B"
        self.win='tie'
        self.countR=12
        self.countB=12

    def onrender(self): # draw black square with appropriate piece and blit onto
                        # board using rects[]
        self.display.fill(self.red)

        for i, x in enumerate(self.spaces):
            if x=="-":
                self.display.blit(self.empty,self.rects[i])
                continue
            elif x=="B":
                self.display.blit(self.blackPiece,self.rects[i])
                continue
            elif x=="R":
                self.display.blit(self.redPiece,self.rects[i])
                continue
            elif x=="KB":
                continue
            elif x=="KR":
                continue
        return False

    def onevent(self,event):
        dirty = False
        if event.type==pg.QUIT:
            self.onexit()
            return False
        else:
            if event.type==pg.MOUSEBUTTONDOWN:
                if self.selected>=0:
                    for x in range(0,32):
                        if self.rects[x].collidepoint(event.pos):
                            if self.validMove(x):
                                self.spaces[self.selected]="-"
                                self.spaces[x]=self.turn
                                if self.turn=="R":
                                    self.turn="B"
                                else:
                                    self.turn="R"
                                self.selected=-1
                                return True

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
                                    break #invalid piece
                                self.rects[x].fill(self.gray)
        return False

    def validMove(self,x):
        if self.spaces[x]==self.turn: #can't move on top of own piece
            return False
        if self.turn=="B":
            if (self.selected==0 or self.selected==8 or self.selected==16 or self.selected==24 or #left side
                self.selected==7 or self.selected==15 or self.selected==23): #right side
                if self.selected==x-4:
                    if self.spaces[x]=="-":
                        return True
                    elif self.spaces[x]=="R" or self.spaces=="KR":
                        if jumpPiece(x):
                            return True
            else:
                if self.selected+4==x or self.selected+3==x: #middle
                    if self.spaces[x]=="-":
                        return True
                    elif self.spaces[x]=="R" or self.spaces=="KR":
                        if jumpPiece(x):
                            return True

                    return True

        elif self.turn=="R":
            if (self.selected==24 or self.selected==16 or self.selected==8 or #left
                self.selected==31 or self.selected==23 or self.selected==15 or self.selected==7): #right
                if self.selected==x+4:
                    return True
            else:
                if self.selected-4==x or self.selected-3==x:
                    return True

        return False

    def jumpPiece(self,x): #checks a valid jump and forces mulitple jumps if possible

        return False
    def checkWin(self): #checks if either side has lost all pieces (moves>=80 means tie)
        #if moves==80:
        #    self.win="Tie"
        if countB==0:
            self.win="Red"
        elif countR==0:
            self.win="Black"
        else:
            self.win="Tie"
