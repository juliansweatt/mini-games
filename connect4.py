import pygame

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

NUM_CELLS_VERTICAL = 6
NUM_CELLS_HORIZONTAL = 7
CELL_RADIUS = 10
MARGIN = 5
WINDOW_HEIGHT = (CELL_RADIUS * 2 + MARGIN) * NUM_CELLS_VERTICAL + MARGIN
WINDOW_WIDTH = (CELL_RADIUS * 2 + MARGIN) * NUM_CELLS_HORIZONTAL + MARGIN

WIN_SERIES_LENGTH = 4

class Grid:
    def __init__(self, width, height, neutral_color, p1_color, p2_color):
        self.grid = []
        self.neutral_color = neutral_color
        self.p1_color = p1_color
        self.p2_color = p2_color
        self.height = height
        self.width = width
        
        self.reset()
    
    def reset(self):
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
        setIndex = -1
        for index, cell in enumerate(self.grid[col]):
            if cell == 0:
                setIndex = index
                break
        
        if setIndex > -1:
            self.grid[col][setIndex] = playerNumber
            victor = self.checkVictor(col, setIndex)
            if victor != 0:
                print("VICTOR:", victor) # Replace Print with UI/End Game Logic
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
        self.victor = 0
        self.grid = Grid(NUM_CELLS_HORIZONTAL, NUM_CELLS_VERTICAL, WHITE, RED, GREEN)
        self.start(self.setupWindow())

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

    @staticmethod
    def drawGrid(window, grid):
        uiGrid = []

        for col in range(NUM_CELLS_HORIZONTAL):
            uiGrid.append([])
            for row in range(NUM_CELLS_VERTICAL):
                uiGrid[col].append(pygame.draw.circle(window, grid.getCellColor(col, NUM_CELLS_VERTICAL-1-row), ((MARGIN+CELL_RADIUS*2) * col + CELL_RADIUS + MARGIN, (MARGIN+CELL_RADIUS*2) * row + CELL_RADIUS + MARGIN), CELL_RADIUS))

        pygame.display.update()
        return uiGrid

    def start(self, window):
        run = True
        while run:
            pygame.time.delay(100)

            UI = self.drawGrid(window, self.grid)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    for index,col in enumerate(UI):
                        for cell in col:
                            if cell.collidepoint(mousePos):
                                self.attemptMove(index)

        pygame.quit()
    
    def attemptMove(self, column):
        if self.grid.playColumn(self.currentPlayer, column):
            # Move Successful
            if self.currentPlayer == 1:
                self.currentPlayer = 2
            elif self.currentPlayer == 2:
                self.currentPlayer = 1
        else:
            # Invalid Move
            print("Invalid Move!")

if __name__ == '__main__':
    Connect4()