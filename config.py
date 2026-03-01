# config.py
# Game settings
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 15
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Node states
START = (0, 255, 0)        # Green
GOAL = (255, 0, 0)          # Red
WALL = (0, 0, 0)            # Black
VISITED = (100, 100, 255)   # Light blue
FRONTIER = (255, 255, 0)    # Yellow
PATH = (0, 255, 0)          # Green
EMPTY = (255, 255, 255)     # White