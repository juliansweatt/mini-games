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
from typing import Callable, Dict, List, Tuple, Union, Optional
import importlib
import functools
import pathlib
import pygame  # type: ignore[import]
import sys
import traceback

from pygame.locals import (  # type: ignore[import]
    QUIT,
    MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN
)

MOUSE_TYPES = { MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN }

# initialize pygame and pygame.font
pygame.init()
pygame.font.init()


# Useful globals

ROOT = pathlib.Path(__file__).parent

FONT_TITLE = pygame.font.Font(str(ROOT/"fonts/exo/Exo-Regular.ttf"), 50)
FONT_MENU_ITEM = pygame.font.Font(str(ROOT/"fonts/exo/Exo-Regular.ttf"), 30)


api = None


def launch_api():
    global api
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
        """ :mod:`PlethoraAPI` constructor
        """

        # attempt to dynamically import all games
        self.imports = {}
        self.import_errors = {}
        self.games = {}
        for path in (ROOT/"games").iterdir():
            if not (path/"__init__.py").is_file():
                continue
            name = path.name
            loaded = self.import_game("arcade.games", name)
            if loaded:
                self.games[name] = self.imports[name].get_name()

        self.size = self.width, self.height = (400, 400)
        self.display = pygame.display.set_mode(self.size)
        self.background = (255, 255, 255)
        self.display.fill(self.background)
        self.clock = pygame.time.Clock()

        self.uifps = 20
        self.fps = self.uifps

        self.title = UILabel(100, 10, "PlethoraPy", FONT_TITLE, fromApi=True)
        logo = pygame.image.load(str(ROOT/"images/plethora-icon-shadow.png"))
        self.logo = pygame.transform.scale(logo, (80, 80))
        self.logo_rect = pygame.Rect(5, 5, 0, 0)

        self.clickables = []
        self.buttons = []
        self.menus = []
        self.click_await = None

        self.menu = self.add_menu(UIMenu(40, 120, self.games, self.onMenuClick,
                 FONT_MENU_ITEM, background=(255, 255, 255), lineColor=(185, 185, 185),
                 maxWidth=300, fixedWidth=True,
                 maxHeight=200, fixedHeight=True,
                 fromApi=True))

        backbtn = pygame.image.load(str(ROOT/"images/back-arrow.png"))
        backbtn.convert_alpha()
        self.backbtn = self.add_button(UIButton(20, 20, backbtn, self.close_game, padding=4, hidden=True, fromApi=True))

        self.game = None
        self.game_rect = pygame.Rect((20, 30 + self.title.rect.height), (0, 0))
        self.game_surface = None
        self.game_dirty = None

        self.dirty = False
        self.running = False

    def close_game(self):
        if not self.game:
            return
        self.game.onexit(True)
        self.dirty = True

    def main(self) -> None:
        """ :mod:`PlethoraAPI` main - this is the entry point and should be called from main()
        """
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
            return False
        return True

    def add_button(self, button: "UIButton", fromApi=False) -> None:
        self.buttons.append(button)
        self.clickables.append(button)
        return button

    def add_menu(self, menu: "UIMenu", fromApi=False) -> None:
        self.menus.append(menu)
        self.clickables.append(menu)
        return menu

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
        game_running = bool(self.game)
        if self.game:
            if event.type in MOUSE_TYPES:
                event.abs_pos, event.pos = event.pos, (event.pos[0] - self.game_rect.left, event.pos[1] - self.game_rect.top)
            self.game_dirty |= self.game.onevent(event)
            if event.type in MOUSE_TYPES:
                event.pos = event.abs_pos
        else:
            if event.type == QUIT:
                self.running = not self.onexit()
                if not self.running:
                    return
        inGame = False  # click inside game?
        if game_running and event.type in MOUSE_TYPES:
            # only allow game to intercept mouse clicks by setting `inGame`
            x, y = event.pos
            inGame = (x >= self.game_rect.left and x <= self.game_rect.right
                    and y >= self.game_rect.top and y <= self.game_rect.bottom)
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for el in self.clickables:
                if inGame and el.fromApi or el.hidden:
                    continue
                if el.rect.collidepoint(pos):
                    self.click_await = el
        elif event.type == MOUSEBUTTONDOWN and event.button in (4,5):
            pos = event.pos
            scrollAmt = (event.button - 4) * 2 - 1
            scrollJump = 4
            for el in self.menus:
                if inGame and el.fromApi or el.hidden:
                    continue
                if el.rect.collidepoint(pos):
                    el.scroll(scrollAmt * scrollJump)
                    self.dirty = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            pos = event.pos
            for el in self.clickables:
                if el == self.click_await and el.rect.collidepoint(pos):
                    el.onclick(pos)
            self.click_await = None

    def onMenuClick(self, itemInd, item):
        self.launch_game(item)

    def onrender(self) -> None:
        """ called when game or self is dirty to re-render
        """
        flip = False
        if self.refill:
            self.display.fill(self.background)
            self.dirty = True
            self.refill = False
        if self.dirty:
            # UI dirty
            self.draw_ui_el(self.title)
            if not self.game:
                self.display.blit(self.logo, self.logo_rect)
            for el in self.clickables:
                if el.hidden:
                    continue
                self.draw_ui_el(el)
            flip = True
            self.dirty = False
        if self.game and self.game_dirty:
            # game dirty; call :func:`game.onrender`
            self.game_dirty = self.game.onrender()
            if self.game:
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
        if el.background:
            self.display.fill(el.background, el.rect)
        self.display.blit(el.get_blitsurface(), el.rect.topleft)

    def launch_game(self, name: str) -> None:
        """ load imported game and run it
        """
        if name not in self.imports:
            if name in self.import_errors:
                print("Error: there was an error loading \"{}\": ".format(name), self.import_errors[name])
            else:
                print("Error: \"{}\" has not been loaded".format(name))
        elif self.imports[name] is None:
            print("Error: there was an error loading \"{}\": ".format(name), self.import_errors[name])
        else:
            self.backbtn.hidden = False
            self.menu.hidden = True
            try:
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
            except Exception as error:
                print("Error while running game: {}".format(error))
                print("-" * 100)
                traceback.print_exc(file=sys.stdout)
                print("-" * 100)
                return False
                self.handle_game_exit()

    def handle_game_exit(self):
        """ (should be) called when running game exits
        """
        self.backbtn.hidden = True
        self.menu.hidden = False
        self.click_await = None
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
        """ PlethoraAPI onexit()
        """
        return True


