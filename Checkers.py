import pygame as pg
pg.init()

class Piece():
    def __init__(self):
        self.color="black" #or red
        self.king=False

    def setColor(self,col):
        if col=="red":
            self.color="red"
        elif col=="black":
            self.color="black"

class Checkers():
    def __init__(self):
        self.surfaceDim=420
        self.sqDim=60
        self.Board=pg.display.set_mode(self.surfaceDim,self.surfaceDim)

        self.white= (255,255,255)
        self.black= (0,0,0)
        self.red=(255,0,0)

        self.Board.fill(self.white)


while
