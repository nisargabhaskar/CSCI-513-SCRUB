from typing import Tuple, List
from utils import in_bounds, DIRECTIONS

Coord = Tuple[int, int]

class Grid:
    def __init__(self, rows: int, cols: int, initial: List[List[int]] = None):
        self.rows = rows
        self.cols = cols
        if initial:
            self.cells = [row[:] for row in initial]
        else:
            self.cells = [[0 for _ in range(cols)] for _ in range(rows)]

    def get(self, pos: Coord):
        r, c = pos
        return self.cells[r][c]

    def set(self, pos: Coord, value: int):
        r, c = pos
        self.cells[r][c] = value

    def collect(self, pos: Coord, amount: int = None):
        r, c = pos
        val = self.cells[r][c]
        if val <= 0:
            return 0
        if amount is None:
            collected = val
        else:
            collected = min(val, amount)
        self.cells[r][c] = val - collected
        return collected

    def neighbors(self, pos: Coord):
        r, c = pos
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if in_bounds((nr, nc), self.rows, self.cols):
                if self.cells[nr][nc] == -1: #assuming -1 is obstacle
                    continue
                yield (nr, nc)

    def nonzero_cells(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c] > 0:
                    yield (r, c)

    def zero_cells(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c] == 0:
                    yield (r, c)
