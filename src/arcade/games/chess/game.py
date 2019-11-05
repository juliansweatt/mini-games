# -*- coding: utf-8 -*-

import enum
import pathlib
import pygame
import time

from arcade import plethoraAPI
from arcade.games.chess.chess import Square, Color, PieceType, Piece, BaseBoard
from typing import Tuple

def range_for(start, step, num):
    return range(start, start + step * num, step)

IMAGE_DIR = pathlib.Path(__file__).with_name("images")

# size of a chess square on a board
SQUARE_SIZE = (60, 60)

# alpha for piece
GHOST_ALPHA = 102

# Piece -> light or dark piece image
PIECE_IMAGES = {}
# Ghost Piece -> semi-transparent light or dark piece drawn
GHOST_IMAGES = {}
for pt in PieceType:
    for c in Color:
        piece = Piece(c, pt)
        path = IMAGE_DIR/"{}_{}.png".format(pt.name.lower(), c.name.lower())
        img = pygame.image.load(str(path))
        PIECE_IMAGES[piece] = img
        tmp = pygame.Surface(SQUARE_SIZE)
        tmp.fill((0, 255, 0))
        tmp.set_colorkey((0, 255, 0))
        tmp.blit(img, (0, 0))
        tmp.set_alpha(GHOST_ALPHA)
        GHOST_IMAGES[piece] = tmp

BORDER_ALPHA = 100

# background color (only seen on border): white
BG_COLOR = (104, 74, 50)

# padding (border) around board
BOARD_PADDING = 6

SQ_RECTS = tuple(pygame.Rect((x, y), SQUARE_SIZE)
    for y in range_for(BOARD_PADDING, SQUARE_SIZE[1], 8)
    for x in range_for(BOARD_PADDING, SQUARE_SIZE[0], 8)
)

# square colors for light and dark squares
SQUARE_COLORS = [None, None]
# light square color: light brown
SQUARE_COLORS[Color.LIGHT] = (240, 217, 181)
# dark square color: dark brown
SQUARE_COLORS[Color.DARK] = (181, 136, 99)

def _get_sq_surfs() -> Tuple[pygame.Surface, pygame.Surface]:
    sq_surfs = (
        pygame.Surface(SQUARE_SIZE),
        pygame.Surface(SQUARE_SIZE)
    )
    sq_surfs[Color.LIGHT].fill(SQUARE_COLORS[Color.LIGHT])
    sq_surfs[Color.DARK].fill(SQUARE_COLORS[Color.DARK])
    return sq_surfs

SQ_SURFS = _get_sq_surfs()

# width of lines inside a square to denote cursor location
CURSOR_PADDING = 5

# color of cursor: dark green
CURSOR_COLOR = (20, 112, 70)

def _get_cursor_surf():
    # left/right vertical rectangle
    vsurf = pygame.Surface((CURSOR_PADDING, SQUARE_SIZE[1]))
    vsurf.fill(CURSOR_COLOR)
    # top/bottom horizontal rectangle (can subtract 2 cursor paddings from w to prevent overlap)
    hsurf = pygame.Surface((SQUARE_SIZE[0] - 2 * CURSOR_PADDING, CURSOR_PADDING))
    hsurf.fill(CURSOR_COLOR)
    cursor_surf = pygame.Surface(SQUARE_SIZE)
    cursor_surf.set_colorkey((0, 0, 0))
    cursor_surf.blit(vsurf, (0, 0))
    cursor_surf.blit(vsurf, (SQUARE_SIZE[0] - CURSOR_PADDING, 0))
    cursor_surf.blit(hsurf, (CURSOR_PADDING, 0))
    cursor_surf.blit(hsurf, (CURSOR_PADDING, SQUARE_SIZE[1] - CURSOR_PADDING))
    return cursor_surf

CURSOR_SURF = _get_cursor_surf()

SELECTED_COLOR = (20, 85, 30)

SELECTED_ALPHA = 128

def _get_selected_surf():
    selected_surf = pygame.Surface(SQUARE_SIZE)
    selected_surf.fill(SELECTED_COLOR)
    selected_surf.set_alpha(SELECTED_ALPHA)
    return selected_surf

SELECTED_SURF = _get_selected_surf()

