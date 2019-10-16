import pygame as pg
pg.init()

class Board():
    def __init__(self):
        self.turn = 'x'
        self.moves=[''] *9              #array to track spaces
        self.clock=pg.time.Clock()
        self.dim=800                    #size of screen
        self.sqDim= 200
        self.size= (self.dim, self.dim) #dimension for entire screen
        self.pad=100
        self.center=(self.dim//2, 50)
        self.white= (255,255,255)
        self.black= (0,0,0)
        self.blue= (0,0,128)
        self.red=(255,0,0)
        self.run= True
        self.screen= pg.display.set_mode(self.size)
        self.font = pg.font.Font('freesansbold.ttf', 16)
        self.text = self.font.render('X goes first', True, self.black, self.white)
        self.dirty =True
        pg.display.set_caption("Tic-Tac-Toe")

    def onrender(self):
        p1=self.pad + self.sqDim
        p2=self.pad
        self.screen.fill(self.white)
        pg.draw.line(self.screen,self.black,(p1, p2), (p1, self.dim - p2)) #left vertical line
        pg.draw.line(self.screen,self.black,(p1+self.sqDim,p2),(p1+self.sqDim,self.dim-p2)) #right vertical

        pg.draw.line(self.screen,self.black,(p2, p1), (self.dim-p2,p1))  #upper horizontal
        pg.draw.line(self.screen,self.black,(p2, p1+self.sqDim), (self.dim-p2,p1+self.sqDim))  #lower horizontal
        self.textRect= self.text.get_rect()
        self.textRect.center = (self.center)
        self.screen.blit(self.text,self.textRect)


    def mainloop(self):
        while self.run:
            for event in pg.event.get():
                self.onevent(event)
            if self.dirty:
                self.onrender()
                pg.display.flip()
                self.dirty=False
            self.clock.tick(20)

    def onevent(self,event):
        if event.type==pg.MOUSEBUTTONDOWN:
            print(event)
        if event.type == pg.QUIT:
            self.run=False
