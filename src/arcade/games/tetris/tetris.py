
from arcade import plethoraAPI
from collections import namedtuple
from enum import Enum
from functools import partial
from math import floor
from random import randint
import pathlib
import pygame

# border width
BORDER = 10

# only seen on border
BACKGROUND_COLOR = (45, 45, 45)

# background for game
GAME_COLOR = (80, 80, 80)

# dimension for a square
SQUARE_DIM = 40

# padding (non-colored part) around square
# note that this is inner padding (ie, not margin)
SQUARE_PAD = 3

# playfield size is 10 x 20:
# https://tetris.fandom.com/wiki/Gameplay_overview
PLAY_SIZE = (10, 20)

# create height of display for multiple uses
DISPLAY_HEIGHT = BORDER * 2 + SQUARE_DIM * PLAY_SIZE[1]

# RIGHT padding for staging area on left
STAGE_MARGIN = 8

# color for confusingly, left-part of stage (background)
STAGE_BACKGROUND = (100, 100, 100)

# color for slender right-part of stage (margin)
STAGE_MARGIN_COLOR = (60, 60, 60)

# stage inner rect for blitting to STAGE_SURF; coordinates local to STAGE_SURF
STAGE_INNER_RECT = pygame.Rect(0, 0, 4 * SQUARE_DIM + 2 * BORDER, DISPLAY_HEIGHT)

# stage rect for use in onrender; coordinates global to Game#display.rect
STAGE_RECT = pygame.Rect(BORDER, BORDER, STAGE_INNER_RECT.width + STAGE_MARGIN, DISPLAY_HEIGHT - 2 * BORDER)

# the staging area; aka: the stage
STAGE_SURF = pygame.Surface(STAGE_RECT.size)

# size of entire display
DISPLAY_SIZE = (BORDER + SQUARE_DIM * PLAY_SIZE[0] + STAGE_RECT.width + STAGE_MARGIN,
        DISPLAY_HEIGHT)

# Rect for only the play area
PLAY_RECT = pygame.Rect(BORDER + STAGE_RECT.width, BORDER,
        DISPLAY_SIZE[0] - STAGE_RECT.width - 2 * BORDER, DISPLAY_HEIGHT - 2 * BORDER)

# use this to draw the play area
PLAY_SURF = pygame.Surface(PLAY_RECT.size)

# should run at 60 fps:
# https://tetris.fandom.com/wiki/TGM_legend#Frame
FPS = 60

# wait 30 frames before locking piece:
# https://tetris.fandom.com/wiki/Lock_delay
LOCK_DELAY = 30

# root directory of plethora
ROOT = pathlib.Path(plethoraAPI.__file__).parent

# frames to wait when counting down in beginning
BEGIN_COUNT_FRAMES = 60

# font to use for count in beginning
BIG_FONT = pygame.font.Font(str(ROOT/"fonts/exo/Exo-Regular.ttf"), 50)

# font for buttons in end game
SMALL_FONT = pygame.font.Font(str(ROOT/"fonts/exo/Exo-Regular.ttf"), 30)

# font for text in game
TINY_FONT = pygame.font.Font(str(ROOT/"fonts/exo/Exo-Regular.ttf"), 18)

# each number in the countdown
COUNTS = [
    BIG_FONT.render(str(i), True, (255, 255, 255))
    for i in range(1, 4)
]

TETROMINO_COLORS = {
    "I": (25, 225, 225),
    "O": (225, 225, 25),
    "T": (160, 25, 225),
    "S": (25, 225, 25),
    "Z": (225, 25, 25),
    "J": (25, 25, 225),
    "L": (225, 160, 25),
}

TETROMINOS = {
    "I": ["----",
          "----",
          "xxxx",
          "----"],

    "O": ["----",
          "-xx-",
          "-xx-",
          "----"],

    "T": ["----",
          "-x--",
          "xxx-",
          "----"],

    "S": ["----",
          "-xx-",
          "xx--",
          "----"],

    "Z": ["----",
          "xx--",
          "-xx-",
          "----"],

    "J": ["----",
          "x---",
          "xxx-",
          "----"],

    "L": ["----",
          "--x-",
          "xxx-",
          "----"],
}