# pygame key tuples
UP_KEYS = (pygame.K_UP, pygame.K_k)
RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_l)
DOWN_KEYS = (pygame.K_DOWN, pygame.K_j)
LEFT_KEYS = (pygame.K_LEFT, pygame.K_h)

# game frames/sec
FPS = 60

# delay when key first pressed **in seconds**
# NOTE: `CPD = REPEAT_DELAY * FPS` -> "frames per delay" (now: FPD = 0.2 * 40 = 8)
REPEAT_DELAY = 0.2

# wait between presses when key held down **in seconds**
# NOTE: `CPW = REPEAT_WAIT * FPS` -> "frames per wait" (now: FPW = 0.05 * 40 = 2)
REPEAT_WAIT = 0.05


# util functions

def get_color(index):
    return Color((index // 8) % 2 != index % 2)

def pos_to_index(x, y):
    if (x < BOARD_PADDING or y < BOARD_PADDING or
            x > BOARD_PADDING + 8 * SQUARE_SIZE[0] or y > BOARD_PADDING + 8 * SQUARE_SIZE[1]):
        return None
    xfloor, yfloor = (x - BOARD_PADDING) // SQUARE_SIZE[0], (y - BOARD_PADDING) // SQUARE_SIZE[1]
    return xfloor + 8 * yfloor


@enum.unique
class DirMask(enum.IntFlag):
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8


class Game(plethoraAPI.Game):
    def __init__(self):
        size = (8 * SQUARE_SIZE[0] + 2 * BOARD_PADDING, 8 * SQUARE_SIZE[1] + 2 * BOARD_PADDING)
        super().__init__(size=size, fps=FPS)
        self.dirmask = DirMask(0)     # mask for directions (has all directions)
        self.dirtime = None           # direction time (when direction key first pressed)
        self.dirtime_repeat = None    # direction time repeat (when dir key repeated)
        self.cursor = Square.E2       # cursor
        self.selected_sq = None       # selected square
        self.baseboard = BaseBoard()  # baseboard ->TODO: update when chess has more abstract game
        self.dragpiece = None         # piece currently being dragged with mouse
        self.dragpos = None           # position of piece being dragged
        self.piecemoved = False       # indicates if piece moved at all between mouse DOWN and UP
        self.ignore_mouseup = False   # should ignore next mouseup event
        self.draw_cursor = True       # do blit cursor (turn off if only mouse events used)

    def onevent(self, event):
        if event.type == pygame.QUIT:
            self.onexit()
            return False
        dirty = False
        if event.type == pygame.KEYDOWN:
            dirty |= self.keydown(event)
        elif event.type == pygame.KEYUP:
            dirty |= self.keyup(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dirty |= self.mousedown(event)
        elif event.type == pygame.MOUSEMOTION:
            dirty |= self.mousemove(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dirty |= self.mouseup(event)
        return dirty

    def keydown(self, event):
        self.draw_cursor = True
        key = event.key
        dirty = False
        if key == pygame.K_SPACE:
            # TODO: dirtyRects
            dirty = True
            if self.selected_sq:
                if self.selected_sq != self.cursor:
                    self.baseboard.move(self.selected_sq, self.cursor)
                self.selected_sq = None
            elif self.baseboard.has_piece_at(self.cursor):
                self.selected_sq = self.cursor
        elif key in UP_KEYS:
            self.dirmask |= DirMask.UP
            self.dirmask &= ~DirMask.DOWN
        elif key in RIGHT_KEYS:
            self.dirmask |= DirMask.RIGHT
            self.dirmask &= ~DirMask.LEFT
        elif key in DOWN_KEYS:
            self.dirmask |= DirMask.DOWN
            self.dirmask &= ~DirMask.UP
        elif key in LEFT_KEYS:
            self.dirmask |= DirMask.LEFT
            self.dirmask &= ~DirMask.RIGHT
        dirty |= bool(self.dirmask)
        if not dirty:
            self.dirtime = None
        return dirty

    def keyup(self, event):
        dirty = False
        key = event.key
        if key == pygame.K_SPACE:
            dirty = True
        elif key in UP_KEYS:
            self.dirmask &= ~DirMask.UP
        elif key in RIGHT_KEYS:
            self.dirmask &= ~DirMask.RIGHT
        elif key in DOWN_KEYS:
            self.dirmask &= ~DirMask.DOWN
        elif key in LEFT_KEYS:
            self.dirmask &= ~DirMask.LEFT
        dirty |= bool(self.dirmask)
        if not dirty:
            self.dirtime = None
        return dirty

    def mousedown(self, event):
        index = pos_to_index(*event.pos)
        if index is None:
            return False
        self.cursor = Square.from_index(index)
        if self.selected_sq:
            if self.cursor != self.selected_sq:
                self.draw_cursor = False
                self.baseboard.move(self.selected_sq, self.cursor)
            self.ignore_mouseup = True
            self.selected_sq = None
            return True
        else:
            self.selected_sq = self.cursor
            p = self.baseboard[self.selected_sq]
            if p is not None:
                self.dragpiece = p
                x, y = event.pos
                self.dragpos = (x - SQUARE_SIZE[0] // 2, y - SQUARE_SIZE[1] // 2)
                self.piecemoved = False
                return True
        return False

    def mousemove(self, event):
        if self.dragpos:
            index = pos_to_index(*event.pos)
            if index is None:
                return False
            cursor = Square.from_index(index)
            x, y = event.pos
            self.dragpos = (x - SQUARE_SIZE[0] // 2, y - SQUARE_SIZE[1] // 2)
            if cursor != self.cursor:
                self.piecemoved = True
            return True
        return False

    def mouseup(self, event):
        if self.ignore_mouseup:
            self.ignore_mouseup = False
        else:
            index = pos_to_index(*event.pos)
            if index is None:
                self.dragpos = None
                self.dragpiece = None
                self.selected_sq = None
                return True
            self.cursor = Square.from_index(index)
            self.dragpiece = None
            self.dragpos = None
            if not self.piecemoved:
                self.selected_sq = self.cursor
            else:
                self.draw_cursor = False
                if self.selected_sq != self.cursor:
                    self.baseboard.move(self.selected_sq, self.cursor)
                self.selected_sq = None
        return True

    def onrender(self):
        # TODO: populate when plethoraAPI supports
        # self.dirtyRects = []
        if self.dirmask:
            move = False
            t = time.time()
            if self.dirtime is None:
                move = True
                self.dirtime = t
                self.dirtime_repeat = self.dirtime
            elif t - self.dirtime > REPEAT_DELAY:
                if t - self.dirtime_repeat > REPEAT_WAIT:
                    self.dirtime_repeat = t
                    move = True
            if move:
                inc = 0
                if DirMask.UP in self.dirmask:
                    if self.cursor.index // 8 > 0:
                        inc += -8
                if DirMask.RIGHT in self.dirmask:
                    if self.cursor.index % 8 < 7:
                        inc += 1
                if DirMask.DOWN in self.dirmask:
                    if self.cursor.index // 8 < 7:
                        inc += 8
                if DirMask.LEFT in self.dirmask:
                    if self.cursor.index % 8 > 0:
                        inc += -1
                if inc:
                    # TODO: dirtyRects (much lighter rendering)
                    self.cursor = Square.from_index(self.cursor.index + inc)
        # TODO: bust out into `onstart` when plethoraAPI supports
        self.display.fill(BG_COLOR)
        # draw board
        for i, (sq, p) in enumerate(zip(Square, self.baseboard)):
            sr = SQ_RECTS[i]
            self.display.blit(SQ_SURFS[get_color(i)], sr)
            sel_sr = SQ_RECTS[self.selected_sq.index] if sq == self.selected_sq else None
            if p is not None:
                if sel_sr:
                    # draw transparent ghost piece
                    self.display.blit(GHOST_IMAGES[p], sr)
                    # draw select background
                    self.display.blit(SELECTED_SURF, sr)
                else:
                    # draw normal piece
                    self.display.blit(PIECE_IMAGES[p], sr)
        # draw cursor
        if self.draw_cursor:
            ind = self.cursor.index
            x, y = ind // 8, ind % 8
            self.display.blit(CURSOR_SURF, SQ_RECTS[self.cursor.index])
        # draw drag piece
        if self.dragpos:
            self.display.blit(PIECE_IMAGES[self.dragpiece], self.dragpos)
        return bool(self.dirmask)
