from grid import Grid
from robot import Robot

ROWS, COLS = 10, 12
RECHARGE = (0, 0)
START = (0, 0)
CAPACITY = 15
THRESHOLD = 15  
MAX_STEPS = 1000


def create_example_grid(rows, cols):
    import random
    random.seed(0)
    grid = Grid(rows, cols)
    for r in range(rows):
        for c in range(cols):
            grid.set((r, c), random.choice([0]*6 + [1,2,3,4,5]))
    grid.set(START, 0)
    return grid


def run_sim():
    grid = create_example_grid(ROWS, COLS)
    robot = Robot(grid, RECHARGE, START, capacity=CAPACITY)

    step = 0
    while step < MAX_STEPS:
        step += 1

        if not robot.path:
            if robot.dust_collected < THRESHOLD:
                #Explore to collect dust
                planned = robot.plan_explore()
                if not planned:
                    print("Exploration complete: All the dust is cleaned.")
                    break

        robot.follow_step()
        grid.set(robot.pos, 0)  # clean the cell
        if robot.dust_collected >= THRESHOLD and not robot.at_recharge():
            planned = robot.plan_return()
            if not planned:
                    # direct dijkstra to start
                    from pathfinding import dijkstra_shortest_path
                    p = dijkstra_shortest_path(grid, robot.pos, robot.recharge)
                    if p:
                        robot.path = p[1:] 
                    else:
                        print("Return to recharge failed: No path found.")
                        break
        elif robot.at_recharge() and robot.dust_collected > 0:
            robot.deposit()
    print(f"Simulation ended after {step} steps.")
if __name__ == '__main__':
    run_sim()
