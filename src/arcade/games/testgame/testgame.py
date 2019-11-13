#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Plethora API Test Game

This submodule contains a small test game that demonstrates the initial PlethoraAPI.
:class:`arcade.plethoraAPI.PlethoraAPI` loads :file:`src/arcade/games/test/__init__.py` which loads
this module and returns a :class:`Game` instance
"""

import pygame

from arcade import plethoraAPI
from enum import IntFlag, auto, unique

from pygame.locals import (
    QUIT,
    K_SPACE,
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_q,
    KEYDOWN, KEYUP,
    MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN,
)

from typing import Tuple

@unique
class ArrowMask(IntFlag):
    """ Enum used to mask arrow keys (up, right, down, left) """
    up = auto()
    right = auto()
    down = auto()
    left = auto()


class Game(plethoraAPI.Game):
    """ The small test game that implements the plethora API

    A small black square can be moved with the arrow keys but is constrained to the viewport. When
    the left click for mouse is held down, the block can be dragged. When the user attempts to close
    the window, interecept and return to the main window.
    """

    def __init__(self) -> None:
        """ :class:`Game` constructor """
        super().__init__(size=(800, 600), fps=60)  # call plethoraAPI.Game.__init__ to initialize :attr:`size` and :attr:`fps`
        self.arrows = 0b0000  # bitmask for arrow keys
        self.arrows_hidden = 0b0000  # bitmask for hiding opposite keys on key down while that key is down
        square_size = (25, 25)  # size of the square
        self.square_surf = pygame.Surface(square_size)  # square surface
        self.square_rect = pygame.Rect((10, 10), square_size)  # square rect for position and bounds testing
        self.mouse_down_pos = None

    def onevent(self, event: pygame.event) -> bool:
        """ called from :func:`PlethoraAPI.mainloop` when there is an event while this game is running

        Args:
            event: a pygame.event fetched from :func:`pygame.event.get` in
                   :func:`arcade.plethoraAPI.PlethoraAPI.mainloop`

        Returns:
            bool: True if onrender should be called on the next frame; False otherwise
        """
        if event.type == QUIT:
            # exit game and return to main UI by calling onexit() defined in :class:`arcade.plethoraAPI.PlethoraAPI`
            self.onexit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_down_pos = event.pos
                return True
        elif event.type == MOUSEMOTION:
            if self.mouse_down_pos:
                self.mouse_down_pos = event.pos
                return True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down_pos = None
                return True
        elif event.type == KEYDOWN:
            # if arrow keydown:
            #   1) add to key mask to `self.arrows`
            #   2) add opposite key mask to `self.arrows_hidden`
            #   3) remove key mask from `self.arrows_hidden`
            if event.key == pygame.K_UP:
                self.arrows |= ArrowMask.up
                self.arrows_hidden |= ArrowMask.down
                self.arrows_hidden &= ~ArrowMask.up
            elif event.key == pygame.K_RIGHT:
                self.arrows |= ArrowMask.right
                self.arrows_hidden |= ArrowMask.left
                self.arrows_hidden &= ~ArrowMask.right
            elif event.key == pygame.K_DOWN:
                self.arrows |= ArrowMask.down
                self.arrows_hidden |= ArrowMask.up
                self.arrows_hidden &= ~ArrowMask.down
            elif event.key == pygame.K_LEFT:
                self.arrows |= ArrowMask.left
                self.arrows_hidden |= ArrowMask.right
                self.arrows_hidden &= ~ArrowMask.left
            else:
                return False
            return True
        if event.type == KEYUP:
            # if arrow keyup:
            #   1) remove key mask from `self.arrows`
            #   2) remove both key and opposite key from `self.arrows_hidden`
            if event.key == pygame.K_UP:
                self.arrows &= ~ArrowMask.up
                self.arrows_hidden &= ~(ArrowMask.up | ArrowMask.down)
            elif event.key == pygame.K_RIGHT:
                self.arrows &= ~ArrowMask.right
                self.arrows_hidden &= ~(ArrowMask.left | ArrowMask.right)
            elif event.key == pygame.K_DOWN:
                self.arrows &= ~ArrowMask.down
                self.arrows_hidden &= ~(ArrowMask.up | ArrowMask.down)
            elif event.key == pygame.K_LEFT:
                self.arrows &= ~ArrowMask.left
                self.arrows_hidden &= ~(ArrowMask.left | ArrowMask.right)
            else:
                return False
            return True
        return False

    def move(self, x: int, y: int) -> None:
        """ move square by x, y with bounds checking

        Args:
            x: move ``self.square_rect`` by x-pixels
            y: move ``self.square_rect`` by y-pixels
        """
        r = self.square_rect.move(x, y)
        if r.left < 0:
            r.left = 0
        elif r.right > self.rect.width:
            r.right = self.rect.width
        if r.top < 0:
            r.top = 0
        elif r.bottom > self.rect.height:
            r.bottom = self.rect.height
        self.square_rect = r

    def moveto(self, pos: Tuple[int, int]) -> None:
        """ move square to position x, y with bounds checking

        Args:
            x: set ``self.square_rect`` to x
            y: set ``self.square_rect`` to y
        """
        self.square_rect.center = pos
        if self.square_rect.left < 0:
            self.square_rect.left = 0
        elif self.square_rect.right > self.rect.width:
            self.square_rect.right = self.rect.right
        if self.square_rect.top < 0:
            self.square_rect.top = 0
        elif self.square_rect.bottom > self.rect.height:
            self.square_rect.bottom = self.rect.height

    def onrender(self) -> bool:
        """ called from :func:`PlethoraAPI.mainloop` when game is dirty

        The game is dirty when:
            - The game is first loaded
            - True is returned from :func:`Game.onevent`
            - True is returned from :func:`Game.onrender`

        Returns:
            bool: True if onrender should be called again on the next frame - this is useful if a
                  key is down and re-rendering should occur; False otherwise
        """
        self.display.fill((200, 200, 200))
        rerender = False
        if self.mouse_down_pos:
            self.moveto(self.mouse_down_pos)
        else:
            arrows = self.arrows & ~self.arrows_hidden
            vmove = 0
            hmove = 0
            if arrows & ArrowMask.up:
                vmove -= 5
            if arrows & ArrowMask.right:
                hmove += 5
            if arrows & ArrowMask.down:
                vmove += 5
            if arrows & ArrowMask.left:
                hmove -= 5
            if vmove or hmove:
                self.move(hmove, vmove)
            rerender = bool(arrows)  # return True if an arrow key is down; otherwise False
        self.display.blit(self.square_surf, self.square_rect.topleft)  # redraw square
        return rerender
