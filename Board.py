import pygame as pg
pg.init()

class Board():
    def __init__(self):
        self.clock=pg.time.Clock()
        self.size= (900, 900)
        self.center= (450,25)
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
        self.screen.fill(self.white)
        pg.draw.line(self.screen, self.black, (300,100), (300,700)) #left vertical line
        pg.draw.line(self.screen, self.black, (600,100), (600,700)) #right vertical
        pg.draw.line(self.screen, self.black, (50,300), (850,300))  #upper horizontal
        pg.draw.line(self.screen, self.black, (50,500), (850,500))  #lower horizontal
        self.textRect= self.text.get_rect()
        self.textRect.center = (450,25)
        self.screen.blit(self.text,self.textRect)


    def mainloop(self):
        while self.run:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    self.run=False
            if self.dirty:
                self.onrender()
                pg.display.flip()
                self.dirty=False
            self.clock.tick(20)
