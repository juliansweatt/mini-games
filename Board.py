import pygame as pg
pg.init()

class Board():
    def __init__(self):
        self.turn = 'x'
        self.moves=[''] *9              #array to track spaces
        self.clock=pg.time.Clock()
        self.dim=800                    #size of screen
        self.sqDim= 200
        self.square=(self.sqDim,self.sqDim)
        self.size= (self.dim, self.dim) #dimension for entire screen
        self.pad=100                    #all sides have 100 buffer
        self.center=(self.dim//2, self.pad//2)
        self.white= (255,255,255)
        self.black= (0,0,0)
        self.blue= (0,0,128)
        self.red=(255,0,0)
        self.run= True
        self.screen= pg.display.set_mode(self.size)
        self.font = pg.font.Font('freesansbold.ttf', 16)
        message="Welcome to Tic-Tac-Toe, X goes first. Select a space"
        self.text = self.font.render(message, True, self.black, self.white)
        self.dirty =True
        pg.display.set_caption("Tic-Tac-Toe")
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
        moveCount=0;
        box=-1
        win=''
        while self.run:
            if moveCount==9:
                message="It's a tie!"
            for event in pg.event.get():
                box=self.onevent(event)

            if self.dirty:
                self.onrender()
                if box != -1:
                    self.drawTurn(box)
                    box=-1

                pg.display.flip()
                self.dirty=False
                win=CheckWin(moves)
            if win=='x' or win=='o':
                message=win+"IS THE WINNER!"

            self.clock.tick(20)

    def onevent(self,event):
        if event.type==pg.MOUSEBUTTONDOWN:
            for x in range (0,9):
                if self.rects[x].collidepoint(event.pos):
                    print(event)
                    self.dirty=True
                    return int(x)

        if event.type == pg.QUIT:
            self.run=False

    def drawTurn(self,box):
        if self.turn == 'x':
            self.moves[box]='x'
            print(box)
        if self.turn == 'o':
            self.moves[box]='o'
            print(box)

    def CheckWin(self):
        #Chech rows for win
        if self.moves[0] == self.moves[1] and self.moves[1]==self.moves[2]:
            return self.moves[0]
        elif self.moves[3] == self.moves[4] and self.moves[4]==self.moves[5]:
            return self.moves[3]
        elif self.moves[6] == self.moves[7] and self.moves[7]==self.moves[8]:
            return self.moves[6]
        #check columns for win
        if self.moves[0] == self.moves[3] and self.moves[3]==self.moves[6]:
            return self.moves[0]
        elif self.moves[1] == self.moves[4] and self.moves[4]==self.moves[7]:
            return self.moves[1]
        elif self.moves[2] == self.moves[5] and self.moves[5]==self.moves[8]:
            return self.moves[2]
        #check Diagonals for win
        if self.moves[0] == self.moves[4] and self.moves[4]==self.moves[8]:
            return self.moves[1]
        elif self.moves[6] == self.moves[4] and self.moves[4]==self.moves[2]:
            return self.moves[3]