def _make_tetromino_border(borderwidth, borderoff):
    """ semi-transparent border for tetrominos
    """
    surf = pygame.Surface((SQUARE_DIM, SQUARE_DIM))
    surf.set_colorkey((0, 0, 0))
    surf.fill((0, 0, 0))
    surf.set_alpha(0x7f)
    # vertical leaves
    ###################
    width = borderwidth - borderoff
    height = SQUARE_DIM - 2 * borderoff
    top = borderoff
    # left
    left = borderoff
    surf.fill((1, 1, 1), (left, top, width, height))
    # right
    left = SQUARE_DIM - borderwidth
    surf.fill((1, 1, 1), (left, top, width, height))
    # horizontal leaves
    ###################
    width = SQUARE_DIM - borderwidth * 2
    height = borderwidth
    left = borderwidth
    # top
    top = borderoff
    surf.fill((1, 1, 1), (left, top, width, height))
    # bottom
    top = SQUARE_DIM - borderwidth - borderoff
    surf.fill((1, 1, 1), (left, top, width, height))
    return surf
TETROMINO_BORDER = _make_tetromino_border(borderoff=1, borderwidth=4)

def get_tetromino_surf():
    surf = pygame.Surface((SQUARE_DIM * 4, SQUARE_DIM * 4))
    surf.set_colorkey((0, 0, 0))
    # color_rect = pygame.Rect(SQUARE_PAD, SQUARE_PAD,
    #         SQUARE_DIM - 2 * SQUARE_PAD, SQUARE_DIM - 2 * SQUARE_PAD)
    # surf.fill(TETROMINO_COLORS[name], color_rect)
    return surf

# used to keep track of left/right for key arrows
# this prevents updating every frame
MIN_KARROW_COUNT = -10  # must be <0
MAX_KARROW_COUNT = 2  # must be > 0
KARROW_INC = 1  # must be >0

BoundSq = namedtuple("BoundSq", "left top right bottom")

def have_collision(matrix1, matrix2):
    for l1, l2 in zip(matrix1, matrix2):
        for c1, c2 in zip(l1, l2):
            if c1 != "-" and c2 != "-":
                return True
    return False


class TetrominoType(Enum):
    # https://tetris.fandom.com/wiki/Tetromino
    I = 1
    O = 2
    T = 3
    S = 4
    Z = 5
    J = 6
    L = 7

    def __init__(self, value):
        self.mask = TETROMINOS[self.name]
        self.color = TETROMINO_COLORS[self.name]


class Tetromino:
    def __init__(self, ttype, rotation=0):
        """ A tetronimo piece

            :param TetrominoType ttype: TetrominoType
            :param int rotation: rotation in terms of pi/2 radian increments (1 is pi/2, 2 is pi, etc)
        """
        self.ttype = ttype
        self.name = ttype.name
        self.color = ttype.color
        self.mask = ttype.mask.copy()
        self.surf = get_tetromino_surf()
        self._draw_surf()

    def rrotate(self, times=1):
        """ right rotate: used when user presses Up

            :param int times: number of times to rotate (default: 1)
        """
        for _ in range(times % 4):
            self.mask = list(''.join(rl) for rl in zip(*reversed(self.mask)))
            self._draw_surf()

    def lrotate(self, times=1):
        """ left rotate: if right rotate fails, this is used to reverse it

            :param int times: number of times to rotate (default: 1)
        """
        for _ in range(times % 4):
            self.mask = list(reversed(list(''.join(rl) for rl in zip(*self.mask))))
            self._draw_surf()

    def _draw_surf(self):
        """ private function used to draw/redraw to its surface
        """
        self.surf.fill((0, 0, 0))
        rect = pygame.Rect(0, 0, SQUARE_DIM, SQUARE_DIM)
        left, top = 5, 5
        right, bottom = 0, 0
        for y, line in enumerate(self.mask):
            rect.left = 0
            for x, char in enumerate(line):
                if char == "x":
                    self.surf.fill(self.color, rect)
                    self.surf.blit(TETROMINO_BORDER, rect)
                    if x < left:
                        left = x
                    if x > right:
                        right = x
                    if y < top:
                        top = y
                    if y > bottom:
                        bottom = y
                    bottom = y
                rect.left += SQUARE_DIM
            rect.top += SQUARE_DIM
        self.boundsq = BoundSq(left, top, right, bottom)


# arrow masks for up, right, down, left (similar to enum.IntFlag like dylan used in testgame)
ARROW_MASKS = M_UP, M_RIGHT, M_DOWN, M_LEFT = 0b0001, 0b0010, 0b0100, 0b1000