@unique
class Side(Enum):
    """ Side for padding
    """

    top = "top"  #: top
    right = "right"  #: right
    bottom = "bottom"  #: bottom
    left = "left"  #: left

    def __str__(self) -> str:
        """ stringify for :func:`str`
        """
        return self.name

    def __repr__(self) -> str:
        """ raw print or :func:`repr`
        """
        return "Side.{}".format(self.name)

    def __hash__(self) -> int:
        """ hash for :func:`hash` and to store as keys in a dict
        """
        return hash(self.name)


class UIEl:
    """ Base UI element

        This simply has a bounding rect and a surface

    """
    def __init__(self, x, y, w, h, surface=None, background=None, hidden=False, **kwargs):
        if surface:
            self.surface = surface
        else:
            if w is None or h is None:
                w = 0
                h = 0
            self.surface = pygame.Surface((w, h))
        if w is None:
            if surface is None:
                w = 0
            else:
                w = surface.get_width()
        if h is None:
            if surface is None:
                h = 0
            else:
                h = surface.get_height()
        self.rect = pygame.Rect(x, y, w, h)
        self.background = background
        self.hidden = hidden
        self.fromApi = kwargs.get("fromApi", False)

    def move(self, x, y):
        self.move_x(x)
        self.move_y(y)

    def move_x(self, x):
        self.rect.x += x

    def move_y(self, y):
        self.rect.y += y

    def set_size(self, w, h):
        self.set_width(w)
        self.set_height(h)

    def set_width(self, w):
        self.rect.width = w

    def set_height(self, h):
        self.rect.height = h

    def get_blitsurface(self):
        return self.surface


class UILabel(UIEl):
    """ A simple UI label used by :mod:`PlethoraAPI`
        A label has a :attr:`surface`, the rendered text that will be blitted, and :attr:`rect` for
        position and size
    """
    def __init__(self,
            x: int,
            y: int,
            text: str,
            font: pygame.font = FONT_TITLE,
            fontAntialias: bool = True,
            fontColor: Tuple[int,int,int] = (0, 0, 0),
            fontBackground: Optional[Tuple[int,int,int]] = None,
            **kwargs
        ) -> None:
        """ UILabel constructor
        """
        self.font = font
        self.text = text
        self.fontAntialias = fontAntialias
        self.fontColor = fontColor
        surface = font.render(text, fontAntialias, fontColor, fontBackground)
        super().__init__(x, y, *surface.get_size(), surface=surface, background=fontBackground, **kwargs)

    def set_text(self, text: str):
        self.surface = self.font.render(self.text, self.fontAntialias, self.fontColor, self.fontBackground)
        self.set_size(*surface.get_size())

    def get_blitsurface(self):
        return self.surface


