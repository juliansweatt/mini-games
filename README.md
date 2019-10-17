# Plethora Py


## Development


### Virtual Environment

A virtual environment in python allows developers to use different python
interpretters for a package and also manage dependencies without breaking user
or global python dependencies on the system. As a developer, you should create a
virtual environment to facilitate development.

#### Set up virtual environment

In order to set up a virtual environment, run `python3 -m venv env`. This
creates a `env/` directory that should be at the root of the project.

#### Using a virtual environment

While developing, you should make sure that you activate your virtual
environment (venv) when you:
- are using `pip`
- are using `python`

You can activate the venv by running `source env/bin/activate` in **sh/bash/zsh
shells on linux, bsd, and os x** [after setting up a
venv](#set-up-a-virtual-environment). (Fish and csh shells have different syntax
and, therefore, there are also `env/bin/activate.{fish,csh}` variants.)

You can activate the venv by running `call env/Scripts/activate.bat` on **windows** [after setting up a venv](#set-up-a-virtual-environment).

You can deactivate the venv if you want by calling `deactivate`.

### Running

Before you run Plethora Py, you need to build the package and its dependencies
as well as install a console script to run the program. `setup.py` with `pip`
makes this very easy.

First, [make sure you are in a venv](#using-a-virtual-environment).

Then, to build and install Plethora Py, use `pip install -e .`. This builds and installs Plethora Py in the venv, and it also installs the console script `plethora` that is accessible as a script in the venv. **You only need to run `pip install -e .` once as long as you use `-e`.**

Finally, to run Plethora Py, run the console script: `plethora`.


### Quickref

```sh
cd $somewhere/mini-games
python -m venv env       # only once to create venv
source env/bin/activate  # once per shell/terminal **
pip install -e .         # only once to build and install
plethora                 # run Plethora Py
```

\*\* `call env\Scripts\activate.bat` on windows

![quick reference terminal screenshot](.resources/quickref.png)


### Dependencies

If you want to add python programs for testing, feel free. Just make sure you
are in a venv and then use `pip install {pipy-pkg}`. `pytest` and `mypy` are
already being used for *unit testing* and *static type checking* (resp) for
*chess*. To install them both, use `pip install pytest mypy`, or you can install
just one.

If there is a **mandatory** dependency for a game, **be sure to add it to *setup.py* in `install_requires` list** and re-run `pip -install -e .` to rebuild.

## Plethora Py UI and API

Once `plethora` is run, it calls `plethoraAPI:main` in the arcade package. This
launches the UI and dynamically imports all games in the `src/arcade/games/`
directory that have an `__init__.py` file. For example, *chess* has
`src/arcade/games/chess/__init__.py` and all related files "next to"
`__init__.py`.

Each `__init__.py` should create a function called `insert_cartridge()` that
returns a *game* instance. Python developers often rely on duck typing to create
interfaces, however the *PlethoraAPI* class offers a `Game` class that can be
inherited. It will make your life much easier, as it handles registering the game
for you -- so long as you call `super().__init__(size=(400,400), fps=40)`, for
instance, in the games `__init__(self)`. The only other things you need to implement
then would be the `onrender(self)` and `onevent(self, event)` methods. See [Testgame Stubs](#testgame-stubs) to get quickly set up with a new game.

### Testgame Stubs

Use these to get set up with a new project.

Create `src/arcade/games/testgame/`

#### __init__.py

```python
from arcade.games.testgame import testgame

def insert_cartridge():
    return testgame.Game()
```

#### testgame.py

```python
# -*- coding: utf-8 -*-

""" Plethora API Test Game

This submodule contains small test game that demonstrates the initial PlethoraAPI.
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
)

@unique
class ArrowMask(IntFlag):
    """ Enum used to mask arrow keys (up, right, down, left)

    >>> from arcade.games.test.main import ArrowMask
    >>> list(ArrowMask)
    [<ArrowMask.up: 1>, <ArrowMask.right: 2>, <ArrowMask.down: 4>, <ArrowMask.left: 8>]
    >>> int(ArrowMask.up)
    1
    >>> int(ArrowMask.right)
    2
    """
    up = auto()
    right = auto()
    down = auto()
    left = auto()


class Game(plethoraAPI.Game):
    """ The small test game that implements the plethora API

    A small black square can be moved with the arrow keys but is constrained to the viewport. When
    the user attempts to close the window, interecept and return to the main window.
    """

    def __init__(self) -> None:
        """ :class:`Game` constructor """
        super().__init__(size=(200, 200), fps=40)  # call plethoraAPI.Game.__init__ to initialize :attr:`size` and :attr:`fps`
        self.arrows = 0b0000  # bitmask for arrow keys
        self.arrows_hidden = 0b0000  # bitmask for hiding opposite keys on key down while that key is down
        square_size = (25, 25)  # size of the square
        self.square_surf = pygame.Surface((square_size))  # square surface
        self.square_rect = pygame.Rect((10, 10, *square_size))  # square rect for position and bounds testing

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

    def move(self, x: int, y: int) -> None:
        """ move square by x, y with bounds checking

        Args:
            x: ``self.rect`` by x-pixels
            y: ``self.rect`` by y-pixels
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
        self.display.blit(self.square_surf, self.square_rect.topleft)  # redraw square
        return bool(arrows)  # return True if an arrow key is down; otherwise False
```


## Todo

1. **Do Group Project Iteration 1 before _Oct 20_**
    - See *Project guidelines ABET.pdf* for the deliverables
    - *Note*: each person must submit his/her *own* peer reviews
    - *Note*: each of us must contribute to the following:
        1. Progress report (*Progress Report Template.docx*)
        2. Software requirements and design (*IT Template.docx*)
        3. A 5-7 min video
        4. Source code for the project
    - We also need a demo for phase 1 (which will be incorporated in the video)
2. ~Set up UI properly and hand off to first game~
3. ~Meet to discuss how to interface with the app's API~
    - ~Discuss which method will be implemented (see [API Thoughts](#api-thoughts))~
    - ~Register game~
    - ~Implement callbacks~
    - ~Add *API* section documenting API~
4. ~Create a `setup.py` that handles dependencies and all of the setup stuff~
5. Implement individual games
    - Almost there! Keep up good work team! Good job so far!
6. Make logo(?)
