# -*- coding: utf-8 -*-

""" Plethora API

This module contains the API to launch PlethoraPy using pygame as well as Game,
which can be inhereted by each game to allow plethora to continue to render the
UI but make render and event calls to the game.

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
from typing import Callable, Tuple, Union, Optional
import importlib
import pathlib
import pygame  # type: ignore[import]
import sys

from pygame.locals import (  # type: ignore[import]
    QUIT,
    MOUSEBUTTONDOWN
)


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
            # TODO: instead of using main.py just import and call load_cartridge
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

    def main(self) -> None:
        """ :mod:`PlethoraAPI` main - this is the entry point and should be called from main() """
        self.dirty = True
        self.running = True
        self.mainloop()

    def import_game(self, idir: str, gameName: str, fname: str = "main") -> None:
        """ try to import a game; if succeeds: store in `self.imports`; if
            fails: store in `self.import_errors`

        Args:
            idir: include directory (eg "arcade.games")
            gameName: module name (eg "chess")
            fname: file name (defaults to main): :todo: just import module to call ``load_cartridge``
        """
        try:
            self.imports[gameName] = importlib.import_module(".".join([idir, gameName, fname]))
        except Exception as error:
            print("Error loading game, \"{}\": {}".format(gameName, error))
            self.import_errors[gameName] = error

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
            self.game_dirty = self.game.onevent(event)
        else:
            if event.type == QUIT:
                self.running = not self.onexit()
                if not self.running:
                    return
            if event.type == MOUSEBUTTONDOWN:
                # TODO: handle menu not just one button
                if not self.game:
                    if self.test_btn.rect.collidepoint(event.pos):
                        # handoff to Test as example
                        self.launch_game("test")

    def onrender(self) -> None:
        """ called when game or self is dirty to re-render """
        flip = False
        game_flip = False
        if self.dirty:
            # UI dirty
            self.draw_ui_el(self.title)
            if not self.game:
                self.draw_ui_el(self.test_btn)  # TODO: update with menu
            flip = True
            self.dirty = False
        if self.game and self.game_dirty:
            # game dirty; call :func:`game.onrender`
            self.game_dirty = self.game.onrender()
            game_flip = True
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
            el: a UI element that needs a :attr:`rect` and a :func:`get_blitsurface`
        """
        self.display.fill(self.background, el.rect)
        self.display.blit(el.get_blitsurface(), el.rect.topleft)

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
            self.game = self.imports[name].Game()
            self.game_surface = pygame.Surface(self.game.rect.size)
            self.fps, self.game_rect.size = self.game.register(self.game_surface, self.clock, self.handle_game_exit)
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

    A label has a :attr:`text` (which is returned from :func:`UILabel.get_blitsurface` and
    :attr:`rect` for position and size
    """
    def __init__(self, x: int, y: int, text: str, font: pygame.font, fontAntialias: bool = True,
            fontColor: Tuple[int,int,int] = (0, 0, 0),
            fontBackground: Optional[Tuple[int,int,int]] = None) -> None:
        """ UILabel constructor """
        self.font = font
        self.text = font.render(text, fontAntialias, fontColor, fontBackground)
        self.rect = pygame.Rect((x, y), self.text.get_size())

    def get_blitsurface(self) -> Union[pygame.text.Text,pygame.Surface]:
        """ get the blittable surface, :attr:`text` """
        return self.text


class UIButton():
    """ A UI button used by :mod:`PlethoraAPI`

    A button has a :attr:`surface` (which is returned from :func:`UIButton.get_blitsurface`) to
    which :attr:`text` is rendered; it also has a :attr:`rect` for position and size
    """
    def __init__(self,
            x: int,
            y: int,
            text: str,
            font: pygame.font.Font,
            fontAntialias: bool = True,
            fontColor: Union[Tuple[int,int,int], pygame.Color] = (0, 0, 0),
            background: Optional[Union[Tuple[int,int,int], pygame.Color]] = None,
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

    def get_blitsurface(self):
        """ get the blittable surface, :attr:`surface` """
        return self.surface


class Game():
    """
    A basic game that can be inherited. This game doesn't render anything. See
    the module docstring on how to use this class in a game.
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
