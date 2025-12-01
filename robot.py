from typing import Tuple, List
from grid import Grid
from pathfinding import a_star, dijkstra_shortest_path, choose_return_path_to_dump
from utils import manhattan

Coord = Tuple[int, int]

class Robot:
    def __init__(
        self,
        grid: Grid,
        recharge: Coord,
        trash_bin: Coord,
        start: Coord,
        battery_capacity: int = 100,
        bin_capacity: int = 15,
        vacuum_cost_per_unit: int = 1,
    ):
        self.grid = grid
        self.recharge = recharge
        self.trash_bin = trash_bin
        self.pos = start
        self.battery_capacity = battery_capacity
        self.battery = battery_capacity
        self.dustthreshold = bin_capacity
        self.bin_capacity = bin_capacity
        self.dust_collected = 0
        self.vacuum_cost_per_clean_cell = vacuum_cost_per_unit
        self.dist_to_recharge = 0
        self.path: List[Coord] = []
        self.state = "EXPLORING"

    def pick_explore_target(self):
        best_score = -float('inf')
        best = None
        for cell in self.grid.nonzero_cells():
            dist = manhattan(self.pos, cell)
            score = self.grid.get(cell) / (dist + 1)
            if score > best_score:
                best_score = score
                best = cell
        return best

    def plan_explore(self):
        target = self.pick_explore_target()
        if target is None:
            return False
        path = a_star(self.grid, self.pos, target)
        if not path:
            return False
        self.path = path[1:]
        return True

    def plan_return_to_charge(self):
        path = dijkstra_shortest_path(self.grid, self.pos, list(self.grid.zero_cells()))
        if not path:
            return False
        self.path = path[1:]
        return True

    def plan_return_to_trash(self):
        path = choose_return_path_to_dump(self.grid, self.pos, self.trash_bin)
        if path:
            self.path = path[1:]
            return True
        return False

    def follow_step(self):
        if not self.path:
            return
        self.pos = self.path.pop(0)
        if self.state == "EXPLORING":
            self.attempt_vacuum_here()
            return
        self.battery -= self.vacuum_cost_per_clean_cell

    def attempt_vacuum_here(self):
        dust = self.grid.get(self.pos)
        battery_left_to_clean = self.battery - (self.dist_to_recharge + 1)
        bin_capacity_left = self.bin_capacity - dust
       
        if self.bin_capacity < dust:
                self.state = "RETURNING_TO_TRASH"
                self.path = []
                return
        if battery_left_to_clean < 0:
                self.state = "RETURNING_TO_CHARGE"
                self.path = []
                return
        max_cleanable = min(dust, bin_capacity_left, battery_left_to_clean)
        collected = self.grid.collect(self.pos, amount=max_cleanable)
        self.battery -= collected 
        self.bin_capacity -= collected
        self.dust_collected += collected

        if self.bin_capacity == 0:
            self.path = []
            self.state = "RETURNING_TO_TRASH"
            return

        if self.battery <= manhattan(self.pos, self.recharge):
            self.path = []
            self.state = "RETURNING_TO_CHARGE"
            return

    def at_recharge(self) -> bool:
        return self.pos == self.recharge

    def at_trash(self) -> bool:
        return self.pos == self.trash_bin

    def deposit(self):
        self.bin_capacity = self.dustthreshold
        return 

    def charge(self):
        self.battery = self.battery_capacity
        self.dist_to_recharge = 0
        return
