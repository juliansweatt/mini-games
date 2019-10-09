#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import join as pathjoin
import pathlib
import pygame

import chess

from pygame.locals import (
    K_SPACE,
    K_UP, K_k,
    K_DOWN, K_j,
    K_LEFT, K_h,
    K_RIGHT, K_l,
    K_ESCAPE, K_q,
    KEYDOWN, KEYUP,
    QUIT,
)


MASKS = M_UP, M_RIGHT, M_DOWN, M_LEFT = tuple(1 << i for i in range(4))


image_dir = pathlib.Path(__file__).with_name("images")

def get_piece_image(piece_type, color):
    return pygame.image.load(pathjoin(image_dir, "{}_{}.png".format(chess.PIECE_NAMES[piece_type], ["dark", "light"][color])))

def get_piece_border(piece_type):
    return pygame.image.load(pathjoin(image_dir, "{}_border.png".format(chess.PIECE_NAMES[piece_type])))

pieces = dict(
    (chess.Piece(piece_type, color), get_piece_image(piece_type, color))
    for piece_type in chess.PIECE_TYPES
    for color in chess.COLORS
    if piece_type != chess.P_NONE
)

piece_borders = dict(
    (piece_type, get_piece_border(piece_type))
    for piece_type in chess.PIECE_TYPES
    if piece_type != chess.P_NONE
)

def getPiece(char):
    lower = char.lower()
    if lower not in pieces:
        raise ValueError("key not in pieces: " + char)
    return pieces[lower][char.isupper()], pieces[lower][2]


class Square():
    def __init__(self, ind: int):
        self.ind = ind
        self.row = ind // 8
        self.col = ind % 8
        self.color = self.row % 2 != self.col % 2
        self.ld_ind = 0 if self.color else 1
        self.row_chr = str(8 - self.row)
        self.col_chr = chr(self.col + ord('A'))
        self.selected = False

    def get_xy(self, dim, pad):
        return (
            pad + self.col * dim,
            pad + self.row * dim
        )


