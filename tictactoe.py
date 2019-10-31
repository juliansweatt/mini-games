import pygame as pg
import Board
pg.init()

WINNER=""
cont=True   #continue

while cont:
    board=Board.Board()
    WINNER=board.mainloop()
    cont=board.endGame()
