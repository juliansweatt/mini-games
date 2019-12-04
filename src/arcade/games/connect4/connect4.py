import pygame

from arcade import plethoraAPI

# Predefined Colors for the UI
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
GREY = (160,160,160)

# Connect 4 Board Configuration
NUM_CELLS_VERTICAL = 6
NUM_CELLS_HORIZONTAL = 7
WIN_SERIES_LENGTH = 4

# UI Anchor Points & Dimensions
CELL_RADIUS = 10
MARGIN = 5
GAME_HEIGHT = (CELL_RADIUS * 2 + MARGIN) * NUM_CELLS_VERTICAL + MARGIN
GAME_WIDTH = (CELL_RADIUS * 2 + MARGIN) * NUM_CELLS_HORIZONTAL + MARGIN
SCOREBOARD_HEIGHT = (MARGIN * 3)
WINDOW_HEIGHT = GAME_HEIGHT + SCOREBOARD_HEIGHT
SIZE_MULTIPLIER = 4

class Grid:
    """Class Grid used for Connect 4 matrix and associated logic.

    """
    def __init__(self, width, height, neutral_color, p1_color, p2_color):
        """Grid constructor.

        :param int width: The number of cells used in the grid horizontally.
        :param int height: The number of cells used in the grid vertically.
        :param (int, int, int) neutral_color: The neutral color for the grid used to represent unclaimed cells, represented in RGB.
        :param (int, int, int) p1_color: The player 1 color for the grid used to represent cells claimed by player 1, represented in RGB.
        :param (int, int, int) p2_color: The player 2 color for the grid used to represent cells claimed by player 2, represented in RGB.
        :rtype: None
        """
        self.neutral_color = neutral_color
        self.p1_color = p1_color
        self.p2_color = p2_color
        self.height = height
        self.width = width
        self.reset()
    
    def reset(self):
        """Reset grid for a new game (clear all cells).

        :rtype: None
        """
        self.grid = []
        self.victor = 0
        for col in range(self.width):
            self.grid.append([])
            for cell in range(self.height):
                self.grid[col].append(0)

    def getPlayerColor(self, playerNumber):
        """Get the assigned color of a player, searched by player number.

        :param playerNumber: The number of the player.
        :type playerNumber: 1 <= int <= 2
        :return: The color of the player, represented in RGB.
        :rtype: (int, int, int)
        """
        if playerNumber == 1:
            return self.p1_color
        elif playerNumber == 2:
            return self.p2_color
        else:
            return self.neutral_color

    def getCellColor(self, x, y):
        """Get the appropriate color for a cell in the grid.

        :param x: The horizontal index of the grid cell being searched.
        :type playerNumber: 0 <= int <= self.width
        :param y: The vertical index of the grid cell being searched.
        :type playerNumber: 0 <= int <= self.height
        :return: The appropriate color of the cell, represented in RGB.
        :rtype: (int, int, int)
        """
        if x < self.width and x > -1 and y > -1 and y < self.height:
            cell = self.grid[x][y]
            return self.getPlayerColor(cell)
    
    def playColumn(self, playerNumber, col):
        """Attempt a play by a particular player on a grid column. 

        Attempts a play on the grid by a certain player, at a column. The play will be made at the
        highest neutral cell in the column. 

        :param playerNumber: The player number of the player making the play.
        :type playerNumber: 1 <= int <= 2
        :param col: The column to attempt a play on.
        :type col: 0 <= int <= self.width
        :return: Returns True if the play could be made, else False (invalid or impossible).
        :rtype: bool
        """
        if self.victor == 0:
            setIndex = -1
            for index, cell in enumerate(self.grid[col]):
                if cell == 0:
                    setIndex = index
                    break
            
            if setIndex > -1:
                self.grid[col][setIndex] = playerNumber
                self.victor = self.checkVictor(col, setIndex)
                return True
            else:
                return False

    def checkVictor(self, x, y):
        """Check for a victory condition on the grid.

        Checks for a victory condition on the grid at a particular cell. This should be run any time
        a change is made to the grid. Victory conditions model the Connect 4 board game, checking for a series of 
        WIN_SERIES_LENGTH by the same player in any direction.

        :param x: The horizontal index of the grid cell where a change has been made..
        :type playerNumber: 0 <= int <= self.width
        :param y: The vertical index of the grid cell where a change has been made.
        :type playerNumber: 0 <= int <= self.height
        :return: If a victor is found, return player number, else 0. Returns -1 if the grid is completely full
        and no victor was found.
        :rtype: -1 <= int <= 2
        """
        player = self.grid[x][y]

        # Vertical (|)
        searching_up = True
        searching_down = True
        sequence_length = 1
        for i in range(1, WIN_SERIES_LENGTH):
            if searching_up:
                if y + i < len(self.grid[x]):
                    if self.grid[x][y+i] == player:
                        sequence_length += 1
                        if sequence_length >= WIN_SERIES_LENGTH:
                            return player 
                    else:
                        searching_up = False
                else:
                    searching_up = False
            if searching_down:
                if y - i > -1:
                    if self.grid[x][y-i] == player:
                        sequence_length += 1
                        if sequence_length >= WIN_SERIES_LENGTH:
                            return player 
                    else:
                        searching_down = False
                else:
                    searching_down = False

        # Horizontal (-)
        searching_left = True
        searching_right = True
        sequence_length = 1
        for i in range(1, WIN_SERIES_LENGTH):
            if searching_right:
                if x + i < len(self.grid):
                    if self.grid[x+i][y] == player:
                        sequence_length += 1
                        if sequence_length >= WIN_SERIES_LENGTH:
                            return player 
                    else:
                        searching_right = False
                else:
                    searching_right = False
            if searching_left:
                if x - i > -1:
                    if self.grid[x-i][y] == player:
                        sequence_length += 1
                        if sequence_length >= WIN_SERIES_LENGTH:
                            return player 
                    else:
                        searching_left = False
                else:
                    searching_left = False

        # Diagonal (/)
        searching_left = True
        searching_right = True
        sequence_length = 1
        for i in range(1, WIN_SERIES_LENGTH):
            if searching_right:
                if x + i < len(self.grid) and y + i < len(self.grid[x]):
                    if self.grid[x+i][y+i] == player:
                        sequence_length += 1
                        if sequence_length >= WIN_SERIES_LENGTH:
                            return player 
                    else:
                        searching_right = False
                else:
                    searching_right = False
            if searching_left:
                if x - i > -1 and y - i > -1:
                    if self.grid[x-i][y-i] == player:
                        sequence_length += 1
                        if sequence_length >= WIN_SERIES_LENGTH:
                            return player 
                    else:
                        searching_left = False
                else:
                    searching_left = False
        
        # Diagonal (\)
        searching_left = True
        searching_right = True
        sequence_length = 1
        for i in range(1, WIN_SERIES_LENGTH):
            if searching_right:
                if x + i < len(self.grid) and y - i > -1:
                    if self.grid[x+i][y-i] == player:
                        sequence_length += 1
                        if sequence_length >= WIN_SERIES_LENGTH:
                            return player 
                    else:
                        searching_right = False
                else:
                    searching_right = False
            if searching_left:
                if x - i > -1 and y + i < len(self.grid[x]):
                    if self.grid[x-i][y+i] == player:
                        sequence_length += 1
                        if sequence_length >= WIN_SERIES_LENGTH:
                            return player 
                    else:
                        searching_left = False
                else:
                    searching_left = False
        
        # Grid Full Check
        gridFull = False
        if y == NUM_CELLS_VERTICAL - 1:
            gridFull = True
            for col in self.grid:
                if col[NUM_CELLS_VERTICAL - 1] == 0:
                    gridFull = False
                    break
        
        if gridFull:
            return -1

        return 0

