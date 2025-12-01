import heapq
from typing import Tuple, Optional, Dict, Set, List
from utils import manhattan

Coord = Tuple[int, int]

class _Cell:
    def __init__(self):
        self.parent = None
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')

def a_star(grid, start: Coord, goal: Coord):
    open_heap = []
    cell_info: Dict[Coord, _Cell] = {}

    def push(pos, g, h, parent):
        cell = cell_info.setdefault(pos, _Cell())
        cell.g = g
        cell.h = h
        cell.f = g + h
        cell.parent = parent
        heapq.heappush(open_heap, (cell.f, pos))

    push(start, 0.0, manhattan(start, goal), None)
    closed: Set[Coord] = set()

    while open_heap:
        f, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        if current == goal:
            path = []
            cur = current
            while cur is not None:
                path.append(cur)
                cur = cell_info[cur].parent
            path.reverse()
            return path

        closed.add(current)

        for nb in grid.neighbors(current):
            if nb in closed:
                continue
            g_new = cell_info[current].g + 1
            h_new = manhattan(nb, goal)
            info = cell_info.get(nb)
            if info is None or g_new < info.g:
                cell = cell_info.setdefault(nb, _Cell())
                cell.g = g_new
                cell.h = h_new
                cell.f = g_new + h_new
                cell.parent = current
                heapq.heappush(open_heap, (cell.f, nb))

    return None

def dijkstra_shortest_path(grid, start: Coord, goal: Coord, visited: Optional[Set[Coord]] = None):

    pq = []
    heapq.heappush(pq, (0, start))
    came_from: Dict[Coord, Optional[Coord]] = {start: None}
    cost_so_far: Dict[Coord, int] = {start: 0}

    while pq:
        _, current = heapq.heappop(pq)
        if current == goal:
            path = []
            c = current
            while c is not None:
                path.append(c)
                c = came_from[c]
            path.reverse()
            return path

        for nb in grid.neighbors(current):
            if visited is not None and nb not in visited:
                continue
            new_cost = cost_so_far[current] + 1
            if nb not in cost_so_far or new_cost < cost_so_far[nb]:
                cost_so_far[nb] = new_cost
                came_from[nb] = current
                heapq.heappush(pq, (new_cost, nb))

    return None

def choose_return_path_to_dump(grid, current: Coord, trash_bin: Coord):
    zero_cells = list(grid.zero_cells())
    if not zero_cells:
        return None

    best_total = float('inf')
    best_path = None

    zeros_set = set(zero_cells)

    for z in zero_cells:
        # path from current to z 
        p1 = dijkstra_shortest_path(grid, current, z)
        if p1 is None:
            continue
        # from z to start only using the cells with zero value
        p2 = dijkstra_shortest_path(grid, z, trash_bin, visited=zeros_set)
        if p2 is None:
            continue
        total = (len(p1) - 1) + (len(p2) - 1)
        if total < best_total:
            best_total = total
            best_path = p1 + p2[1:]

    return best_path
