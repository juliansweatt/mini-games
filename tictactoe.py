import pygame as pg
import Board
pg.init()

WINNER=""
cont=True   #continue

while cont:
    board=Board.Board()
    board.mainloop(WINNER)
    cont=board.endGame()
