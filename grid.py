from typing import Tuple
from utils import in_bounds, DIRECTIONS, obstacle


Coord = Tuple[int, int]


class Grid:
    def __init__(self, rows: int, cols: int, initial=None):
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


    def collect(self, pos: Coord):
        r, c = pos
        val = self.cells[r][c]
        self.cells[r][c] = 0
        return val


    def neighbors(self, pos: Coord):
        r, c = pos
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if in_bounds((nr, nc), self.rows, self.cols) and not obstacle((nr, nc), self):
                yield (nr, nc)


    def nonzero_cells(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c] != 0:
                    yield (r, c)


    def zero_cells(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c] == 0:
                    yield (r, c)

