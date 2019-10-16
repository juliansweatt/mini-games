import pygame

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
GREY = (160,160,160)

NUM_CELLS_VERTICAL = 6
NUM_CELLS_HORIZONTAL = 7
CELL_RADIUS = 10
MARGIN = 5
GAME_HEIGHT = (CELL_RADIUS * 2 + MARGIN) * NUM_CELLS_VERTICAL + MARGIN
GAME_WIDTH = (CELL_RADIUS * 2 + MARGIN) * NUM_CELLS_HORIZONTAL + MARGIN
SCOREBOARD_HEIGHT = (MARGIN * 3)
WINDOW_HEIGHT = GAME_HEIGHT + SCOREBOARD_HEIGHT

WIN_SERIES_LENGTH = 4

class Grid:
    def __init__(self, width, height, neutral_color, p1_color, p2_color):
        self.neutral_color = neutral_color
        self.p1_color = p1_color
        self.p2_color = p2_color
        self.height = height
        self.width = width
        self.reset()
    
    def reset(self):
        self.grid = []
        self.victor = 0
        for col in range(self.width):
            self.grid.append([])
            for cell in range(self.height):
                self.grid[col].append(0)

    def getPlayerColor(self, playerNumber):
        if playerNumber == 1:
            return self.p1_color
        elif playerNumber == 2:
            return self.p2_color
        else:
            return self.neutral_color

    def getCellColor(self, x, y):
        if x < self.width and x > -1 and y > -1 and y < self.height:
            cell = self.grid[x][y]
            return self.getPlayerColor(cell)
    
    def playColumn(self, playerNumber, col):
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