class Connect4(plethoraAPI.Game):
    """Class Connect4 represents the Connect 4 game.

    The Connect4 class contains primarily UI and pygame implementations. Depends upon the
    Grid class as a back-end.
    """
    def __init__(self, neutral_color=WHITE, p1_color=RED, p2_color=GREEN):
        """Connect4 constructor.

        :param (:obj:`(int,int,int)`, optional) neutral_color: The color used to represent a neutral cell in the game (RBG).
        :param (:obj:`(int,int,int)`, optional) p1_color: The color used to represent a cell owned by player 1 in the game (RBG).
        :param (:obj:`(int,int,int)`, optional) p2_color: The color used to represent a cell owned by player 2 in the game (RBG).
        :rtype: None
        """
        self.expandWindow(SIZE_MULTIPLIER)
        super().__init__(size=(GAME_WIDTH, WINDOW_HEIGHT), fps=60)
        self.score = [0,0]
        self.currentPlayer = 1
        self.activeGame = True
        self.captive = False
        self.captiveKeyResponse = True
        self.grid = Grid(NUM_CELLS_HORIZONTAL, NUM_CELLS_VERTICAL, neutral_color, p1_color, p2_color)
        self.targetedCol = -1
        self.columnMasks = self.buildColumns()

    def buildColumns(self):
        """Form column definitions around the cells.

        :return: Rectangle definitions around the cell columns.
        :rtype: [int]
        """
        columns = []
        for i in range(NUM_CELLS_HORIZONTAL):
            columns.append(pygame.Rect((MARGIN+CELL_RADIUS*2) * i + (MARGIN/2), 0, CELL_RADIUS*2 + int(MARGIN), GAME_HEIGHT))
        return columns

    @staticmethod
    def expandWindow(multiplier=2):
        """Expand the game window.

        :param (:obj:`int`, optional) multiplier: The factor by which to expand or multiply the size of the game.
        :rtype: None
        """
        global CELL_RADIUS
        global MARGIN
        global GAME_HEIGHT
        global GAME_WIDTH
        global WINDOW_HEIGHT
        global SCOREBOARD_HEIGHT

        CELL_RADIUS *= multiplier
        MARGIN *= multiplier
        GAME_HEIGHT *= multiplier
        WINDOW_HEIGHT *= multiplier
        GAME_WIDTH *= multiplier
        SCOREBOARD_HEIGHT *= multiplier

    @staticmethod
    def resetWindow(n=2):
        """Reduce the game window.

        :param (:obj:`int`, optional) n: The factor by which to reduce or shrink the size of the game.
        :rtype: None
        """
        global CELL_RADIUS
        global MARGIN
        global GAME_HEIGHT
        global GAME_WIDTH
        global WINDOW_HEIGHT
        global SCOREBOARD_HEIGHT

        CELL_RADIUS = int(CELL_RADIUS/n)
        MARGIN = int(MARGIN/n)
        GAME_HEIGHT = int(GAME_HEIGHT/n)
        WINDOW_HEIGHT = int(WINDOW_HEIGHT/n)
        GAME_WIDTH = int(GAME_WIDTH/n)
        SCOREBOARD_HEIGHT = int(SCOREBOARD_HEIGHT/n)

    @staticmethod
    def brightenRGB(color):
        """Brighten an RGB color code.

        :param (int, int, int) color: The color to brighten
        :return: Brightened RGB color code
        :rtype: (int, int, int)
        """
        red = color[0]
        blue = color[1]
        green = color[2]

        if red == blue == green:
            red += 50
            return (red, red, red)
        else:
            maximumRGB = max(color)

            if red == maximumRGB:
                blue += 100
                green += 100
            elif green == maximumRGB:
                red += 100
                blue += 100
            elif blue == maximumRGB:
                red += 100
                green += 100
            
        if red > 256:
            red = 255
        if green > 256:
            green = 255
        if blue > 256:
            blue = 255

        return (red, blue, green)

    def drawGrid(self):
        """Draw the Connect 4 grid to the UI.

        :rtype: None
        """
        # Background
        self.window.fill(BLACK)

        # Selection Highlighting
        if(self.targetedCol > -1):
            highlightColor = self.brightenRGB(GREY)
            if self.grid.grid[self.targetedCol][NUM_CELLS_VERTICAL-1] == 0:
                # Playable Column
                highlightColor = self.brightenRGB(self.grid.getPlayerColor(self.currentPlayer))

            pygame.draw.rect(self.window, highlightColor, self.columnMasks[self.targetedCol])

        # Cells/Dots
        for col in range(self.grid.width):
            for row in range(self.grid.height):
                x = (MARGIN+CELL_RADIUS*2) * col + CELL_RADIUS + MARGIN
                y = (MARGIN+CELL_RADIUS*2) * row + CELL_RADIUS + MARGIN
                pygame.draw.circle(self.window, self.grid.getCellColor(col, self.grid.height-1-row), (x, y), CELL_RADIUS)
                pygame.draw.circle(self.window, self.brightenRGB(BLACK), (x, y), CELL_RADIUS+int(MARGIN/4), int(MARGIN/2))

    def drawScoreBoard(self):
        """Draw the scoreboard to the bottom of the UI.

        :rtype: None
        """
        # Board
        background = pygame.draw.rect(self.window, GREY, (0, GAME_HEIGHT, GAME_WIDTH, SCOREBOARD_HEIGHT))

        # Status Circle
        status_circle = pygame.draw.circle(self.window, self.grid.getPlayerColor(self.currentPlayer), (int(SCOREBOARD_HEIGHT/2), background.center[1]), int(SCOREBOARD_HEIGHT/2)-int(MARGIN/3))
        pygame.draw.circle(self.window, BLACK, (int(SCOREBOARD_HEIGHT/2), background.center[1]), int(SCOREBOARD_HEIGHT/2)-int(MARGIN/4), int(MARGIN/4))

        # Player Name
        font_player = pygame.font.Font('freesansbold.ttf', 8*SIZE_MULTIPLIER)
        surface_player = font_player.render('Player ' + str(self.currentPlayer), False, BLACK)
        rect_player = surface_player.get_rect()
        rect_player.midleft = (status_circle.right + int(MARGIN/2), status_circle.center[1]+int(MARGIN/2))
        self.window.blit(surface_player, rect_player)

        # Current Player Header
        font_cp = pygame.font.Font('freesansbold.ttf', 3*SIZE_MULTIPLIER)
        surface_cp = font_cp.render('Current Player:', True, BLACK)
        rect_cp = surface_cp.get_rect()
        rect_cp.bottomleft = rect_player.topleft
        self.window.blit(surface_cp, rect_cp)

        # Score Header
        font_score_header = pygame.font.Font('freesansbold.ttf', 3*SIZE_MULTIPLIER)
        surface_score_header = font_score_header.render('Score:', True, BLACK)
        rect_score_header = surface_score_header.get_rect()
        rect_score_header.topright = (GAME_WIDTH-(MARGIN*2), GAME_HEIGHT+int(MARGIN/3))
        self.window.blit(surface_score_header, rect_score_header)

        # Score P1
        font_score_p1 = pygame.font.Font('freesansbold.ttf', 3*SIZE_MULTIPLIER)
        surface_score_p1 = font_score_p1.render('Player 1: ' + str(self.getScore(1)), True, BLACK)
        rect_score_p1 = surface_score_p1.get_rect()
        rect_score_p1.center = (rect_score_header.center[0], rect_score_header.center[1]+ int(SCOREBOARD_HEIGHT/4))
        self.window.blit(surface_score_p1, rect_score_p1)

        # Score P2
        font_score_p2 = pygame.font.Font('freesansbold.ttf', 3*SIZE_MULTIPLIER)
        surface_score_p2 = font_score_p2.render('Player 2: ' + str(self.getScore(2)), True, BLACK)
        rect_score_p2 = surface_score_p2.get_rect()
        rect_score_p2.center = (rect_score_header.center[0], rect_score_header.center[1]+ int((SCOREBOARD_HEIGHT/4)*2))
        self.window.blit(surface_score_p2, rect_score_p2)

    def onrender(self):
        """Render implementation for Plethora.

        :return: Returns True to repeat rendering or False to render once.
        :rtype: bool
        """
        self.window = self.display
        if not self.captive:
            self.drawGrid()
            self.drawScoreBoard()
        return False
    
    def onevent(self, event):
        """Event handler for Plethora.

        :return: Returns True to render or False to not render.
        :rtype: bool
        """
        if event.type == pygame.QUIT:
            self.onexit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = event.pos
            if(event.button == 1):
                if self.activeGame:
                    for columnNumber, colMask in enumerate(self.columnMasks):
                        if colMask.collidepoint(mousePos):
                            self.attemptMove(columnNumber)
                            return True
                elif not self.activeGame and self.captive:
                    if self.confirm_button.collidepoint(mousePos):
                        # Play Again
                        self.reset()
                        self.captive = False
                    elif self.decline_button.collidepoint(mousePos):
                        # Exit Game
                        self.onexit()
                        self.captive = False
                    return True
        elif event.type == pygame.MOUSEMOTION:
            mousePos = event.pos
            for columnNumber, colMask in enumerate(self.columnMasks):
                if colMask.collidepoint(mousePos):
                    self.targetedCol = columnNumber
                    return True
        elif event.type == pygame.KEYDOWN:
            if self.activeGame:
                if event.key == pygame.K_LEFT:
                    self.targetLeft()
                elif event.key == pygame.K_RIGHT:
                    self.targetRight()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if self.targetedCol > -1:
                        self.attemptMove(self.targetedCol)
                return True
            else:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.captiveKeyResponse = not self.captiveKeyResponse
                    self.refreshCaptiveButtons("Play Again", "Exit", MARGIN * 7, MARGIN * 2)
                    return True
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if self.captiveKeyResponse:
                        self.reset()
                        self.captive = False
                    else:
                        self.onexit()
                        self.captive = False
                    return True
        return False
    
    def attemptMove(self, column):
        """Attempt to make a play, then handle next game stage.

        Attempts a play at a column. If the play is valid, either the game will end or
        the other player will be given a turn. 

        :param column: The column to attempt a play at, for the current player.
        :type column: 0 <= int <= self.width
        :return: Returns True on valid move, or False on invalid move.
        :rtype: bool
        """
        if self.grid.playColumn(self.currentPlayer, column):
            # Move Successful
            if self.grid.victor == 0:
                if self.currentPlayer == 1:
                    self.currentPlayer = 2
                elif self.currentPlayer == 2:
                    self.currentPlayer = 1
            else:
                self.endGame()
            return True
        else:
            # Invalid Move
            return False

    def targetLeft(self):
        """Shift the target column left.

        :rtype: None
        """
        if self.targetedCol > -1:
            newTarget = self.targetedCol - 1
            if newTarget > -1:
                self.targetedCol = newTarget
            else:
                self.targetedCol = NUM_CELLS_HORIZONTAL-1
        else:
            self.targetedCol = 0
    
    def targetRight(self):
        """Shift the target column right.

        :rtype: None
        """
        if self.targetedCol > -1:
            newTarget = self.targetedCol + 1
            if newTarget < NUM_CELLS_HORIZONTAL:
                self.targetedCol = newTarget
            else:
                self.targetedCol = 0
        else:
            self.targetedCol = NUM_CELLS_HORIZONTAL-1

    def displayCaptiveMessage(self, header, body, confirm, decline):
        """Capture the main surface with a message which requires a user confirmation or denial to dismiss.

        :param str header: Message to be displayed as the header.
        :param str body: Longer message to be displayed as the text body.
        :param str confirm: Confirmation button label.
        :param str decline: Denial button label.
        :rtype: None
        """

        self.captive = True

        # Dimensions
        button_width = MARGIN * 7
        button_height = MARGIN * 2

        # Containing Box
        pygame.draw.rect(self.window, GREY, (MARGIN, MARGIN, GAME_WIDTH-(MARGIN*2), GAME_HEIGHT-(MARGIN*2)))

        # Header Message
        font_header = pygame.font.Font('freesansbold.ttf', 16*SIZE_MULTIPLIER)
        surface_header = font_header.render(header, True, RED)
        rect_header = surface_header.get_rect()
        rect_header.center = (GAME_WIDTH/2, GAME_HEIGHT/4)
        self.window.blit(surface_header, rect_header)

        # Body Message
        font_body = pygame.font.Font('freesansbold.ttf', 8*SIZE_MULTIPLIER)
        surface_body = font_body.render(body, True, BLACK)
        rect_body = surface_body.get_rect()
        rect_body.center = (GAME_WIDTH/2, (GAME_HEIGHT/3) + MARGIN)
        self.window.blit(surface_body, rect_body)
    
        # Buttons
        self.refreshCaptiveButtons(confirm, decline, button_width, button_height)

    def refreshCaptiveButtons(self, confirm, decline, button_width, button_height):
        """Draw the buttons for the captive message window.

        :param str confirm: Confirmation button label.
        :param str decline: Denial button label.
        :param int button_width: Width of the button to draw.
        :param int button_height: Height of the button to draw.
        :rtype: None
        """
        # Confirm Button
        confirmColor = GREEN
        declineColor = RED
        if self.captiveKeyResponse:
            confirmColor = self.brightenRGB(confirmColor)
        else:
            declineColor = self.brightenRGB(declineColor)
        self.confirm_button = pygame.draw.rect(self.window, confirmColor, ((GAME_WIDTH/2)-button_width-MARGIN, (GAME_HEIGHT/4)*3, button_width, button_height))
        font_confirm = pygame.font.Font('freesansbold.ttf', 4*SIZE_MULTIPLIER) 
        surface_confirm = font_confirm.render(confirm, True, WHITE)
        rect_confirm = surface_confirm.get_rect()
        rect_confirm.center = self.confirm_button.center
        self.window.blit(surface_confirm, rect_confirm)

        # Decline Button
        self.decline_button = pygame.draw.rect(self.window, declineColor, ((GAME_WIDTH/2)+MARGIN, (GAME_HEIGHT/4)*3, button_width, button_height))
        font_decline = pygame.font.Font('freesansbold.ttf', 4*SIZE_MULTIPLIER) 
        surface_decline = font_decline.render(decline, True, WHITE)
        rect_decline = surface_decline.get_rect()
        rect_decline.center = self.decline_button.center
        self.window.blit(surface_decline, rect_decline)

    def getScore(self, playerNumber):
        """Get the win count of a player.

        :param playerNumber: The number of the player whose score to retrieve.
        :type playerNumber: 1 <= int <= 2
        :return: Score of the player (number of game wins).
        :rtype: int
        """
        if playerNumber == 1:
            return self.score[0]
        elif playerNumber == 2:
            return self.score[1]
        else:
            return -1
    
    def addWinToScore(self, playerNumber):
        """Add a win to a player's score.

        :param playerNumber: The number of the player whose score to retrieve.
        :type playerNumber: 1 <= int <= 2
        :rtype: None
        """
        if playerNumber == 1:
            self.score[0] += 1
        elif playerNumber == 2:
            self.score[1] += 1
    
    def endGame(self):
        """End the current game and prompt user to exit or play again.

        :rtype: None
        """
        self.activeGame = False
        self.targetedCol = -1
        self.window.fill(BLACK)
        self.drawScoreBoard()
        if self.grid.victor == -1:
            self.displayCaptiveMessage('Game Over!', 'No One Wins...', "Play Again", "Exit")
        else:
            self.addWinToScore(self.grid.victor)
            self.displayCaptiveMessage('Game Over!', 'Player ' + str(self.grid.victor) + ' Wins!', "Play Again", "Exit")

    def reset(self):
        """Reset the game for a new round.

        :rtype: None
        """
        self.activeGame = True
        self.grid.reset()
    
    def onexit(self, *args):
        """Exit the game, return to Plethora.

        :rtype: None
        """
        self.resetWindow(SIZE_MULTIPLIER)
        super().onexit()


if __name__ == '__main__':
    Connect4()
