# Robot Explorer Simulator


Simulates a robot exploring a grid world collecting dust. When the robot's dust collection reaches a threshold it returns to the recharge point to deposit, choosing a return path by reaching a cleaned cell as soon as possible and thereafter stays on cleaned cells to the recharge point. The robot prefers moving to uncleaned cells during exploration.


Run:


```bash
python sim.py