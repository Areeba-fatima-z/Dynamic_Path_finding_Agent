import pygame
import sys
import time
import random
from grid import Grid
from algorithms import SearchAlgorithm

class PathfindingGUI:
    def __init__(self, rows=20, cols=20, cell_size=30):
        pygame.init()
        
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        
        # Calculate window size
        self.width = cols * cell_size + 300  # Extra space for controls
        self.height = rows * cell_size
        
        # Handle cases where screen might be too small
        if self.height < 600:
            self.height = 600
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dynamic Pathfinding Agent")
        
        # Colors
        self.COLORS = {
            'empty': (255, 255, 255),
            'obstacle': (0, 0, 0),
            'start': (0, 255, 0),
            'goal': (255, 0, 0),
            'path': (0, 255, 0),
            'visited': (173, 216, 230),  # Light blue
            'frontier': (255, 255, 0),    # Yellow
            'grid_line': (200, 200, 200),
            'button': (220, 220, 220),
            'button_hover': (200, 200, 200)
        }
        
        # Initialize grid
        self.grid = Grid(rows, cols)
        self.grid.generate_random_maze(0.3)
        
        # Algorithm settings
        self.current_algorithm = 'a_star'  # 'a_star' or 'greedy'
        self.current_heuristic = 'manhattan'
        self.dynamic_mode = False
        self.obstacle_spawn_prob = 0.05
        
        # Search state
        self.search_result = None
        self.last_path_time = 0
        
        # Font for metrics
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Button states
        self.buttons = []
        self.button_hover = None
        
    def draw_grid(self):
        """Draw the grid and cells"""
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size
                y = row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                # Determine cell color
                if (row, col) == self.grid.start:
                    color = self.COLORS['start']
                elif (row, col) == self.grid.goal:
                    color = self.COLORS['goal']
                elif self.grid.is_obstacle(row, col):
                    color = self.COLORS['obstacle']
                elif self.search_result and (row, col) in self.search_result.path:
                    color = self.COLORS['path']
                elif self.search_result and (row, col) in self.search_result.visited_nodes:
                    color = self.COLORS['visited']
                elif self.search_result and (row, col) in self.search_result.frontier_nodes:
                    color = self.COLORS['frontier']
                else:
                    color = self.COLORS['empty']
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.COLORS['grid_line'], rect, 1)
    
    def draw_buttons(self, panel_x, y_offset):
        """Draw all buttons"""
        self.buttons = []
        
        button_configs = [
            ("a_star", "A*", (panel_x + 10, y_offset + 30, 80, 30)),
            ("greedy", "Greedy", (panel_x + 100, y_offset + 30, 80, 30)),
            ("heuristic", f"Heuristic: {self.current_heuristic[:3]}", (panel_x + 10, y_offset + 70, 170, 30)),
            ("maze", "Random Maze", (panel_x + 10, y_offset + 110, 170, 30)),
            ("dynamic", f"Dynamic: {'ON' if self.dynamic_mode else 'OFF'}", (panel_x + 10, y_offset + 150, 170, 30)),
            ("run", "Run Search", (panel_x + 10, y_offset + 190, 170, 30)),
            ("clear", "Clear Grid", (panel_x + 10, y_offset + 230, 170, 30))
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for btn_id, text, rect in button_configs:
            # Check hover
            if (rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and 
                rect[1] <= mouse_pos[1] <= rect[1] + rect[3]):
                color = self.COLORS['button_hover']
                self.button_hover = btn_id
            else:
                color = self.COLORS['button']
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)
            
            # Handle long text
            if len(text) > 12:
                text = text[:12] + "..."
            
            btn_text = self.small_font.render(text, True, (0, 0, 0))
            text_rect = btn_text.get_rect(center=(rect[0] + rect[2]//2, rect[1] + rect[3]//2))
            self.screen.blit(btn_text, text_rect)
            self.buttons.append((btn_id, rect))
    
    def draw_controls(self):
        """Draw control panel and metrics"""
        panel_x = self.cols * self.cell_size + 10
        panel_width = self.width - panel_x - 10
        
        # Draw panel background
        pygame.draw.rect(self.screen, (240, 240, 240), 
                         (panel_x, 0, panel_width, self.height))
        
        # Controls title
        title = self.font.render("Controls", True, (0, 0, 0))
        self.screen.blit(title, (panel_x + 10, 10))
        
        # Draw buttons
        self.draw_buttons(panel_x, 50)
        
        # Metrics dashboard
        if self.search_result:
            y_offset = 300
            metrics_title = self.font.render("Metrics", True, (0, 0, 0))
            self.screen.blit(metrics_title, (panel_x + 10, y_offset))
            
            metrics = [
                f"Nodes Visited: {self.search_result.nodes_visited}",
                f"Path Cost: {self.search_result.path_cost}",
                f"Time: {self.search_result.execution_time:.2f}ms"
            ]
            
            for i, metric in enumerate(metrics):
                metric_text = self.small_font.render(metric, True, (0, 0, 0))
                self.screen.blit(metric_text, (panel_x + 10, y_offset + 30 + i*25))
            
            # Algorithm and heuristic info
            algo_text = self.small_font.render(
                f"Algorithm: {self.current_algorithm}", True, (0, 0, 0))
            self.screen.blit(algo_text, (panel_x + 10, y_offset + 120))
        
        # Instructions
        inst_y = self.height - 100
        inst_title = self.small_font.render("Instructions:", True, (0, 0, 0))
        self.screen.blit(inst_title, (panel_x + 10, inst_y))
        
        instructions = [
            "Click cells: Toggle obstacle",
            "Start: Green | Goal: Red",
            "Yellow: Frontier | Blue: Visited"
        ]
        
        for i, inst in enumerate(instructions):
            inst_text = self.small_font.render(inst, True, (100, 100, 100))
            self.screen.blit(inst_text, (panel_x + 10, inst_y + 20 + i*18))
        
        # Dynamic mode indicator
        if self.dynamic_mode:
            dyn_text = self.font.render("⚠ DYNAMIC MODE", True, (255, 0, 0))
            self.screen.blit(dyn_text, (panel_x + 10, self.height - 30))
    
    def handle_click(self, pos):
        """Handle mouse clicks for grid editing"""
        x, y = pos
        
        # Check if click is in grid area
        if x < self.cols * self.cell_size and y < self.rows * self.cell_size:
            col = x // self.cell_size
            row = y // self.cell_size
            
            # Toggle obstacle
            self.grid.toggle_cell(row, col)
            
            # Clear previous search results
            self.search_result = None
            return True
        return False
    
    def handle_button_click(self, pos):
        """Handle button clicks"""
        x, y = pos
        
        for button_id, rect in self.buttons:
            if (rect[0] <= x <= rect[0] + rect[2] and 
                rect[1] <= y <= rect[1] + rect[3]):
                
                if button_id == "a_star":
                    self.current_algorithm = 'a_star'
                    print("Switched to A* Algorithm")
                
                elif button_id == "greedy":
                    self.current_algorithm = 'greedy'
                    print("Switched to Greedy BFS Algorithm")
                
                elif button_id == "heuristic":
                    heuristics = ['manhattan', 'euclidean', 'chebyshev']
                    current_idx = heuristics.index(self.current_heuristic)
                    self.current_heuristic = heuristics[(current_idx + 1) % 3]
                    print(f"Switched to {self.current_heuristic} heuristic")
                
                elif button_id == "maze":
                    self.grid.generate_random_maze(0.3)
                    self.search_result = None
                    print("Generated new random maze")
                
                elif button_id == "dynamic":
                    self.dynamic_mode = not self.dynamic_mode
                    print(f"Dynamic mode: {'ON' if self.dynamic_mode else 'OFF'}")
                
                elif button_id == "run":
                    self.run_search()
                
                elif button_id == "clear":
                    self.grid.clear_grid()
                    self.search_result = None
                    print("Grid cleared")
                
                return True
        return False
    
    def run_search(self):
        """Execute the selected search algorithm"""
        print(f"Running {self.current_algorithm} with {self.current_heuristic} heuristic...")
        algorithm = SearchAlgorithm(self.grid, self.current_heuristic)
        
        if self.current_algorithm == 'greedy':
            success = algorithm.greedy_bfs()
        else:
            success = algorithm.a_star()
        
        if success:
            print(f"Path found! Cost: {algorithm.path_cost}, Nodes: {algorithm.nodes_visited}")
        else:
            print("No path found!")
        
        self.search_result = algorithm
        self.last_path_time = time.time()
    
    def spawn_dynamic_obstacle(self):
        """Spawn a new obstacle randomly"""
        if not self.dynamic_mode or not self.search_result:
            return
        
        if random.random() < self.obstacle_spawn_prob:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            # Don't place obstacles on start or goal
            if (row, col) != self.grid.start and (row, col) != self.grid.goal:
                if not self.grid.is_obstacle(row, col):
                    self.grid.grid[row][col] = 1
                    
                    # Check if current path is blocked
                    if (self.search_result.path and 
                        (row, col) in self.search_result.path):
                        print("Path blocked! Replanning...")
                        self.run_search()  # Replan
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        last_spawn_time = time.time()
        
        while running:
            current_time = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if not self.handle_button_click(event.pos):
                            self.handle_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.run_search()
                    elif event.key == pygame.K_d:
                        self.dynamic_mode = not self.dynamic_mode
                        print(f"Dynamic mode: {'ON' if self.dynamic_mode else 'OFF'}")
            
            # Dynamic obstacle spawning (every 0.5 seconds)
            if self.dynamic_mode and current_time - last_spawn_time > 0.5:
                self.spawn_dynamic_obstacle()
                last_spawn_time = current_time
            
            # Clear screen
            self.screen.fill((255, 255, 255))
            
            # Draw grid and controls
            self.draw_grid()
            self.draw_controls()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()