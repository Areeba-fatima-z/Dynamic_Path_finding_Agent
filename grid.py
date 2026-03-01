import random

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # List of lists use karo numpy ki jagah
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.goal = (rows-1, cols-1)
        self.obstacle_density = 0.3
    
    def generate_random_maze(self, density=None):
        """Generate random obstacles with given density"""
        if density:
            self.obstacle_density = density
        
        # Reset grid - sab cells ko 0 karo
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = 0
        
        # Random obstacles generate karo
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) != self.start and (i, j) != self.goal:
                    if random.random() < self.obstacle_density:
                        self.grid[i][j] = 1  # 1 means obstacle
        
        # Ensure start and goal are clear
        self.grid[self.start[0]][self.start[1]] = 0
        self.grid[self.goal[0]][self.goal[1]] = 0
    
    def toggle_cell(self, row, col):
        """Toggle obstacle state for interactive editing"""
        if (row, col) != self.start and (row, col) != self.goal:
            self.grid[row][col] = 1 - self.grid[row][col]  # 0->1, 1->0
            return True
        return False
    
    def get_neighbors(self, node):
        """Get valid neighbors (4-directional movement)"""
        row, col = node
        neighbors = []
        
        # Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if (0 <= r < self.rows and 0 <= c < self.cols and 
                self.grid[r][c] == 0):  # Not an obstacle
                neighbors.append((r, c))
        
        return neighbors
    
    def is_obstacle(self, row, col):
        """Check if cell is obstacle"""
        return self.grid[row][col] == 1
    
    def set_start(self, row, col):
        """Set start position"""
        if not self.is_obstacle(row, col):
            self.start = (row, col)
            return True
        return False
    
    def set_goal(self, row, col):
        """Set goal position"""
        if not self.is_obstacle(row, col):
            self.goal = (row, col)
            return True
        return False
    
    def clear_grid(self):
        """Clear all obstacles"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = 0