class ChessGame():
    """
    8x8 Chess game
    """
    # TODO: update to use chess not BaseBoard

    def __init__(self, screen, clock = None, fps: int = 20):
        """ Chess game init """
        self.cont = True       # continue in run?
        self.screen = screen   # pygame screen
        self.clock = (clock     # pygame clock
            if clock else pygame.time.Clock()
        )
        self.fps = fps         # frames per second
        self.dirty = True      # need to redraw?
        self.dirty_cells = []  # specific cells that are dirty
        self.padding = 10      # padding around board
        self.square_dim = 60   # dimensions (w & h) of each square
        self.cursor = 52       # index (index=x+y*8) cursor position
        self.selected_square = None  # selected square
        self.square_surfaces = [  # surfaces for 2 squares
                pygame.Surface((self.square_dim,) * 2),  # light
                pygame.Surface((self.square_dim,) * 2)   # dark
                ]
        self.square_surfaces[0].fill(pygame.Color('#b4b4b4'))  # light
        self.square_surfaces[1].fill(pygame.Color('#5c5c5c'))  # dark
        self.cursor_padding = 3  # cursor padding (amt to occupy on border)
        self.cursor_surfaces = [
                # left/right vertical components
                pygame.Surface((self.cursor_padding,
                                self.square_dim)),
                # top/bottom horizontal components
                pygame.Surface((self.square_dim - 2 * self.cursor_padding,
                                self.cursor_padding))
                ]
        self.cursor_surfaces[0].fill((252, 94, 50))
        self.cursor_surfaces[1].fill((252, 94, 50))
        self.direction_mask = 0
        self.last_direction = 0
        self.direction_count = 0
        self.direction_count_repeat = 5
        self.select_surfaces = [
                # left/right vertical components
                pygame.Surface((self.cursor_padding,
                                self.square_dim)),
                # top/bottom horizontal components
                pygame.Surface((self.square_dim - 2 * self.cursor_padding,
                                self.cursor_padding))
                ]
        self.select_surfaces[0].fill((252, 94, 50))
        self.select_surfaces[1].fill((252, 94, 50))

        self.base_board = chess.BaseBoard()
        self.squares = tuple(
            Square(i)
            for i in range(64)
        )
        screen.fill((255, 255, 255))  # white screen

        pygame.display.set_mode((500, 500))

    def drawCell(self, ind):
        """ draw a single cell based on `ind` = x + y*8 """
        square = self.squares[ind]
        surf = self.square_surfaces[square.ld_ind]
        pos = square.get_xy(self.square_dim, self.padding)
        self.screen.blit(surf, pos)
        piece = self.base_board.get_piece_at(ind)
        if piece in pieces:
            # print(ind, repr(piece))
            self.screen.blit(pieces[piece], pos)
            if square.selected:
                self.screen.blit(piece_borders[piece.type], pos)
        # if square.has_piece:
        #     self.screen.blit(square.piece.img, pos)
        #     if square.selected:
        #         self.screen.blit(square.piece.border, pos)

    def drawBoard(self):
        """ render board if dirty; called from run """
        # print(repr(self.base_board))
        for i in range(64):
            self.drawCell(i)

    def drawCursor(self):
        """ draw the cursor to show selection """
        x, y = self.squares[self.cursor].get_xy(
                self.square_dim, self.padding)
        self.screen.blit(self.cursor_surfaces[0], (
            x,
            y))
        self.screen.blit(self.cursor_surfaces[0], (
            x + self.square_dim - self.cursor_padding,
            y))
        self.screen.blit(self.cursor_surfaces[1], (
            x + self.cursor_padding,
            y))
        self.screen.blit(self.cursor_surfaces[1], (
            x + self.cursor_padding,
            y + self.square_dim - self.cursor_padding))

    def onevent(self, e):
        """ called when an event is fired from run """
        if e.type == QUIT:
            self.cont = False
            return
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE or e.key == K_q:
                self.cont = False
                return
            elif e.key == K_SPACE:
                square = self.squares[self.cursor]
                if not self.selected_square:
                    if self.base_board.has_piece_at(square.ind):
                        square.selected = not square.selected
                        self.dirty_cells.append(self.cursor)
                        self.selected_square = square
                else:
                    if self.selected_square == square:
                        square.selected = False
                        self.dirty_cells.append(square.ind)
                        self.selected_square = None
                    else:
                        self.base_board.move(self.selected_square.ind, square.ind)
                        # square.set_piece(self.selected_square.piece)
                        # self.selected_square.set_piece(None)
                        self.selected_square.selected = False
                        self.dirty_cells.append(self.selected_square.ind)
                        self.dirty_cells.append(square.ind)
                        self.selected_square = None
            elif e.key in (K_UP, K_k):
                self.last_direction = self.direction_mask
                self.direction_mask |= M_UP
                self.direction_count = 0
            elif e.key in (K_RIGHT, K_l):
                self.last_direction = self.direction_mask
                self.direction_mask |= M_RIGHT
                self.direction_count = 0
            elif e.key in (K_DOWN, K_j):
                self.last_direction = self.direction_mask
                self.direction_mask |= M_DOWN
                self.direction_count = 0
            elif e.key in (K_LEFT, K_h):
                self.last_direction = self.direction_mask
                self.direction_mask |= M_LEFT
                self.direction_count = 0
        elif e.type == KEYUP:
            if e.key in (K_UP, K_k):
                self.direction_mask &= ~M_UP
            elif e.key in (K_RIGHT, K_l):
                self.direction_mask &= ~M_RIGHT
            elif e.key in (K_DOWN, K_j):
                self.direction_mask &= ~M_DOWN
            elif e.key in (K_LEFT, K_h):
                self.direction_mask &= ~M_LEFT

    def run(self):
        """ event run that calls onevent and drawBoard """
        bg = (255, 255, 255)
        while self.cont:
            for e in pygame.event.get():
                self.onevent(e)
            if self.direction_mask:
                if self.direction_count == 0 or self.direction_count > self.direction_count_repeat:
                    if self.direction_mask & M_UP:
                        # up
                        if self.cursor // 8 > 0:
                            self.dirty_cells.append(self.cursor)
                            self.cursor -= 8
                    if self.direction_mask & M_RIGHT:
                        # right
                        if self.cursor % 8 < 7:
                            self.dirty_cells.append(self.cursor)
                            self.cursor += 1
                    if self.direction_mask & M_DOWN:
                        # down
                        if self.cursor // 8 < 7:
                            self.dirty_cells.append(self.cursor)
                            self.cursor += 8
                    if self.direction_mask & M_LEFT:
                        # left
                        if self.cursor % 8 > 0:
                            self.dirty_cells.append(self.cursor)
                            self.cursor -= 1
                self.direction_count += 1
            dirty = self.dirty or bool(self.dirty_cells)
            if self.dirty:
                # entire screen dirty
                self.screen.fill(bg)  # fill bg with bg color
                self.drawBoard()      # draw entire board
                self.dirty = False    # now we're clean
            while self.dirty_cells:
                # one or a few cells dirty
                # keep drawing popped cells until clean
                self.drawCell(self.dirty_cells.pop())
            if dirty:
                # either entire screen or 1+ cells dirty
                self.drawCursor()      # draw cursor overlay
                pygame.display.flip()  # flip: necessary to update screen
            # non-busy tick; call once per frame
            self.clock.tick(self.fps)
            # sleep process to allow other programs to share processor
            pygame.time.wait(self.fps)


__entry__ = ChessGame
if __name__ == '__main__':
    pygame.init()
    ChessGame(pygame.display.set_mode((500, 500)),  # 60*8 + 10*2
          pygame.time.Clock(), 20).run()
    pygame.quit()
