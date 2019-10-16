#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

from arcade import plethoraAPI
from enum import IntFlag, auto, unique

from pygame.locals import (
    QUIT,
    K_SPACE,
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_q,
    KEYDOWN, KEYUP,
)

@unique
class ArrowMask(IntFlag):
    up = auto()
    right = auto()
    down = auto()
    left = auto()


class Game(plethoraAPI.Game):
    def __init__(self):
        super().__init__(size=(200, 200), fps=40)
        self.arrows = 0b0000
        self.arrows_hidden = 0b0000
        self.square_size = (25, 25)
        self.square_surf = pygame.Surface((self.square_size))
        self.square_rect = pygame.Rect((10, 10, *self.square_size))

    def onevent(self, event):
        if event.type == QUIT:
            self.onexit()
        if event.type == KEYDOWN:
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

    def move(self, x, y):
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

    def onrender(self):
        self.display.fill((200, 200, 200))
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
        self.display.blit(self.square_surf, self.square_rect.topleft)
        return bool(arrows)
