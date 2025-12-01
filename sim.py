from grid import Grid
from robot import Robot

ROWS, COLS = 10, 12
RECHARGE = (0, 0)
START = (0, 0)
BATTERY_CAPACITY = 100
TRASH_CAPACITY = 15
VACUUM_COST_PER_UNIT = 1
MAX_STEPS = 500

def choose_trash_bin(recharge, rows, cols):
    r, c = recharge
    candidates = [(r, c + 1), (r + 1, c), (r, c - 1), (r - 1, c)]
    for cand in candidates:
        if 0 <= cand[0] < rows and 0 <= cand[1] < cols:
            return cand
    return recharge

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
    trash_bin = choose_trash_bin(RECHARGE, ROWS, COLS)

    grid.set(RECHARGE, 0)
    grid.set(trash_bin, 0)

    robot = Robot(
        grid,
        recharge=RECHARGE,
        trash_bin=trash_bin,
        start=START,
        battery_capacity=BATTERY_CAPACITY,
        bin_capacity=TRASH_CAPACITY,
        vacuum_cost_per_unit=VACUUM_COST_PER_UNIT,
    )

    step = 0
    while step < MAX_STEPS:
        if robot.at_trash() and robot.state == "RETURNING_TO_TRASH":
            robot.deposit()
            if any(True for _ in grid.nonzero_cells()):
                robot.state = "EXPLORING"
                robot.path = []
            else:
                print("All dust collected. Ending simulation.")
                break

        if robot.at_recharge() and robot.state == "RETURNING_TO_CHARGE":
            robot.charge()
            if any(True for _ in grid.nonzero_cells()):
                robot.state = "EXPLORING"
                robot.path = []
            else:
                print("All dust collected. Ending simulation.")
                break

        if robot.path:
            robot.follow_step()
        else:
            if robot.state == "EXPLORING":
                planned = robot.plan_explore()
                if not planned:
                    if robot.dust_collected > 0:
                        robot.state = "RETURNING_TO_TRASH"
                    else:
                        print("No more reachable dust to explore. Ending simulation.")
                        break
            elif robot.state == "RETURNING_TO_TRASH":
                if not robot.path:
                    if not robot.plan_return_to_trash():
                        robot.state = "RETURNING_TO_CHARGE"
                        if not robot.plan_return_to_charge():
                            print("Cannot plan path to trash or recharge. Ending simulation.")
                            break
                        
            elif robot.state == "RETURNING_TO_CHARGE":
                if not robot.path:
                    if not robot.plan_return_to_charge():
                        print("Cannot plan path to recharge. Ending simulation.")
                        break
        step += 1

    print(f"Simulation ended after {step} steps. Battery={robot.battery}, Dust collected ={robot.dust_collected}")
  

if __name__ == "__main__":
    run_sim()
