import heapq
import time
from collections import defaultdict
import heuristics

class SearchAlgorithm:
    def __init__(self, grid, heuristic='manhattan'):
        self.grid = grid
        self.heuristic = heuristics.HEURISTICS[heuristic]
        self.nodes_visited = 0
        self.execution_time = 0
        self.path_cost = 0
        self.path = []
        self.frontier_nodes = []
        self.visited_nodes = []
    
    def greedy_bfs(self):
        """Greedy Best-First Search implementation"""
        start_time = time.time()
        start = self.grid.start
        goal = self.grid.goal
        
        # Priority queue: (heuristic, node, path)
        frontier = [(self.heuristic(start, goal), start, [start])]
        visited = set()
        self.frontier_nodes = [start]
        self.visited_nodes = []
        
        while frontier:
            _, current, path = heapq.heappop(frontier)
            self.frontier_nodes = [node for _, node, _ in frontier]
            
            if current in visited:
                continue
            
            visited.add(current)
            self.visited_nodes.append(current)
            self.nodes_visited = len(visited)
            
            if current == goal:
                self.path = path
                self.path_cost = len(path) - 1
                self.execution_time = (time.time() - start_time) * 1000
                return True
            
            for neighbor in self.grid.get_neighbors(current):
                if neighbor not in visited:
                    h = self.heuristic(neighbor, goal)
                    new_path = path + [neighbor]
                    heapq.heappush(frontier, (h, neighbor, new_path))
        
        self.execution_time = (time.time() - start_time) * 1000
        return False
    
    def a_star(self):
        """A* Search implementation"""
        start_time = time.time()
        start = self.grid.start
        goal = self.grid.goal
        
        # Priority queue: (f, node, path, g)
        # f = g + h
        frontier = [(self.heuristic(start, goal), 0, start, [start])]
        visited = set()
        g_score = defaultdict(lambda: float('inf'))
        g_score[start] = 0
        
        self.frontier_nodes = [start]
        self.visited_nodes = []
        
        while frontier:
            f, g, current, path = heapq.heappop(frontier)
            self.frontier_nodes = [node for _, _, node, _ in frontier]
            
            if current in visited:
                continue
            
            visited.add(current)
            self.visited_nodes.append(current)
            self.nodes_visited = len(visited)
            
            if current == goal:
                self.path = path
                self.path_cost = g
                self.execution_time = (time.time() - start_time) * 1000
                return True
            
            for neighbor in self.grid.get_neighbors(current):
                if neighbor in visited:
                    continue
                
                new_g = g + 1  # Uniform cost per move
                
                if new_g < g_score[neighbor]:
                    g_score[neighbor] = new_g
                    h = self.heuristic(neighbor, goal)
                    f = new_g + h
                    new_path = path + [neighbor]
                    heapq.heappush(frontier, (f, new_g, neighbor, new_path))
        
        self.execution_time = (time.time() - start_time) * 1000
        return False