class UIButton(UIEl):
    """ A UI button used by :mod:`PlethoraAPI`
    A button has a :attr:`surface`, the surface that will be blitted, to which :attr:`text_surface`
    is rendered; it also has a :attr:`rect` for position and size
    """
    def __init__(self,
            x             : int,
            y             : int,
            text          : Union[str,"pygame.image"],
            callback      : Callable,
            font          : pygame.font.Font = FONT_MENU_ITEM,
            fontAntialias : bool = True,
            fontColor     : Union[Tuple[int,int,int], pygame.Color] = (0, 0, 0),
            background    : Optional[Union[Tuple[int,int,int], pygame.Color]] = None,
            **kwargs
        ) -> None:
        # use kwargs["padding"] to initially define padding
        self.padding = kwargs.get("padding", 0)
        if isinstance(self.padding, int):
            self.padding = dict((side, self.padding) for side in Side)
        for side in Side:
            # update ``padding[side]`` individually
            self.padding[side] = kwargs.get("padding_{}".format(side), self.padding[side])
        self.font = font
        if isinstance(text, str):
            self.text_surface = font.render(text, fontAntialias, fontColor)
        else:
            # assuume it is a surface
            self.text_surface = text  # great names.. best names.. big hands.. fake news
        self.text_pos = kwargs.get("text_pos", (0, 0))
        w, h = (sum(t)
                for t in zip(
                    self.text_surface.get_size(),
                    self.text_pos,
                    (self.padding[Side.left], self.padding[Side.top]),
                    (self.padding[Side.right], self.padding[Side.bottom])))
        super().__init__(x, y, w, h, **kwargs)
        self.rect = pygame.Rect(
            (x, y),
            tuple(sum(t) for t in zip(
                self.text_surface.get_size(),
                self.text_pos,
                (self.padding[Side.left], self.padding[Side.top]),
                (self.padding[Side.right], self.padding[Side.bottom]),
            ))
        )
        if isinstance(text, str):
            if self.background is None:
                self.surface.fill((1, 1, 1))
                self.surface.set_colorkey((1, 1, 1))
            else:
                self.surface.fill(background)
            self.surface.blit(self.text_surface, self.text_pos)
        else:
            # assume it's a surface
            self.surface = text  # great names.. best names.. big hands.. fake news
        self.text_pos = tuple(sum(t) for t in zip(self.text_pos, (self.padding[Side.left], self.padding[Side.top])))
        self.callback = callback

    def onclick(self, pos=None):
        """ onclick event handler

            to be called, for example, by the API when it recognizes that a button has been clicked
        """
        self.callback()

    def onclick(self):
        self.callback()


