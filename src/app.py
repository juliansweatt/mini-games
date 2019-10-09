# -*- coding: utf-8 -*-

import importlib
import importlib.util
import pygame
import sys

from pygame.locals import *

class App():
    def __init__(self):
        self.running = False
        self.display = None
        self.size = self._width, self._height = (640, 400)
        self.fps = 20

    def run(self):
        # init
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("fonts/exo/Exo-Regular.ttf", 50)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Plethora Py')
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        # menu .. TODO: make more than one button
        self.btn_offset = (20, 20)
        self.btn_size = (150, 60)
        self.btn = pygame.Surface(self.btn_size)
        self.btn.fill((128, 128, 128))  # set btn background color to gray
        self.btn_rect = pygame.Rect((*self.btn_offset, *self.btn_size))
        btn_text = self.font.render("Chess", True, (0, 0, 0))
        self.btn.blit(btn_text, (5, 0))
        # main loop
        self.dirty = True
        self.running = True
        self.mainloop()

    def onevent(self, event):
        """ called every time pygame receives an event

            :TODO: expand to allow other buttons and don't hardcode src/chess
        """
        if event.type == pygame.QUIT:
            self.running = not self.onexit()
            if not self.running:
                return
        if event.type == pygame.MOUSEBUTTONDOWN:
            size = self.display.get_size()
            if self.btn_rect.collidepoint(event.pos):
                # handoff to chess as example
                # https://stackoverflow.com/questions/41861427/python-3-5-how-to-dynamically-import-a-module-given-the-full-file-path-in-the/41904558#41904558
                # TODO: resolve API details:
                #   a) do we completely hand off to game? *this is what happens now because it is easier*
                #   b) do we call game.onrender and game.onevent and manage everything?
                old_path = sys.path[:]
                # TODO: make not static and allow other games in a menu
                sys.path.insert(0, "src/chess")
                try:
                    spec = importlib.util.spec_from_file_location("dyn_module", "src/chess/main.py")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, '__entry__') and hasattr(module.__entry__, 'run'):
                        app = module.__entry__(self.display)
                        app.run()
                except Exception as e:
                    print("Error loading chess:", e)
                finally:
                    sys.path = old_path
                    self.dirty = True
                    pygame.display.set_mode(size)

    def render(self):
        """ fill background, render botton

            :TODO: in future, render menu, login/logout, other buttons, and game list
        """
        if self.dirty:
            self.display.fill((255, 255, 255))
            self.display.blit(self.btn, self.btn_offset)
            pygame.display.flip()

    def onexit(self) -> bool:
        """ called if exit event detected; returns True if should exit and False if not
        """
        return True

    def mainloop(self):
        """ game main loop; called from ``run()``
        """
        while self.running:
            for event in pygame.event.get():
                self.onevent(event)
            self.render()
            self.clock.tick(self.fps)
