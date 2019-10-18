import pygame as pg
pg.init()

class Board():
    def __init__(self):
        self.moveCount=0;
        self.box=-1
        self.turn = 'X'
        self.moves=['-'] *9              #array to track spaces
        self.win='-'

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
        self.screen= pg.display.set_mode(self.size)         #main surface
        self.font = pg.font.Font('freesansbold.ttf', 16)
        self.message="Welcome to Tic-Tac-Toe, X goes first. Select a space"
        self.text = self.font.render(self.message, True, self.black, self.white)
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
        print(self.message)
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
        print(self.win)

    def mainloop(self,WINNER):
        while self.run:
            if self.moveCount==9:
                self.message="It's a tie!"
                self.run=False
            for event in pg.event.get():
                self.onevent(event)    # box=(clicked box)

            if self.dirty:
                self.onrender()
                if self.box != -1:
                    self.drawTurn(self.moveCount)
                    print(self.moveCount)
                    self.box=-1

                pg.display.flip()
                self.dirty=False
                self.CheckWin()             #after every move check for a win
            if self.win=='X' or self.win=='O':
                self.message=self.win+" IS THE WINNER!"
                self.run=False
            self.clock.tick(20)


    def endGame(self):
        c="-"
        while c!="yes" and c!="no":
            c= input("End Game: would you like to play again? (yes/no): ")

        if c=="yes":
            for x in range(len(self.moves)):
                self.moves[x]="-"
            self.box=-1
            self.turn='X'
            self.moveCount=0;
            return True

        elif c=="no":
            print("OK Bye!")
            return False

    def onevent(self,event):
        if event.type==pg.MOUSEBUTTONDOWN:
            for x in range (0,9):
                if self.rects[x].collidepoint(event.pos):
                    self.dirty=True
                    self.box=int(x)

        if event.type == pg.QUIT:
            self.run=False

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

        for x in range(len(self.moves)):
            print(self.moves[x], end=" ")
            if(x==2 or x==5):
                print("\n")