class Game(plethoraAPI.Game):
    """ Tetris game for plethora API
    """
    def __init__(self):
        super().__init__(size=DISPLAY_SIZE, fps=FPS)
        self.start()

    def start(self):
        self.arrows = 0b0000   # bitmask for arrow keys {up,right,down,left}
        self.lr_hide = 0b0000  # mask for left/right
        self.karrow_count = 0  # frame count for left/right arrows
        self.locked = [None] * (PLAY_SIZE[0] * PLAY_SIZE[1])  # all locked colors
        self.begin_count = len(COUNTS) - 1  # countdown from 3 in beginning
        self.begin_count_tick = 0 # wait BEGIN_COUNT_FRAMES frames
        self.state = 0            # {0,1,3} = {begin,play,end}
        self.curt = None          # current tetromino
        self.curt_rot = 0         # current tet rot: {0,1,2,3}={0,pi/2,pi,3*pi/2}rad={0,90,180,360}deg
        self.curt_y = 0           # current tet y [0, PLAY_SIZE[1]]
        self.curt_x = 0           # current tet x [-2, PLAY_SIZE[0] + 2]
        self.score = 0            # tetris score
        self.G = 1/64             # gravity
        self.dropG = 1/2          # hard-drop gravity
        self.hardG = 20           # instant drop
        self.filled = list(       # all filled colors
                ['-'] * PLAY_SIZE[0]
                for _ in range(PLAY_SIZE[1]))
        self.space = False        # hard (instant) drop)
        self.queue = []           # queue for next pieces
        self.linesCleared = 0     # how many lines are cleared (linesCleared//10 == level)
        self.score = 0            # score
        # text
        self.linesClearedText = TINY_FONT.render("Lines Cleared:", True, (255, 255, 255))
        self.linesClearedWidth = self.linesClearedText.get_width()
        self.scoreText = TINY_FONT.render("Score:", True, (255, 255, 255))
        self.scoreWidth = self.scoreText.get_width()
        self.levelText = TINY_FONT.render("Level:", True, (255, 255, 255))
        self.levelWidth = self.levelText.get_width()
        # buttons
        self.again_btn = plethoraAPI.UIButton(
            x=0,
            y=PLAY_RECT.centery + 20,
            text="Play Again",
            callback=self._play_again_click,
            font=SMALL_FONT,
            fontColor=(0, 0, 0),
            background=(255, 255, 255))
        self.again_btn.rect.right = PLAY_RECT.centerx - 20
        self.quit_btn = plethoraAPI.UIButton(
            x=PLAY_RECT.centerx + 20,
            y=PLAY_RECT.centery + 20,
            text="Quit",
            callback=self._quit_click,
            font=SMALL_FONT,
            fontColor=(0, 0, 0),
            background=(255, 255, 255))
        # fill staging area so it is not black for intro
        STAGE_SURF.fill(GAME_COLOR)


    def _has_collision(self, y=None):
        left = max(0, self.curt_x)
        right = self.curt_x + 4
        mask = self.curt.mask
        if self.curt_x < 0:
            mask = list(line[-self.curt_x:] for line in mask)
        if y is None:
            y = floor(self.curt_y)
        if y < 0:
            mask = mask[-y:]
            filled = self.filled[-y:y+4]
        else:
            filled = self.filled[y:y+4]
        return have_collision(mask, list(line[left:right] for line in filled))

    def onevent(self, event):
        if event.type == pygame.QUIT:
            self.onexit()
        if self.state == 0:
            return False
        elif self.state == 1:
            # modeled after testgame a bit:
            # https://github.com/juliansweatt/mini-games/blob/develop/src/arcade/games/testgame/testgame.py#L79
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.arrows |= M_UP
                    self.curt.rrotate()
                    xsav = self.curt_x
                    ysav = self.curt_y
                    while self.curt_x + self.curt.boundsq.left < 0:
                        self.curt_x += 1
                    while self.curt_x + self.curt.boundsq.right >= PLAY_SIZE[0]:
                        self.curt_x -= 1
                    y = int(self.curt_y)
                    below_map = y + self.curt.boundsq.bottom >= PLAY_SIZE[1]
                    while below_map:
                        self.curt_y -= 1
                        y = int(self.curt_y)
                        below_map = y + self.curt.boundsq.bottom >= PLAY_SIZE[1]
                    collision = self._has_collision()
                    if collision and self.curt_x + self.curt.boundsq.left > 0:
                        # if possible, move one left and check if there is still a collision
                        self.curt_x -= 1
                        collision = self._has_collision()
                        if collision:
                            # set curt_x back for next collision test
                            self.curt_x += 1
                    if collision and self.curt_x - self.curt.boundsq.right < PLAY_SIZE[0] - 1:
                        # if possible, move one right and check if there is still a collision
                        self.curt_x += 1
                        collision = self._has_collision()
                    if collision:
                        # unable to find orientation suitable for this rotation
                        self.curt.lrotate()
                        self.curt_x = xsav
                        self.curt_y = ysav
                elif event.key == pygame.K_DOWN:
                    self.arrows |= M_DOWN
                elif event.key == pygame.K_RIGHT:
                    self.arrows |= M_RIGHT
                    self.lr_hide |= M_LEFT
                    self.lr_hide &= ~M_RIGHT
                    self.karrow_count = MIN_KARROW_COUNT
                elif event.key == pygame.K_LEFT:
                    self.arrows |= M_LEFT
                    self.lr_hide |= M_RIGHT
                    self.lr_hide &= ~M_LEFT
                    self.karrow_count = MIN_KARROW_COUNT
                elif event.key == pygame.K_SPACE:
                    self.space = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.arrows &= ~M_UP
                elif event.key == pygame.K_RIGHT:
                    self.arrows &= ~M_RIGHT
                    self.lr_hide &= ~(M_LEFT | M_RIGHT)
                elif event.key == pygame.K_DOWN:
                    self.arrows &= ~M_DOWN
                elif event.key == pygame.K_LEFT:
                    self.arrows &= ~M_LEFT
                    self.lr_hide &= ~(M_LEFT | M_RIGHT)
            return False # during game, only render on each frame (tetris is fps-driven game)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # modelled after API with help of Dylan
                pos = event.pos
                for btn in [self.again_btn, self.quit_btn]:
                    if btn.rect.collidepoint(pos):
                        btn.onclick()
                        break
            return True

    def _new_tetronimo(self):
        if not self.queue:
            self.queue = [Tetromino(TetrominoType(randint(1, 7))) for i in range(3)]
        self.queue.append(Tetromino(TetrominoType(randint(1, 7))))
        self.curt = self.queue.pop(0)
        self.curt_y = -self.curt.boundsq.top
        self.curt_x = 3

        if self._has_collision():
            # game over
            self.curt_y -= 1
            while self._has_collision():
                self.curt_y -= 1
            self.state += 1
            self._render_surfs()
            return

    def _delete_lines_from(self, fromy):
        linesCleared = 0
        for y, line in enumerate(self.filled[fromy:], start=fromy):
            self.display.fill((255, 0, 0), pygame.Rect(PLAY_RECT.left, PLAY_RECT.top + y * SQUARE_DIM, PLAY_RECT.width, 10))
            if "-" in line:
                if y >= fromy + 4:
                    break
            else:
                # line needs to be cleared
                for yprime, line in reversed(list(enumerate(self.filled[:y]))):
                    self.filled[yprime+1] = self.filled[yprime]
                self.filled[0] = ['-'] * PLAY_SIZE[0]
                linesCleared += 1
        return linesCleared

    def onrender(self):
        if self.state == 0:
            self._render_intro()
        elif self.state == 1:
            self._render_game()
        else:
            self._render_end()
            return False
        return True

    def _render_intro(self):
        if self.begin_count_tick == 0:
            self.display.fill(BACKGROUND_COLOR)
            self.display.blit(STAGE_SURF, STAGE_RECT)
            self.display.fill(GAME_COLOR, PLAY_RECT)
            count = COUNTS[self.begin_count]
            center = (self.rect.centerx - count.get_width() // 2 - 1,
                    self.rect.centery - count.get_height() // 2 - 1)
            self.display.blit(count, center)
        self.begin_count_tick += 1
        if self.begin_count_tick > BEGIN_COUNT_FRAMES:
            self.begin_count -= 1
            self.begin_count_tick = 0
        if self.begin_count < 0:
            # begin game
            self.state += 1
            self._new_tetronimo()

    def _move_left(self):
        self.curt_x -= 1
        if self._has_collision():
            self.curt_x += 1

    def _move_right(self):
        self.curt_x += 1
        if self._has_collision():
            self.curt_x -= 1

    def _render_game(self):
        arrows = self.arrows & ~self.lr_hide  # get unmasked arrows
        softDrop = bool(arrows & M_DOWN)  # True if soft dropping
        hardDrop = False
        if self.space:
            # user pressing space; hard drop (20G)
            self.space = False
            hardDrop = True
            drop = self.hardG
        else:
            # soft drop or normal drop
            drop = self.dropG if softDrop else self.G
        cury = floor(self.curt_y)
        nexty = floor(self.curt_y + drop)

        if arrows & M_LEFT:
            # user holding left and not masked
            if self.karrow_count > MAX_KARROW_COUNT or self.karrow_count == MIN_KARROW_COUNT:
                if self.curt_x + self.curt.boundsq.left > 0:
                    self._move_left()
                if self.karrow_count > 0:
                    self.karrow_count = 0
            self.karrow_count += 1
        if arrows & M_RIGHT:
            # user holding right and not masked
            if self.karrow_count > MAX_KARROW_COUNT or self.karrow_count == MIN_KARROW_COUNT:
                if self.curt_x + self.curt.boundsq.right < PLAY_SIZE[0] - 1:
                    self._move_right()
                if self.karrow_count > 0:
                    self.karrow_count = 0
            self.karrow_count += 1

        if nexty > cury:
            # piece has moved one or more pieces down
            for y in range(cury, nexty + 1):
                # iterate over each square from top to bottom to test if it's a valid move
                below_map = y + self.curt.boundsq.bottom >= PLAY_SIZE[1]
                collision = self._has_collision(y)
                if below_map or collision:
                    # piece is now unable to here; lock it on previous square
                    top = y - 1
                    name = self.curt.name
                    # lock piece by populating filled and calling _new_tetronimo
                    for y, line in enumerate(self.curt.mask, start=top):
                        for x, char in enumerate(line, start=self.curt_x):
                            if char == "-":
                                continue
                            self.filled[y][x] = name
                    linesCleared = self._delete_lines_from(top)  # also delete all full lines
                    self.linesCleared += linesCleared
                    # original nintendo scoring: https://tetris.fandom.com/wiki/Scoring
                    level = self.linesCleared // 10
                    self.score += [40, 100, 300, 1200][linesCleared - 1] * (level + 1)
                    self._new_tetronimo()
                    self._render_surfs()
                    # if lines cleared; increase speed slightly
                    self.G += 0.002 * linesCleared
                    return
                if softDrop:
                    self.score += 1
                if hardDrop:
                    self.score += 2

        # increase current tetromino y and render surfaces
        self.curt_y += drop
        self._render_surfs()

    def _render_surfs(self):
        self.display.fill(BACKGROUND_COLOR)
        # set up stage area
        STAGE_SURF.fill(STAGE_MARGIN_COLOR)
        STAGE_SURF.fill(STAGE_BACKGROUND, STAGE_INNER_RECT)
        for y, t in enumerate(self.queue):
            STAGE_SURF.blit(t.surf, (BORDER + (3 - t.boundsq.right) * SQUARE_DIM, y * (SQUARE_DIM * 4 + BORDER)))
        x = 2
        # lines cleared
        y = SQUARE_DIM * 12 + 40
        score = TINY_FONT.render(str(self.score), True, (255, 255, 255))
        STAGE_SURF.blit(self.scoreText, (x, y))
        STAGE_SURF.blit(score, (x + self.scoreWidth + 2, y))
        # score
        y += 30
        linesCleared = TINY_FONT.render(str(self.linesCleared), True, (255, 255, 255))
        STAGE_SURF.blit(self.linesClearedText, (x, y))
        STAGE_SURF.blit(linesCleared, (x + self.linesClearedWidth + 2, y))
        # level
        y += 30
        level = TINY_FONT.render(str(self.linesCleared // 10), True, (255, 255, 255))
        STAGE_SURF.blit(self.levelText, (x, y))
        STAGE_SURF.blit(level, (x + self.levelWidth + 2, y))
        self.display.blit(STAGE_SURF, STAGE_RECT)
        # setup play area
        PLAY_SURF.fill(GAME_COLOR)
        x = self.curt_x * SQUARE_DIM
        y = floor(self.curt_y) * SQUARE_DIM
        PLAY_SURF.blit(self.curt.surf, (x, y))
        sqrect = pygame.Rect(0, 0, SQUARE_DIM, SQUARE_DIM)
        for y, line in enumerate(self.filled):
            for x, char in enumerate(line):
                if char == "-":
                    continue
                sqrect.topleft = x * SQUARE_DIM, y * SQUARE_DIM
                PLAY_SURF.fill(TETROMINO_COLORS[char], sqrect)
                PLAY_SURF.blit(TETROMINO_BORDER, sqrect)
        self.display.blit(PLAY_SURF, PLAY_RECT)


    def _render_end(self):
        lose_txt = BIG_FONT.render("game over", True, (255, 255, 255))
        center = [PLAY_RECT.centerx - lose_txt.get_width() // 2,
                self.rect.centery - lose_txt.get_height()]
        # create shadow :)
        lose_txt_bg = BIG_FONT.render("game over", True, (5, 5, 5))
        center[0] -= 2
        center[1] += 2
        self.display.blit(lose_txt_bg, center)
        # game over text
        center[0] += 2
        center[1] -= 2
        self.display.blit(lose_txt, center)
        self.display.blit(self.again_btn.surface, self.again_btn.rect.topleft)
        self.display.blit(self.quit_btn.surface, self.quit_btn.rect.topleft)
        return False

    def _play_again_click(self):
        self.start()

    def _quit_click(self):
        self.onexit()

