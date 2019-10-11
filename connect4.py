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
        
        for col in range(width):
            self.grid.append([])
            for cell in range(height):
                self.grid[col].append(0)
    
    def getCellOwner(self, x, y):
        return self.grid[x][y]
    
    def getCellColor(self, x, y):
        if x < NUM_CELLS_HORIZONTAL and x > -1 and y > -1 and y < NUM_CELLS_HORIZONTAL:
            cell = self.grid[x][y]
            if cell == 0:
                return self.neutral_color
            elif cell == 1:
                return self.p1_color
            elif cell == 2:
                return self.p2_color
    
    def playColumn(self, playerNumber, col):
        setIndex = -1
        for index, cell in reversed(list(enumerate(self.grid[col]))):
            if cell == 0:
                setIndex = index
                break
        
        if setIndex > -1:
            self.grid[col][setIndex] = playerNumber
            return True
        else:
            return False

def init():
    pygame.init()
    return setupWindow()

def setupWindow():
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Connect 4")
    win.fill(BLACK)
    expandWindow(3)
    return win

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

def drawGrid(window, grid):
    for col in range(NUM_CELLS_HORIZONTAL):
        for row in range(NUM_CELLS_VERTICAL):
            pygame.draw.circle(window, grid.getCellColor(col, row), ((MARGIN+CELL_RADIUS*2) * col + CELL_RADIUS + MARGIN, (MARGIN+CELL_RADIUS*2) * row + CELL_RADIUS + MARGIN), CELL_RADIUS)

    pygame.display.update()

def start(window, grid):
    run = True
    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        drawGrid(window, grid)

    pygame.quit()

if __name__ == '__main__':
    start(init(), Grid(NUM_CELLS_HORIZONTAL, NUM_CELLS_VERTICAL, WHITE, RED, GREEN))