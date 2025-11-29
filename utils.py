import math
from typing import Tuple


Coord = Tuple[int, int]

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def in_bounds(pos, rows, cols):
    r, c = pos
    return 0 <= r < rows and 0 <= c < cols

def obstacle(pos, grid):
    return grid.get(pos) == -1  # assuming -1 indicates an obstacle

def euclidean(a: Coord, b: Coord):
    return math.dist(a, b)