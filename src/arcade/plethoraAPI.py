# -*- coding: utf-8 -*-

from enum import Enum, unique
import pathlib
import importlib
import pygame
import sys

from typing import Callable

from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN
)

from typing import Callable, Tuple, Optional

""" Plethora API

This module contains the API to launch PlethoraPy using pygame as well as Game,
which can be inhereted by each game to allow plethora to continue to render the
UI but make render and event calls to the game.

Since pygame is implemented on a module-level, the Plethora API is, as well.

Usage:

>> import plethoraAPI
>> plethoraAPI.main()

"""


def main():
    api = PlethoraAPI()
    api.main()


class PlethoraAPI():
    def __init__(self):
        # initialize pygame and pygame.font
        pygame.init()
        pygame.font.init()

        self.imports = {}
        self.import_errors = {}
        # attempt to dynamically import all games
        here = pathlib.Path(__file__).parent
        for path in (here/"games").iterdir():
            if not (path/"main.py").is_file():
                continue
            self.import_game("arcade.games", path.name)

        self.size = self.width, self.height = (640, 400)
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background = (255, 255, 255)
        self.display.fill(self.background)
        self.clock = pygame.time.Clock()

        self.uifps = 20
        self.fps = self.uifps

        font_title = pygame.font.Font(str(here/"fonts/exo/Exo-Regular.ttf"), 50)
        font_menu_item = pygame.font.Font(str(here/"fonts/exo/Exo-Regular.ttf"), 30)

        self.title = UILabel(10, 10, "PlethoraPy", font_title)
        self.test_btn = UIButton(20, 30 + self.title.rect.height, "Test", font_menu_item, background=(128, 128, 128), padding=4)

        # TODO: create UIGame to help simplify game management
        self.game = None
        self.game_rect = pygame.Rect((20, 30 + self.title.rect.height), (0, 0))
        self.game_surface = None
        self.game_dirty = None

        self.dirty = False
        self.running = False

    def import_game(self, idir, gameName, fname="main"):
        try:
            self.imports[gameName] = importlib.import_module(".".join([idir, gameName, fname]))
        except Exception as error:
            self.import_errors[gameName] = error
            return None

    def main(self) -> None:
        self.dirty = True
        self.running = True
        self.mainloop()

    def mainloop(self) -> None:
        while self.running:
            for event in pygame.event.get():
                self.onevent(event)
            self.onrender()
            self.clock.tick(self.fps)

    def onevent(self, event: pygame.event) -> None:
        if self.game:
            self.game_dirty = self.game.onevent(event)
        else:
            if event.type == QUIT:
                self.running = not self.onexit()
                if not self.running:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if not self.game:
                    if self.test_btn.rect.collidepoint(event.pos):
                        # handoff to Test as example
                        self.launch_game("test")

    def onrender(self) -> None:
        flip = False
        game_flip = False
        if self.dirty:
            self.draw_ui_el(self.title)
            if not self.game:
                self.draw_ui_el(self.test_btn)  # TODO: update with menu
            flip = True
            self.dirty = False
        if self.game and self.game_dirty:
            self.game_dirty = self.game.onrender()
            game_flip = True
        if game_flip:
            self.display.fill(self.background, self.game_rect)
            self.display.blit(self.game_surface, self.game_rect.topleft)
            flip = True
        if flip:
            pygame.display.flip()

    def draw_ui_el(self, el):
        self.display.fill(self.background, el.rect)
        self.display.blit(el.blitsurface, el.rect.topleft)

    def launch_game(self, name):
        if name not in self.imports:
            if name in self.import_errors:
                print("Error: there was an error loading \"{}\": ".format(name), self.import_errors[name])
            else:
                print("Error: \"{}\" has not been loaded".format(name))
        elif self.imports[name] is None:
            print("Error: there was an error loading \"{}\": ".format(name), self.import_errors[name])
        else:
            self.game = self.imports[name].Game()
            self.game_surface = pygame.Surface(self.game.rect.size)
            self.fps, self.game_rect.size = self.game.register(self.game_surface, self.clock, self.handle_game_exit)
            self.game_dirty = True

    def handle_game_exit(self):
        self.game = None
        self.game_surface = None
        self.game_dirty = None
        self.display.fill(self.background)
        self.dirty = True
        # reset settings
        self.fps = self.uifps

    def onexit(self):
        """ PlethoraAPI onexit() """
        return True


@unique
class Side(Enum):
    top = "top"
    right = "right"
    bottom = "bottom"
    left = "left"

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Side.{}".format(self.name)

    def __hash__(self):
        return hash(self.name)


class UILabel():
    def __init__(self, x, y, text, font, fontAntialias=True, fontColor=(0, 0, 0), fontBackground=None):
        self.font = font
        self.text = font.render(text, fontAntialias, fontColor, fontBackground)
        self.rect = pygame.Rect((x, y), self.text.get_size())

    @property
    def blitsurface(self):
        return self.text


class UIButton():
    def __init__(self, x, y, text, font, fontAntialias=True, fontColor=(0, 0, 0), background=None, **kwargs):
        # use kwargs["padding"] to initially define padding
        self.padding = kwargs.get("padding", 0)
        if isinstance(self.padding, int):
            self.padding = dict((side, self.padding) for side in Side)
        for side in Side:
            # update padding[Side.?] individually
            self.padding[side] = kwargs.get("padding_{}".format(side), self.padding[side])
        self.font = font
        self.text = font.render(text, fontAntialias, fontColor)
        text_pos = kwargs.get("text_pos", (0, 0))
        self.rect = pygame.Rect(
            (x, y),
            tuple(sum(t) for t in zip(
                self.text.get_size(),
                text_pos,
                (self.padding[Side.left], self.padding[Side.top]),
                (self.padding[Side.right], self.padding[Side.bottom]),
            ))
        )
        # blit `UIButton#surface`
        self.surface = pygame.Surface(self.rect.size)
        self.background = background
        if self.background:
            self.surface.fill(background)
        self.text_pos = tuple(sum(t) for t in zip(text_pos, (self.padding[Side.left], self.padding[Side.top])))
        self.surface.blit(self.text, self.text_pos)

    @property
    def blitsurface(self):
        return self.surface


class Game():
    def __init__(self, size: Tuple[int] = (200, 200), fps: int = 20) -> None:
        self.display = None
        self.fps = fps
        self.rect = pygame.Rect((0, 0), size)
        self.game_exit = None

    def register(self, display: pygame.Surface, clock: pygame.time.Clock, game_exit: Callable) -> Tuple[int, Tuple[int, int]]:
        self.display = display
        self.clock = clock
        self.game_exit = game_exit
        return (self.fps, self.rect.size)

    def onevent(self):
        if not hasattr(self, "oneventImpl"):
            print("WARNING: implement Game#onevent")
        self.oneventImpl = True

    def onrender(self):
        if not hasattr(self, "onrenderImpl"):
            print("WARNING: implement Game#onrender()")
        self.onrenderImpl = True

    def onexit(self, should_exit=True):
        """ Game onexit() """
        if should_exit:
            self.game_exit()


if __name__ == "__main__":
    main()
