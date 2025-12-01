from typing import Tuple

Coord = Tuple[int, int]

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def in_bounds(pos, rows, cols):
    r, c = pos
    return 0 <= r < rows and 0 <= c < cols

def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
