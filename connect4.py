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
WINDOW_HEIGHT = (CELL_RADIUS * 2 + MARGIN) * NUM_CELLS_VERTICAL + MARGIN
WINDOW_WIDTH = (CELL_RADIUS * 2 + MARGIN) * NUM_CELLS_HORIZONTAL + MARGIN

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

    def getCellOwner(self, x, y):
        return self.grid[x][y]
    
    def getCellColor(self, x, y):
        if x < self.width and x > -1 and y > -1 and y < self.height:
            cell = self.grid[x][y]
            if cell == 0:
                return self.neutral_color
            elif cell == 1:
                return self.p1_color
            elif cell == 2:
                return self.p2_color
    
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

        return 0

class Connect4:
    def __init__(self):
        pygame.init()
        self.currentPlayer = 1
        self.activeGame = True
        self.grid = Grid(NUM_CELLS_HORIZONTAL, NUM_CELLS_VERTICAL, WHITE, RED, GREEN)
        self.window = self.setupWindow()
        self.start()

    def setupWindow(self):
        win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Connect 4")
        win.fill(BLACK)
        self.expandWindow(3)
        return win

    @staticmethod
    def expandWindow(n):
        global CELL_RADIUS
        global MARGIN
        global WINDOW_HEIGHT
        global WINDOW_WIDTH

        CELL_RADIUS *= n
        MARGIN *= n
        WINDOW_HEIGHT *= n
        WINDOW_WIDTH *= n
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def drawGrid(self):
        uiGrid = []

        for col in range(self.grid.width):
            uiGrid.append([])
            for row in range(self.grid.height):
                uiGrid[col].append(pygame.draw.circle(self.window, self.grid.getCellColor(col, self.grid.height-1-row), ((MARGIN+CELL_RADIUS*2) * col + CELL_RADIUS + MARGIN, (MARGIN+CELL_RADIUS*2) * row + CELL_RADIUS + MARGIN), CELL_RADIUS))

        pygame.display.update()
        return uiGrid

    def start(self):
        self.RUN = True
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
        pygame.draw.rect(self.window, GREY, (MARGIN, MARGIN, WINDOW_WIDTH-(MARGIN*2), WINDOW_HEIGHT-(MARGIN*2)))

        # Header Message
        font_header = pygame.font.Font('freesansbold.ttf', 64)
        surface_header = font_header.render(header, True, RED)
        rect_header = surface_header.get_rect()
        rect_header.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/4)
        self.window.blit(surface_header, rect_header)

        # Body Message
        font_body = pygame.font.Font('freesansbold.ttf', 32)
        surface_body = font_body.render(body, True, BLACK)
        rect_body = surface_body.get_rect()
        rect_body.center = (WINDOW_WIDTH/2, (WINDOW_HEIGHT/3) + MARGIN)
        self.window.blit(surface_body, rect_body)

        # Confirm Button
        confirm_button = pygame.draw.rect(self.window, GREEN, ((WINDOW_WIDTH/2)-button_width-MARGIN, (WINDOW_HEIGHT/4)*3, button_width, button_height))
        font_confirm = pygame.font.Font('freesansbold.ttf', 16) 
        surface_confirm = font_confirm.render(confirm, True, WHITE)
        rect_confirm = surface_confirm.get_rect()
        rect_confirm.center = confirm_button.center
        self.window.blit(surface_confirm, rect_confirm)

        # Decline Button
        decline_button = pygame.draw.rect(self.window, RED, ((WINDOW_WIDTH/2)+MARGIN, (WINDOW_HEIGHT/4)*3, button_width, button_height))
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
                        captive = False
                    elif decline_button.collidepoint(mousePos):
                        # Exit Game
                        self.exitGame()
                        captive = False
    
    def endGame(self):
        self.activeGame = False
        self.displayCaptiveMessage('Game Over!', 'Player ' + str(self.grid.victor) + ' Wins!', "Play Again", "Exit")

    def reset(self):
        self.window.fill(BLACK)
        self.activeGame = True
        self.grid.reset()
    
    def exitGame(self):
        self.RUN = False


if __name__ == '__main__':
    Connect4()