class Connect4:
    def __init__(self):
        pygame.init()
        self.score = [0,0]
        self.currentPlayer = 1
        self.activeGame = True
        self.grid = Grid(NUM_CELLS_HORIZONTAL, NUM_CELLS_VERTICAL, WHITE, RED, GREEN)
        self.window = self.setupWindow()
        self.start()

    def setupWindow(self):
        win = pygame.display.set_mode((GAME_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Connect 4")
        win.fill(BLACK)
        self.expandWindow(4)
        return win

    @staticmethod
    def expandWindow(n):
        global CELL_RADIUS
        global MARGIN
        global GAME_HEIGHT
        global GAME_WIDTH
        global WINDOW_HEIGHT
        global SCOREBOARD_HEIGHT

        CELL_RADIUS *= n
        MARGIN *= n
        GAME_HEIGHT *= n
        WINDOW_HEIGHT *= n
        GAME_WIDTH *= n
        SCOREBOARD_HEIGHT *= n
        pygame.display.set_mode((GAME_WIDTH, WINDOW_HEIGHT))

    def drawGrid(self):
        uiGrid = []

        for col in range(self.grid.width):
            uiGrid.append([])
            for row in range(self.grid.height):
                uiGrid[col].append(pygame.draw.circle(self.window, self.grid.getCellColor(col, self.grid.height-1-row), ((MARGIN+CELL_RADIUS*2) * col + CELL_RADIUS + MARGIN, (MARGIN+CELL_RADIUS*2) * row + CELL_RADIUS + MARGIN), CELL_RADIUS))

        pygame.display.update()
        return uiGrid

    def drawScoreBoard(self):
        # Board
        background = pygame.draw.rect(self.window, GREY, (0, GAME_HEIGHT, GAME_WIDTH, SCOREBOARD_HEIGHT))

        # Status Circle
        status_circle = pygame.draw.circle(self.window, self.grid.getPlayerColor(self.currentPlayer), (int(SCOREBOARD_HEIGHT/2), background.center[1]), int(SCOREBOARD_HEIGHT/2)-int(MARGIN/3))
        pygame.draw.circle(self.window, BLACK, (int(SCOREBOARD_HEIGHT/2), background.center[1]), int(SCOREBOARD_HEIGHT/2)-int(MARGIN/4), 5)

        # Player Name
        font_player = pygame.font.Font('freesansbold.ttf', 32)
        surface_player = font_player.render('Player ' + str(self.currentPlayer), False, BLACK)
        rect_player = surface_player.get_rect()
        rect_player.midleft = (status_circle.right + int(MARGIN/2), status_circle.center[1]+int(MARGIN/2))
        self.window.blit(surface_player, rect_player)

        # Current Player Header
        font_cp = pygame.font.Font('freesansbold.ttf', 12)
        surface_cp = font_cp.render('Current Player:', True, BLACK)
        rect_cp = surface_cp.get_rect()
        rect_cp.bottomleft = rect_player.topleft
        self.window.blit(surface_cp, rect_cp)

        # Score Header
        font_score_header = pygame.font.Font('freesansbold.ttf', 12)
        surface_score_header = font_score_header.render('Score:', True, BLACK)
        rect_score_header = surface_score_header.get_rect()
        rect_score_header.topright = (GAME_WIDTH-(MARGIN*2), GAME_HEIGHT+int(MARGIN/3))
        self.window.blit(surface_score_header, rect_score_header)

        # Score P1
        font_score_p1 = pygame.font.Font('freesansbold.ttf', 12)
        surface_score_p1 = font_score_p1.render('Player 1: ' + str(self.getScore(1)), True, BLACK)
        rect_score_p1 = surface_score_p1.get_rect()
        rect_score_p1.center = (rect_score_header.center[0], rect_score_header.center[1]+ int(SCOREBOARD_HEIGHT/4))
        self.window.blit(surface_score_p1, rect_score_p1)

        # Score P2
        font_score_p2 = pygame.font.Font('freesansbold.ttf', 12)
        surface_score_p2 = font_score_p2.render('Player 2: ' + str(self.getScore(2)), True, BLACK)
        rect_score_p2 = surface_score_p2.get_rect()
        rect_score_p2.center = (rect_score_header.center[0], rect_score_header.center[1]+ int((SCOREBOARD_HEIGHT/4)*2))
        self.window.blit(surface_score_p2, rect_score_p2)

    def start(self):
        self.RUN = True
        self.drawScoreBoard()
        while self.RUN:
            pygame.time.delay(100)

            if self.activeGame:
                UI = self.drawGrid()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUN = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.activeGame:
                    mousePos = pygame.mouse.get_pos()
                    for index,col in enumerate(UI):
                        for cell in col:
                            if cell.collidepoint(mousePos):
                                self.attemptMove(index)
        pygame.quit()
    
    def attemptMove(self, column):
        if self.grid.playColumn(self.currentPlayer, column):
            # Move Successful
            if self.grid.victor == 0:
                if self.currentPlayer == 1:
                    self.currentPlayer = 2
                elif self.currentPlayer == 2:
                    self.currentPlayer = 1
                self.drawScoreBoard()
            else:
                self.endGame()
        else:
            # Invalid Move
            print("Invalid Move!")
    
    def displayCaptiveMessage(self, header, body, confirm, decline):
        captive = True

        # Dimensions
        button_width = MARGIN * 7
        button_height = MARGIN * 2

        # Containing Box
        pygame.draw.rect(self.window, GREY, (MARGIN, MARGIN, GAME_WIDTH-(MARGIN*2), GAME_HEIGHT-(MARGIN*2)))

        # Header Message
        font_header = pygame.font.Font('freesansbold.ttf', 64)
        surface_header = font_header.render(header, True, RED)
        rect_header = surface_header.get_rect()
        rect_header.center = (GAME_WIDTH/2, GAME_HEIGHT/4)
        self.window.blit(surface_header, rect_header)

        # Body Message
        font_body = pygame.font.Font('freesansbold.ttf', 32)
        surface_body = font_body.render(body, True, BLACK)
        rect_body = surface_body.get_rect()
        rect_body.center = (GAME_WIDTH/2, (GAME_HEIGHT/3) + MARGIN)
        self.window.blit(surface_body, rect_body)

        # Confirm Button
        confirm_button = pygame.draw.rect(self.window, GREEN, ((GAME_WIDTH/2)-button_width-MARGIN, (GAME_HEIGHT/4)*3, button_width, button_height))
        font_confirm = pygame.font.Font('freesansbold.ttf', 16) 
        surface_confirm = font_confirm.render(confirm, True, WHITE)
        rect_confirm = surface_confirm.get_rect()
        rect_confirm.center = confirm_button.center
        self.window.blit(surface_confirm, rect_confirm)

        # Decline Button
        decline_button = pygame.draw.rect(self.window, RED, ((GAME_WIDTH/2)+MARGIN, (GAME_HEIGHT/4)*3, button_width, button_height))
        font_decline = pygame.font.Font('freesansbold.ttf', 16) 
        surface_decline = font_decline.render(decline, True, WHITE)
        rect_decline = surface_decline.get_rect()
        rect_decline.center = decline_button.center
        self.window.blit(surface_decline, rect_decline)

        # Update Window
        pygame.display.update()

        # Button Listeners
        while captive:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if confirm_button.collidepoint(mousePos):
                        # Play Again
                        self.reset()
                        self.drawScoreBoard()
                        captive = False
                    elif decline_button.collidepoint(mousePos):
                        # Exit Game
                        self.exitGame()
                        captive = False

    def getScore(self, playerNumber):
        if playerNumber == 1:
            return self.score[0]
        elif playerNumber == 2:
            return self.score[1]
        else:
            return -1
    
    def addWinToScore(self, playerNumber):
        if playerNumber == 1:
            self.score[0] += 1
        elif playerNumber == 2:
            self.score[1] += 1
        self.drawScoreBoard()
    
    def endGame(self):
        self.activeGame = False
        if self.grid.victor == -1:
            self.displayCaptiveMessage('Game Over!', 'No One Wins...', "Play Again", "Exit")
        else:
            self.addWinToScore(self.grid.victor)
            self.displayCaptiveMessage('Game Over!', 'Player ' + str(self.grid.victor) + ' Wins!', "Play Again", "Exit")

    def reset(self):
        self.window.fill(BLACK)
        self.activeGame = True
        self.grid.reset()
    
    def exitGame(self):
        self.RUN = False


if __name__ == '__main__':
    Connect4()