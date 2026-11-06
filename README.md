# Warehouse Robot: A* Pathfinding Simulation

An autonomous warehouse robot that plans its own routes with the **A\* search algorithm**, collects every package on a randomly generated grid, and delivers them to the delivery station. It includes a live Tkinter dashboard that animates the robot and shows real-time statistics.

## Features
- **A\* pathfinding** with a Manhattan-distance heuristic and a min-heap priority queue (`heapq`)
- **Goal-driven robot loop**: repeatedly picks the nearest package, plans a path, moves, then heads to the delivery station
- **Random warehouse generator** with obstacles, packages, and a delivery station
- **Solvability check**: the generator re-rolls any layout where a package or the station is walled off
- **Live GUI dashboard** (dark theme) with Start and Regenerate controls
- **Real-time metrics**: steps taken, A\* nodes explored, and mission time

## Tech Stack
Python 3 · Tkinter · `heapq` · Object-Oriented Design

## How It Works
1. The grid (12×12) is filled with random obstacles and 5 packages. The robot starts at the top-left and the delivery station is at the bottom-right.
2. The robot picks the nearest package (Manhattan distance) and calls `astar.find_path()` to get the shortest obstacle-free route.
3. It follows the path step by step. Each move redraws the GUI through a callback hook, so the simulation logic stays separate from the interface.
4. After all packages are collected, A\* plans the final route to the delivery station and the mission statistics are shown.

## Project Structure
```
├── astar.py   # A* algorithm (heuristic, open/closed sets, path reconstruction)
├── main.py    # WarehouseSimulation class: robot state, mission loop, statistics
└── gui.py     # Tkinter dashboard: rendering, controls, random layout generation
```

## Setup
```bash
git clone https://github.com/YOUR-USERNAME/warehouse-robot-astar.git
cd warehouse-robot-astar
python gui.py
```
No external libraries are required. Tkinter ships with Python (on Linux you may need `sudo apt install python3-tk`).

## Results
Tested on 2,000 random 12×12 grids: A\* returned the same path length as a breadth-first search on every case. Over 300 full missions, the robot averaged about 37 steps and about 72 explored nodes, and A\* solved a path in under 1 ms.

## Demo
_Add a screenshot or GIF of the dashboard here._

## Future Improvements
- Visit packages in an optimal order (Traveling Salesman heuristics) instead of nearest-first
- Add weighted terrain and diagonal movement
- Support multiple robots with collision avoidance
- Add an LLM-powered natural-language interface (for example, "collect the packages in the top row first") that turns commands into tasks for the robot
