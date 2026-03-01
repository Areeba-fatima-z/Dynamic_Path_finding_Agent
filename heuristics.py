import math

def manhattan_distance(node, goal):
    """Manhattan distance heuristic"""
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def euclidean_distance(node, goal):
    """Euclidean distance heuristic"""
    return math.sqrt((node[0] - goal[0])**2 + (node[1] - goal[1])**2)

def chebyshev_distance(node, goal):
    """Chebyshev distance heuristic"""
    return max(abs(node[0] - goal[0]), abs(node[1] - goal[1]))

# Heuristic dictionary for easy selection
HEURISTICS = {
    'manhattan': manhattan_distance,
    'euclidean': euclidean_distance,
    'chebyshev': chebyshev_distance
}