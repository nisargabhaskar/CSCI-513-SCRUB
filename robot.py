from typing import Tuple, List
from grid import Grid
from pathfinding import weighted_a_star, choose_return_path
from utils import euclidean

Coord = Tuple[int, int]

class Robot:
    def __init__(self, grid: Grid, recharge: Coord, start: Coord, capacity: int = 10):
        self.grid = grid
        self.recharge = recharge
        self.pos = start
        self.capacity = capacity
        self.dust_collected = 0
        self.path: List[Coord] = []  

    def pick_explore_target(self):
        best_score = -float('inf')
        best = None
        for cell in self.grid.nonzero_cells():
            dist = euclidean(self.pos, cell)
            if dist == 0:
                score = self.grid.get(cell)
            else:
                score = self.grid.get(cell) / dist
            if score > best_score:
                best_score = score
                best = cell
        return best

    def plan_explore(self):
        target = self.pick_explore_target()
        if target is None:
            return False
        path = weighted_a_star(self.grid, self.pos, target)
        if path:
            self.path = path[1:]
            return True
        return False

    def plan_return(self):
        ret_path = choose_return_path(self.grid, self.pos, self.recharge)
        if ret_path:
            self.path = ret_path[1:]
            return True
        return False

    def follow_step(self): 
        self.pos = self.path.pop(0)
        self.dust_collected += self.grid.collect(self.pos)

    def at_recharge(self):
        return self.pos == self.recharge

    def deposit(self):
        deposited = self.dust_collected
        self.dust_collected = 0
        return deposited
