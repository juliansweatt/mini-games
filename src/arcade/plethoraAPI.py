# -*- coding: utf-8 -*-

""" Plethora API

This module contains the API to launch PlethoraPy using pygame as well as Game, which can be
inhereted by each game to allow plethora to continue to render the UI but make render and event
calls to the game.

Since pygame is implemented on a module-level, the Plethora API is, as well.

Main usage::

    import plethoraAPI
    plethoraAPI.main()

Game usage::

    # src/arcade/games/myGame/__init__.py
    import myGame
    def load_cartridge():
        return myGame.MyGame()

    # src/arcade/games/myGame/myGame.py
    from arcade import plethoraAPI
    class MyGame(plethoraAPI.Game):
        def __init__(self):
            super().__init__(size=(200, 200), fps=40)

        def onevent(self, event: pygame.event) -> bool:
            print(f"event receieved: {event}")
            return True  # indicates that we need to render

        def onrender(self) -> bool:
            print("rendering")
            self.display.fill((255, 255, 255))  # fake render
            return False  # indicates that we do not need to re-render

Running::

    $ pip install .
    $ plethora
"""

from enum import Enum, unique
from typing import Callable, List, Tuple, Union, Optional
import importlib
import functools
import pathlib
import pygame  # type: ignore[import]
import sys
import traceback

from pygame.locals import (  # type: ignore[import]
    QUIT,
    MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN,
)

MOUSE_TYPES = { MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN }


def main():
    """ entry_point for console_script `plethora` """
    api = PlethoraAPI()
    api.main()


