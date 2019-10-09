# mini-games

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
2. Set up UI properly and hand off to first game
3. Meet to discuss how to interface with the app's API
    - Discuss which method will be implemented (see [API Thoughts](./#api-thoughts))
    - Register game
    - Implement callbacks
    - Add *API* section documenting API
4. Create a `setup.py` that handles dependencies and all of the setup stuff
5. Implement individual games
6. Make logo(?)

## Development Setup

1. Install [Python](https://www.python.org/)
    - **Windows or Os X**
        1. Go to [python.org](https://www.python.org/)
        2. Hover over *Downloads*
        3. Click button **Python 3.x.x** under *Python Source* \*
    - **Os X + [Homebrew](https://brew.sh/)**
        1. `brew install python`
    - **Linux**
        1. Use package manager to install `python`
            - `apt-get install python`
            - `pacman -S python`
            - make sure `python` is python3 and not python2 if not on ubuntu or arch

\* Be sure to enable "Add Python 3.x to PATH" when installing on Windows

2. Install [Git](https://git-scm.com)
    - **Windows or Os X**
        1. Install from [git-scm.com](https://git-scm.com/downloads)
    - **Os X + [Homebrew](https://brew.sh/)**
        1. `brew install git`
    - **Linux**
        1. Use package manager to install `git`

3. Clone
    1. Open cmd.exe, powershell.exe, Terminal.app, or a terminal
    2. `cd Desktop/cen4930/` for example
    3. `git clone https://github.com/juliansweatt/mini-games.git`
    4. `cd mini-games`

4. Set Up Virtual Environment
    1. `python -m venv env`
        - This makes a new virtual environment at `./env/`
    2. Start Virtual Environment; you should to do this before you launch your game/main as well
        - **Windows**: `call env/Scripts/activate.bat`
        - **bash/zsh**: `source env/bin/activate`
        - **fish**: `source env/bin/activate.zsh`

5. Install Packages in VEnv:
    - Before you install things with pip, make sure that you have started the
      virtual environment.
    1. `pip install pygame`
    - It is recommended that you install `pytest`
    2. `pip install pytest`
        - Now you can run `pytest` after starting the VEnv
        - Check out [pytest](https://docs.pytest.org/en/latest/) for documentation
        - It is recommended to create a `test_{proj}.py` file rather than polluting the files
    - if you want static type checking, check out `mypy`
    3. `pip install mypy`
        - Now you can run `mypy foo.py` to validate the *foo.py*
        - Check out [mypy](http://www.mypy-lang.org/) for documentation
    4. Install any deps you want and need, but list them in the [Dependencies](./#dependencies) section!
        - Use the [pypi.org](https://pypi.org) if there is a wheel there
        - Otherwise, provide a URL to the project's installation documentation

6. Running the project
    - Be sure you have activated the Virtual Environment
    1. `python plethora.py`
    - You can also run your game directly if you have `if __name__ == "__main__:"` and call `pygame.init()` that code block and then pass the main display to the main of your game
    - Eg:
        1. `cd src/foo`
        2. `python foo_main.py`

## Dependencies

1. [pygame](https://pypi.org/project/pygame/)
    - Required for project since project based on pygame
2. [pytest](https://pypi.org/project/pytest/)
    - **testing only**
    - for unit testing
3. [mypy](https://pypi.org/project/mypy/)
    - **testing only**
    - for testing static types


## API Thoughts:

- __*Game*__ represents a game that a developer will make. It should reside in `./src/{game}/` where *{game}* is the name of the game.
- __*UI*__ represents the main UI and will likely be located at `src/app.py`

### Approach One

**Main _UI_ is the master**: it creates a surface for *Game* to render to and runs at *Game*'s FPS

Each *Game* has a `register(self)` function and returns a `(fps, size)` tuple (or it could be a dict).

Each *Game* has a `set_display(self, display)` function that is called after `register` to set the display that *UI* creates based on `size`

- *UI* creates surface of size `size` (and passes to `set_display`) and resizes main display
- *UI* will now run at `fps`
- *Game* must implement `onrender(self)` and `onevent(self, e)` that *UI*
  will call at `fps`

**Advantages**:

- Standardized menu and login/logout/settings buttons
- Easier for devs in some ways: don't have to worry about back button and quitting
    - When pressing *Back*, for instance, a pop-up/dialog confirmation
      box/button can pop up since UI controls this .. easy for dev
- More control in main UI

**Disadvantages**:

- Cannot support event-driven game
    - Probably not an issue
- Rendering UI relies on FPS of game
    - Can combat by allowing minimum FPS
- Harder for devs in some ways and ugly: have to remember to call `onrender()`
  and `onevent()` from UI passed during

### Approach Two

**Main _UI_ yields complete control to _Game_**: *UI* simply passes the main display to *Game* and blocks until *Game* is done

*Game* would have a `run(self, display)`, for example, which would be the mainloop for *Game*. It would handle all user input and rendering. When *Game* decides it is finished, it would return from `run(..)` and thereby yield control back to *UI*

**Advantages**

- Straightforward to make
- No extra code for devs
- Easy to interoperate a `if __name__ == "__main__"` (for testing) and *UI* call
  to `run(..)`

**Disadvantages**

- *UI* control over menu and other buttons completely gone
- *Game* running in complete isolation from *UI* while `run(..)` blocks

### Both Approaches

In order to properly implement the API, a `src/{game}/main.py` will probably need to be established. The *Game*'s `main.py` will probably need to create a class--for example, `class Game():`--and then set `__entry__ = Game` so that the *UI* will know which class to create an instance of and either call `run` or `register` and `onrender` and `onevent`.

For example (if *Approach One* is to be used), then an example `src/chess/main.py` might be:

```python
import pygame
from os.path import join as pathjoin

import chess

image_dir = pathlib.Path(__file__).with_name("images")

function loadPieceImg(piece_type, typ):
    return pygame.images.load(pathjoin(image_dir, "{}_{}".format(piece_type, typ)))

PIECES = {}
for piece_type in chess.PieceType:
    for color in chess.Color:
        piece = chess.Piece(piece_type, color)
        PIECES[piece] = loadPieceImg(piece_type, color)
    PIECES[piece_typ] = loadPieceImg(piece_type, "border")

class ChessGame():
    def __init__(self):
        self.dirty = True  # indicates if board needs to be redrawn
        self.board = chess.board()  # create new chess board

        self.display = None  # main display (retrieved from ``register()``)
        self.size = (500, 500)  # size of entire window (returned from ``register()``)
        self.fps = 20  # frames per second (returned from ``register()``)

        self.sq_cursor = chess.Square.E2  # cursor that can select squares
        self.sq_selected = None # indicates which square selected if any

        self.sq_size = (60, 60)  # square size when rendering board
        self.sq_surfs = tuple(  # dark and light square surfaces
            pygame.Surface(self.sq_size)
            for sq_color in sq_colors
        )
        # fill dark and light surfaces with dark and light (resp) colors
        self.sq_surfs[chess.DARK].fill((30, 30, 30))
        self.sq_surfs[chess.LIGHT].fill((225, 225, 225))

        self.cursor_padding = 3  # cursor border thickness
        self.cursor_surfs = (  # vertical and horizontal surfaces for cursor
            # top/bottom horizontal components
            pygame.Surface((self.sq_size[0] - 2 * self.cursor_padding, self.cursor_padding))
            # left/right vertical components
            pygame.Surface((self.cursor_padding, self.sq_size[1])),
        )
        # make cursor orange
        self.cursor_surfs[0].fill((252, 94, 50))
        self.cursor_surfs[1].fill((252, 94, 50))

    def register(self):
        # plethora API:
        #   - accept ``display`` as main display
        #   - return ``(fps, size)`` to UI
        return (self.fps, self.size)

    def set_display(self, display):
        self.display = display

    def draw_board(self):
        """ inefficient rendering for short illustration purposes

            - fill board with white
            - draw each square
            - if square has a piece, draw the piece
            - if piece is selected, draw piece border
        """
        # fill board with white
        self.display.fill((255, 255, 255))
        for sq_ind, square in enumerate(self.board.squares()):
            # find position of square
            pos = (
                10 + self.sq_size * (sq_ind // 8),
                10 + self.sq_size * (sq_ind % 8)
            )
            # draw square surface (dark or light)
            self.display.blit(self.sq_surfs[square.color], pos)
            # get piece at square or None if no piece
            piece = self.board.get_piece_at(sq_ind)
            if piece:
                # draw piece if not None
                self.display.blit(PIECES[piece], pos)
                if self.sq_selected == sq_ind:
                    # draw border since piece selected
                    self.display.blit(PIECES[piece.type], pos)

    def draw_cursor(self):
        """ draw the cursor to show selection """
        x, y = (
            10 + self.sq_size * (self.sq_cursor // 8),
            10 + self.sq_size * (self.sq_cursor % 8)
        )
        self.screen.blit(self.select_surfs[0], (
            x,
            y))
        self.screen.blit(self.select_surfs[0], (
            x + self.square_size[0] - self.cursor_padding,
            y))
        self.screen.blit(self.select_surfs[1], (
            x + self.cursor_padding,
            y))
        self.screen.blit(self.select_surfs[1], (
            x + self.cursor_padding,
            y + self.square_size[1] - self.cursor_padding))

    def onrender(self):
        """ API: called for each render """
        if self.dirty:
            self.draw_board()
            self.draw_cursor()

    def onevent(self, e):
        """ API: called for each event """
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                if self.cursor // 8 > 0:
                    self.cursor -= 8
                    self.dirty = True
            elif e.key == pygame.K_RIGHT:
                if self.cursor % 8 < 7:
                    self.cursor += 1
                    self.dirty = True
            elif e.key == pygame.K_DOWN:
                if self.cursor // 8 < 7:
                    self.cursor += 8
                    self.dirty = True
            elif e.key == pygame.K_LEFT:
                if self.curosr % 7 > 0:
                    self.cursor -= 1
                    self.dirty += True

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    game = ChessGame()
    display = pygame.display.set_mode((500, 500))  # arbitrary size
    # here UI will register the game after dynamically loading it
    # NOTE: UI would not pass main display as the surface for Game to render
    fps, size = game.register()
    # here UI would create a new surface
    # for illustration, just pass main display as surface
    display.set_mode(size)
    game.set_display(display)
    cont = True
    while cont:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                cont = False
                break
            # here UI would handle mouse events to menu and other buttons
            game.onevent(e)
        # here UI would handle drawing menu and other buttons if dirty
        game.onrender()
        # UI handles updating main display
        pygame.display.flip()
        # UI handles game tick
        clock.tick(fps)  # one game tick based on Game's registered FPS
        pygame.time.wait(fps)  # sleep process to prevent CPU hogging
```