class UIMenu(UIEl):
    """ A UI button used by :mod:`PlethoraAPI`

    A button has a :attr:`surface`, the surface that will be blitted, to which :attr:`text_surface`
    is rendered; it also has a :attr:`rect` for position and size
    """

    def __init__(self,
            x : int,
            y : int,
            items: Union[List[str],Dict[str,str]],
            callback: Callable,
            itemFont: pygame.font.Font,
            fontAntialias: bool = True,
            fontColor : Union[Tuple[int,int,int], pygame.Color] = (0, 0, 0),
            lineColor: Union[Tuple[int,int,int], pygame.Color] = (0, 0, 0),
            background: Optional[Union[Tuple[int,int,int], pygame.Color]] = None,
            maxWidth: Optional[int] = None,
            maxHeight: Optional[int] = None,
            fixedWidth: bool = True,
            fixedHeight: bool = False,
            lineMargin: int = 2,
            lineHeight: int = 2,
            borderColor: Union[Tuple[int,int,int], pygame.Color] = (180, 180, 180),
            borderThickness: int = 4,
            **kwargs
        ) -> None:
        self.x = x
        self.y = y
        self.callback = callback
        self.itemFont = itemFont
        self.fontAntialias = fontAntialias
        self.background = background
        self.fontColor = fontColor
        self.lineColor = lineColor
        self.borderColor = borderColor
        self.borderThickness = borderThickness
        # amount scrolled
        self.scrollAmt = 0
        if isinstance(items, dict):
            self.itemKeys, self.itemTitles = zip(*items.items())
        else:
            # should be list or tuple of strings
            self.itemKeys = items[:]
            self.itemTitles = self.itemKeys
        self.fixedWidth = fixedWidth
        self.maxWidth = maxWidth
        self.fixedHeight = fixedHeight
        self.maxHeight = maxHeight
        self.lineMargin = lineMargin
        self.lineHeight = lineHeight
        self._update()
        super().__init__(self.x, self.y,
                self.width, self.height,
                surface=self.surface, **kwargs)

    def scroll(self, amt: int) -> None:
        self.scrollAmt += amt
        if self.scrollAmt < 0:
            self.scrollAmt = 0
        if self.scrollAmt > 999: pass # TODO

    def _update(self):
        self.items = list(self.itemFont.render(item, self.fontAntialias, self.fontColor) for item in self.itemTitles)
        self.widths = list(item.get_width() for item in self.items)
        self.heights = list(item.get_height() for item in self.items)
        # width
        if self.fixedWidth:
            self.width = self.maxWidth if self.maxWidth is not None else max(self.widths)
        else:
            self.width = min(max(self.widths), self.maxWidth)
        # height
        all_h = sum(self.heights)
        extra = (2 * self.lineMargin + self.lineHeight) * (len(self.heights) - 1)
        self.full_height = all_h + extra
        if self.fixedHeight:
            self.height = self.maxHeight if self.maxHeight is not None else all_h + extra
        else:
            self.height = self.full_height
        # bounding rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.full_rect = pygame.Rect(self.x, self.y, self.width, self.full_height)
        # surface and background
        self.surface = pygame.Surface(self.rect.size)
        self.full_surface = pygame.Surface(self.full_rect.size)
        if self.background is None:
            self.full_surface.fill((1, 1, 1))
            self.full_surface.set_colorkey((1, 1, 1))
        else:
            self.full_surface.fill(self.background)
        y = 0
        lastInd = len(self.items) - 1
        for ind, (height, item) in enumerate(zip(self.heights, self.items)):
            self.full_surface.blit(item, (0, y))
            if ind < lastInd:
                liney = y + height + self.lineMargin + self.lineHeight
                self.full_surface.fill(self.lineColor, (0, liney, self.width, self.lineHeight))
            y += height + self.lineMargin * 2 + self.lineHeight

    def get_blitsurface(self) -> pygame.Surface:
        """ get the blittable surface (self.surface)
        """
        # self.surface.fill((255, 0, 0), (0, self.height - 10, self.width, 10))
        self.surface.blit(self.full_surface, (0, 0), pygame.Rect(0, self.scrollAmt, self.width, self.height))
        bot = self.full_height - self.scrollAmt
        if bot < self.height:
            if self.background is None:
                # TODO: FIXME
                self.surface.fill((255, 255, 255), (0, bot, self.width, self.height - bot))
                # self.surface.fill((1, 1, 1), (0, bot, self.width, self.height - bot))
                # self.surface.set_colorkey((1, 1, 1))
            else:
                self.surface.fill(background, (0, bot, self.width, self.height - bot))
        newsurf = pygame.Surface((self.width + 2 * self.borderThickness, self.height + 2 * self.borderThickness))
        newsurf.fill(self.borderColor)
        newsurf.blit(self.surface, (self.borderThickness, self.borderThickness))
        return newsurf

    def onclick(self, pos):
        y = pos[1]
        y -= self.rect.top + self.lineHeight + self.lineMargin // 2 - self.scrollAmt
        ind = 0
        tmpy, *heights = self.heights
        for h in heights:
            if tmpy > y:
                break
            tmpy += h + self.lineMargin * (1 if ind == 0 else 2) + self.lineHeight
            ind += 1
        self.callback(ind, self.itemKeys[ind])


class Game():
    """ Plethora Base Game for API

        A basic game that can be inherited. This game doesn't render anything. See the module
        docstring on how to use this class in a game.
    """

    def __init__(self, size: Tuple[int,int] = (200, 200), fps: int = 20) -> None:
        """ :mod:`Game` constructor
        """
        self.display = None
        self.fps = fps
        self.rect = pygame.Rect((0, 0), size)
        self.game_exit: Optional[Callable] = None

    def register(self, display: pygame.Surface, clock: pygame.time.Clock, game_exit: Callable) -> Tuple[int, Tuple[int, int]]:
        """ register a game with :mod:`PlethoraAPI`
        """
        self.display = display
        self.clock = clock
        self.game_exit = game_exit
        return (self.fps, self.rect.size)

    def onevent(self) -> bool:
        """ onevent stub
        """
        print("WARNING: implement Game#onevent")
        return False

    def onrender(self) -> bool:
        """ onrender stub
        """
        print("WARNING: implement Game#onrender()")
        return False

    def onexit(self, should_exit=True):
        """ Game onexit()
        """
        if should_exit:
            self.game_exit()


def main():
    """ entry_point for console_script `plethora`
    """
    launch_api()


if __name__ == "__main__":
    """ main if plethoraAPI.py called directly
    """
    main()