class PlethoraAPI():
    """ This class runs the UI and launches a game via the API.

    In order for a game to run, it should extend :mod:`plethoraAPI.Game` and implement
    :func:`onrender` and :func:`onevent`. Then, the game should be placed in
    :file:`src/arcade/games/{name}/` and :file:`src/arcade/games/{name}/__init__.py` should contain
    the function, :func:`load_cartridge`, which returns a Game object that extends
    `plethoraAPI.Game`.
    """

    def __init__(self):
        """ :mod:`PlethoraAPI` constructor """
        # initialize pygame and pygame.font
        pygame.init()
        pygame.font.init()

        # attempt to dynamically import all games
        self.imports = {}
        self.import_errors = {}
        here = pathlib.Path(__file__).parent
        for path in (here/"games").iterdir():
            if not (path/"__init__.py").is_file():
                continue
            self.import_game("arcade.games", path.name)

        self.size = self.width, self.height = (640, 400)
        self.display = pygame.display.set_mode(self.size)
        self.background = (255, 255, 255)
        self.display.fill(self.background)
        self.clock = pygame.time.Clock()

        self.uifps = 20
        self.fps = self.uifps

        font_title = pygame.font.Font(str(here/"fonts/exo/Exo-Regular.ttf"), 50)
        font_menu_item = pygame.font.Font(str(here/"fonts/exo/Exo-Regular.ttf"), 30)

        self.title = UILabel(10, 10, "PlethoraPy", font_title)
        self.buttons = []
        btn_padding = 30
        # Test Button
        btn_start = 10 + self.title.rect.height + btn_padding
        self.add_button(UIButton(20, btn_start, "Chess",
                functools.partial(self.launch_game, "chess"), font_menu_item,
                background=(128, 128, 128), padding=4))
        # Tic-Tac-Toe Button
        btn_start += self.buttons[0].rect.height + btn_padding
        self.add_button(UIButton(20, btn_start, "Tic-Tac-Toe",
                functools.partial(self.launch_game, "tictactoe"), font_menu_item,
                background=(128, 128, 128), padding=4))
        # Connect 4 Button
        btn_start += self.buttons[1].rect.height + btn_padding
        self.add_button(UIButton(20, btn_start, "Connect 4",
                functools.partial(self.launch_game, "connect4"), font_menu_item,
                background=(128, 128, 128), padding=4))
        # Bomberman Button
        btn_start += self.buttons[2].rect.height + btn_padding
        self.add_button(UIButton(20, btn_start, "Bomberman",
                functools.partial(self.launch_game, "bomberman"), font_menu_item,
                background=(128, 128, 128), padding=4))
        # Checkers Button
        btn_start += self.buttons[3].rect.height + btn_padding
        self.add_button(UIButton(20, btn_start, "Checkers",
                functools.partial(self.launch_game, "checkers"), font_menu_item,
                background=(128, 128, 128), padding=4))        
        # btn_start += self.buttons[1].rect.height + btn_padding
        self.btn_await = None

        # TODO: create UIGame to help simplify game management
        self.game = None
        self.game_rect = pygame.Rect((20, 30 + self.title.rect.height), (0, 0))
        self.game_surface = None
        self.game_dirty = None

        self.dirty = False
        self.running = False

    def main(self) -> None:
        """ :mod:`PlethoraAPI` main - this is the entry point and should be called from main() """
        self.refill = True
        self.dirty = True
        self.running = True
        self.mainloop()

    def import_game(self, idir: str, gameName: str) -> None:
        """ try to import a game; if succeeds: store in `self.imports`; if fails: store in
            `self.import_errors`

        Args:
            idir: include directory (eg "arcade.games")
            gameName: module name (eg "chess")
        """
        try:
            self.imports[gameName] = importlib.import_module("{}.{}".format(idir, gameName))
        except Exception as error:
            print("Error loading game, \"{}\": {}".format(gameName, error))
            print("-" * 100)
            traceback.print_exc(file=sys.stdout)
            print("-" * 100)
            self.import_errors[gameName] = error

    def add_button(self, button) -> None:
        self.buttons.append(button)

    def mainloop(self) -> None:
        """ keep feeding events to :func:`plethoraAPI.onevent`, keep calling
            :func:`plethoraAPI.onrender`, and then sleep to share CPU thread.

        When this loop ends, the entire display will close.
        """
        while self.running:
            for event in pygame.event.get():
                self.onevent(event)
            self.onrender()
            self.clock.tick(self.fps)
        pygame.quit()

    def onevent(self, event: pygame.event) -> None:
        """ called when any event is generated

        Args:
            event: the event (has ``type`` and various attributes)
        """
        if self.game:
            if event.type in MOUSE_TYPES:
                event.abs_pos, event.pos = event.pos, (event.pos[0] - self.game_rect.left, event.pos[1] - self.game_rect.top)
            self.game_dirty |= self.game.onevent(event)
            return
        if event.type == QUIT:
            self.running = not self.onexit()
            if not self.running:
                return
        # TODO: handle menu not just buttons
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for btn in self.buttons:
                if btn.rect.collidepoint(pos):
                    self.btn_await = btn
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            pos = event.pos
            for btn in self.buttons:
                if btn == self.btn_await and btn.rect.collidepoint(pos):
                    btn.onclick()
            self.btn_await = None

    def onrender(self) -> None:
        """ called when game or self is dirty to re-render """
        flip = False
        if self.refill:
            self.display.fill(self.background)
            self.dirty = True
            self.refill = False
        if self.dirty:
            # UI dirty
            self.draw_ui_el(self.title)
            if not self.game:
                for btn in self.buttons:
                    # TODO: update with menu
                    self.draw_ui_el(btn)
            flip = True
            self.dirty = False
        if self.game and self.game_dirty:
            # game dirty; call :func:`game.onrender`
            self.game_dirty = self.game.onrender()
            # blit game to display
            self.display.fill(self.background, self.game_rect)
            self.display.blit(self.game_surface, self.game_rect.topleft)
            flip = True
        if flip:
            # either game or main display updated: flip
            pygame.display.flip()

    def draw_ui_el(self, el) -> None:
        """ draw ui element

        Args:
            el: a UI element that needs a :attr:`rect` and a :func:`surface` to blit
        """
        self.display.fill(self.background, el.rect)
        self.display.blit(el.surface, el.rect.topleft)

    def launch_game(self, name: str) -> None:
        """ load imported game and run it """
        if name not in self.imports:
            if name in self.import_errors:
                print("Error: there was an error loading \"{}\": ".format(name), self.import_errors[name])
            else:
                print("Error: \"{}\" has not been loaded".format(name))
        elif self.imports[name] is None:
            print("Error: there was an error loading \"{}\": ".format(name), self.import_errors[name])
        else:
            self.game = self.imports[name].insert_cartridge()
            self.game_surface = pygame.Surface(self.game.rect.size)
            self.fps, self.game_rect.size = self.game.register(self.game_surface, self.clock, self.handle_game_exit)
            w, h = self.size
            if self.game_rect.width + 2 * self.game_rect.left > self.width:
                w = self.game_rect.width + 2 * self.game_rect.left
            if self.game_rect.height + self.game_rect.top + self.game_rect.left > self.height:
                h = self.game_rect.height + self.game_rect.top + self.game_rect.left
            if (w, h) != self.size:
                pygame.display.set_mode((w, h))
                self.refill = True
                self.dirty = True
            self.game_dirty = True

    def handle_game_exit(self):
        """ (should be) called when running game exits """
        self.game = None
        self.game_surface = None
        self.game_dirty = None
        self.display.fill(self.background)
        self.dirty = True
        # reset settings
        self.fps = self.uifps
        if self.display.get_size() != self.size:
            pygame.display.set_mode(self.size)
            self.refill = True

    def onexit(self):
        """ PlethoraAPI onexit() """
        return True


