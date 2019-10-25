#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from arcade import plethoraAPI

class Game(plethoraAPI.Game):
    def __init__(self) -> None:
        super().__init__(size=(800, 600), fps=60)


    def onevent(self, event: pygame.event) -> bool:
        if event.type == pygame.QUIT:
            self.onexit()
        return False

    def onrender(self) -> bool:
        return False