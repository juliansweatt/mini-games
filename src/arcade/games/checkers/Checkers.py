import pygame as pg
from arcade import plethoraAPI
import math

class Checkers(plethoraAPI.Game):
    def __init__(self):
        self.surfaceDim=480
        super().__init__(size=(self.surfaceDim,self.surfaceDim), fps=20)
        self.sqDim=60
        self.square=(60,60)
        #self.Board=pg.display.set_mode(self.surfaceDim,self.surfaceDim)
        self.selected=-1    #selected square
        self.piece="R"  #actual piece could be R KR B or KB
        self.clock=pg.time.Clock()

        self.white= (255,255,255)
        self.black= (0,0,0)
        self.red=(255,0,0)
        self.gray=(80,80,80)
        self.yellow=(204,204,0)

        self.empty=pg.Surface(self.square)
        self.empty.fill(self.white)

        self.redPiece=pg.Surface(self.square)
        self.redPiece.fill(self.white)
        pg.draw.circle(self.redPiece,self.red,(self.sqDim//2,self.sqDim//2),self.sqDim//2)

        self.blackPiece=pg.Surface(self.square)
        self.blackPiece.fill(self.white)
        pg.draw.circle(self.blackPiece,self.black,(self.sqDim//2,self.sqDim//2),self.sqDim//2)

        #self.kingBlack=self.blackPiece

        #self.kingRed=self.redPiece

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
            elif x=="B" or x=="KB":
                if i==self.selected:
                    self.blackPiece.fill(self.gray)
                    pg.draw.circle(self.blackPiece,self.black,(self.sqDim//2,self.sqDim//2),self.sqDim//2)

                self.display.blit(self.blackPiece,self.rects[i])
                if x=="KB":
                    pg.draw.arc(self.display, self.yellow, self.rects[i],0,2*math.pi,10)
                self.blackPiece.fill(self.white)
                pg.draw.circle(self.blackPiece,self.black,(self.sqDim//2,self.sqDim//2),self.sqDim//2)
                continue
            elif x=="R" or x=="KR":
                if i==self.selected:
                    self.redPiece.fill(self.gray)
                    pg.draw.circle(self.redPiece,self.red,(self.sqDim//2,self.sqDim//2),self.sqDim//2)

                self.display.blit(self.redPiece,self.rects[i])
                if x=="KR":
                    pg.draw.arc(self.display, self.yellow, self.rects[i],0,2*math.pi,10)
                self.redPiece.fill(self.white)
                pg.draw.circle(self.redPiece,self.red,(self.sqDim//2,self.sqDim//2),self.sqDim//2)

                continue
        return False

    def onevent(self,event):
        if event.type==pg.QUIT:
            self.onexit()
            return False
        else:
            if event.type==pg.MOUSEBUTTONDOWN:
                if self.selected>=0:
                    for x in range(0,32):
                        if self.rects[x].collidepoint(event.pos):
                            self.piece=self.spaces[self.selected]
                            if self.validMove(x):
                                self.kingME(x) #check for kings
                                if self.turn=="R":
                                    self.turn="B"
                                else:
                                    self.turn="R"

                                self.selected=-1
                                return True
                            else:
                                self.selected=-1
                                return True

                if self.selected==-1:
                    for x in range(0,32):
                        if self.rects[x].collidepoint(event.pos):
                                if self.spaces[x]==self.turn:   #correct piece selected
                                    self.selected=x
                                    return True
                                elif self.spaces[x]=="KR" and self.turn=='R': #select king
                                    self.selected=x
                                    return True
                                elif self.spaces[x]=="KB" and self.turn=='B': #select king
                                    self.selected=x
                                    return True
                                else:
                                    break #invalid piece
        return False

    def validMove(self,x):
        if self.piece=="B":
            if self.spaces[x]=="B" or self.spaces[x]=="KB":
                return False
            if x%8==0 or x+1%8==0: #edge of board
                if self.selected==x-4 and self.spaces[x]=="-":
                    self.spaces[self.selected]="-"
                    self.spaces[x]=self.piece
                    return True
            else:
                if self.spaces[x]=="-":
                    return self.noJumpDOWN(x)
                else: #if self.spaces[x]=="R" or self.spaces[x]=="KR":
                    if self.jumpDOWN(x):
                        #TODO while self.checkJump(): #more possible moves
                        self.countR-=1
                        return True

        elif self.piece=="R":
            if self.spaces[x]=="R" or self.spaces[x]=="KR":
                return False
            if x%8==0 or x+1%8==0: #edge of board
                if self.selected==x+4 and self.spaces[x]=="-":
                    self.spaces[self.selected]="-"
                    self.spaces[x]=self.piece
                    return True
            else:
                if self.spaces[x]=="-":
                    return self.noJumpUP(x)
                else: #if self.spaces[x]=="B" or self.spaces[x]=="KB":
                    if self.jumpUP(x):
                        #TODO while self.checkJump(): #more possible moves
                        self.countB-=1
                        return True
        elif self.piece=="KR":
            if self.selected-x<0:
                if self.spaces[x]=="-":
                    return self.noJumpDOWN(x)
                else: #if self.spaces[x]=="B" or self.spaces[x]=="KB":
                    return self.jumpDOWN(x)
            else:
                if self.spaces[x]=="-":
                    return self.noJumpUP(x)
                else: #if self.spaces[x]=="B" or self.spaces[x]=="KB":
                    return self.jumpUP(x)

        else:#self.piece=="KB":
            if self.selected-x<0:
                if self.spaces[x]=="-":
                    return self.noJumpDOWN(x)
                else: #if self.spaces[x]=="R" or self.spaces[x]=="KR":
                    return self.jumpDOWN(x)
            else:
                if self.spaces[x]=="-":
                    return self.noJumpUP(x)
                else: #if self.spaces[x]=="R" or self.spaces[x]=="KR":
                    return self.jumpUP(x)

        return False

    def noJumpDOWN(self,x): #black goes down
        if self.selected+4==x:
            self.spaces[self.selected]="-"
            self.spaces[x]=self.piece
            return True
        elif (self.selected//4)%2==0 and self.selected+3==x: #even rows
            self.spaces[self.selected]="-"
            self.spaces[x]=self.piece
            return True
        elif (self.selected//4)%2==1 and self.selected+5==x: #odd rows
            self.spaces[self.selected]="-"
            self.spaces[x]=self.piece
            return True
        else:
            return False

    def noJumpUP(self,x): #red goes up
        if self.selected-4==x:
            self.spaces[self.selected]="-"
            self.spaces[x]=self.piece
            return True
        elif (self.selected//4)%2==0 and self.selected-5==x: #even rows
            self.spaces[self.selected]="-"
            self.spaces[x]=self.piece
            return True
        elif (self.selected//4)%2==1 and self.selected-3==x: #odd rows
            self.spaces[self.selected]="-"
            self.spaces[x]=self.piece
            return True
        else:
            return False

    def jumpDOWN(self,x):
        if x%8==0 or x+1%8==0:
            return False #edge of board no where to jump

        row=self.selected//4
        if row%2==1:
            if x-self.selected==4 and self.spaces[x+3]=="-": #selected + 7 #odds left ((+4)-(+7) space jump)
                self.spaces[self.selected]="-"
                self.spaces[x]="-"
                self.spaces[x+3]=self.piece
                return True

            elif x-self.selected==5 and self.spaces[x+4]=="-": #odds right((+5)-(+9) space jump)
                self.spaces[self.selected]="-"
                self.spaces[x]="-"
                self.spaces[x+4]=self.piece # selected + 9
                return True

        else: # row%2==0
            if x-self.selected==3 and self.spaces[x+4]=="-": #evens left ((+3)-(+7) space jump)
                self.spaces[self.selected]="-"
                self.spaces[x]="-"
                self.spaces[x+4]=self.piece #selected + 7
                return True

            elif x-self.selected==4 and self.spaces[x+5]=="-": # evens right ((+4)-(+9) space jump)
                self.spaces[self.selected]="-"
                self.spaces[x]="-"
                self.spaces[x+5]=self.piece #selected + 9
                return True

        return False

    def jumpUP(self,x):
        if x%8==0 or x+1%8==0:
            return False #edge of board no where to jump

        row=self.selected//4
        if row%2==0:
            if self.selected-x==4 and self.spaces[x-3]=="-":#evens right ((-4)-(-7) space jump)
                self.spaces[self.selected]="-"
                self.spaces[x]="-"
                self.spaces[x-3]=self.piece #selected - 7
                return True

            elif self.selected-x==5 and self.spaces[x-4]=="-": #evens left((-5)-(-9) space jump)
                self.spaces[self.selected]="-"
                self.spaces[x]="-"
                self.spaces[x-4]=self.piece # selected - 9
                return True

        else: # row%2==1
            if self.selected-x==3 and self.spaces[x-4]=="-": #odds right ((-3)-(-7) space jump)
                self.spaces[self.selected]="-"
                self.spaces[x]="-"
                self.spaces[x-4]=self.piece #selected - 7
                return True

            elif self.selected-x==4 and self.spaces[x-5]=="-": # odds left ((-4)-(-9) space jump)
                self.spaces[self.selected]="-"
                self.spaces[x]="-"
                self.spaces[x-5]=self.piece #selected + 9
                return True

        return False

    def kingME(self,x):
        for i, x in enumerate(self.spaces):
            if i>27 and x=="B":
                self.spaces[i]="KB"
                continue
            if i<4 and x=="R":
                self.spaces[i]="KR"

    def checkWin(self): #checks if either side has lost all pieces (moves>=80 means tie)
        #if moves==80: #80 moves with no capture is tie
        #    self.win="Tie"
        if countB==0:
            self.win="Red"
        elif countR==0:
            self.win="Black"
        else:
            self.win="Tie"