@unique
class Side(Enum):
    """ Side for padding """

    top = "top"  #: top
    right = "right"  #: right
    bottom = "bottom"  #: bottom
    left = "left"  #: left

    def __str__(self) -> str:
        """ stringify for :func:`str` """
        return self.name

    def __repr__(self) -> str:
        """ raw print or :func:`repr` """
        return "Side.{}".format(self.name)

    def __hash__(self) -> int:
        """ hash for :func:`hash` and to store as keys in a dict """
        return hash(self.name)


class UILabel():
    """ A simple UI label used by :mod:`PlethoraAPI`

    A label has a :attr:`surface`, the rendered text that will be blitted, and :attr:`rect` for
    position and size
    """
    def __init__(self, x: int, y: int, text: str, font: pygame.font, fontAntialias: bool = True,
            fontColor: Tuple[int,int,int] = (0, 0, 0),
            fontBackground: Optional[Tuple[int,int,int]] = None) -> None:
        """ UILabel constructor """
        self.font = font
        self.surface = font.render(text, fontAntialias, fontColor, fontBackground)
        self.rect = pygame.Rect((x, y), self.surface.get_size())

class UIButton():
    """ A UI button used by :mod:`PlethoraAPI`

    A button has a :attr:`surface`, the surface that will be blitted, to which :attr:`text_surface`
    is rendered; it also has a :attr:`rect` for position and size
    """
    def __init__(self,
            x             : int,
            y             : int,
            text          : str,
            callback      : Callable,
            font          : pygame.font.Font,
            fontAntialias : bool = True,
            fontColor     : Union[Tuple[int,int,int], pygame.Color] = (0, 0, 0),
            background    : Optional[Union[Tuple[int,int,int], pygame.Color]] = None,
            **kwargs
        ) -> None:
        # use ``kwargs["padding"]`` to initially define padding
        self.padding = kwargs.get("padding", 0)
        if isinstance(self.padding, int):
            self.padding = dict((side, self.padding) for side in Side)
        for side in Side:
            # update ``padding[side]`` individually
            self.padding[side] = kwargs.get("padding_{}".format(side), self.padding[side])
        self.font = font
        self.text_surface = font.render(text, fontAntialias, fontColor)
        text_pos = kwargs.get("text_pos", (0, 0))
        self.rect = pygame.Rect(
            (x, y),
            tuple(sum(t) for t in zip(
                self.text_surface.get_size(),
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
        self.surface.blit(self.text_surface, self.text_pos)
        self.callback = callback

    def get_blitsurface(self) -> pygame.Surface:
        """ get the blittable surface, :attr:`surface` """
        return self.surface

    def onclick(self):
        self.callback()


class Game():
    """ Plethora Base Game for API

    A basic game that can be inherited. This game doesn't render anything. See the module docstring
    on how to use this class in a game.
    """

    def __init__(self, size: Tuple[int,int] = (200, 200), fps: int = 20) -> None:
        """ :mod:`Game` constructor """
        self.display = None
        self.fps = fps
        self.rect = pygame.Rect((0, 0), size)
        self.game_exit: Optional[Callable] = None

    def register(self, display: pygame.Surface, clock: pygame.time.Clock, game_exit: Callable) -> Tuple[int, Tuple[int, int]]:
        """ register a game with :mod:`PlethoraAPI` """
        self.display = display
        self.clock = clock
        self.game_exit = game_exit
        return (self.fps, self.rect.size)

    def onevent(self) -> bool:
        """ onevent stub """
        print("WARNING: implement Game#onevent")
        return False

    def onrender(self) -> bool:
        """ onrender stub """
        print("WARNING: implement Game#onrender()")
        return False

    def onexit(self, should_exit=True):
        """ Game onexit() """
        if should_exit:
            self.game_exit()


if __name__ == "__main__":
    """ main if :file:`plethoraAPI.py` called directly """
    main()
