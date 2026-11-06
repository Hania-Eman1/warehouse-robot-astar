# ==========================================
# main.py
# AI Warehouse Robot Simulation
# Random Warehouse Generator
# ==========================================

import random
import time


import astar


# ==========================================
# CONFIGURATION
# ==========================================

GRID_SIZE = 12

MIN_PACKAGES = 6
MAX_PACKAGES = 10

OBSTACLE_PERCENTAGE = 18


# ==========================================
# CREATE EMPTY GRID
# ==========================================

def create_empty_grid():

    return [

        ["." for _ in range(GRID_SIZE)]

        for _ in range(GRID_SIZE)

    ]


# ==========================================
# GET RANDOM EMPTY CELL
# ==========================================

def random_empty_cell(grid):

    while True:

        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)

        if grid[row][col] == ".":

            return (row, col)


# ==========================================
# PLACE ROBOT
# ==========================================

def place_robot(grid):

    row, col = random_empty_cell(grid)

    grid[row][col] = "R"

    return (row, col)


# ==========================================
# PLACE DELIVERY STATION
# ==========================================

def place_delivery(grid):

    row, col = random_empty_cell(grid)

    grid[row][col] = "D"

    return (row, col)


# ==========================================
# PLACE PACKAGES
# ==========================================

def place_packages(grid):

    package_locations = []

    total = random.randint(

        MIN_PACKAGES,

        MAX_PACKAGES

    )

    for _ in range(total):

        row, col = random_empty_cell(grid)

        grid[row][col] = "P"

        package_locations.append(

            (row, col)

        )

    return package_locations


# ==========================================
# PLACE RANDOM OBSTACLES
# ==========================================

def place_obstacles(grid):

    total_cells = GRID_SIZE * GRID_SIZE

    obstacles = int(

        total_cells *

        OBSTACLE_PERCENTAGE / 100

    )

    count = 0

    while count < obstacles:

        row = random.randint(

            0,

            GRID_SIZE - 1

        )

        col = random.randint(

            0,

            GRID_SIZE - 1

        )

        if grid[row][col] == ".":

            grid[row][col] = "#"

            count += 1


# ==========================================
# GENERATE RANDOM WAREHOUSE
# ==========================================

def generate_random_warehouse():

    grid = create_empty_grid()

    robot = place_robot(grid)

    delivery = place_delivery(grid)

    packages = place_packages(grid)

    place_obstacles(grid)

    return (

        grid,

        robot,

        delivery,

        packages

    )


# ==========================================
# DISPLAY GRID
# ==========================================

def display_grid(grid):

    symbols = {

        "R": "🤖",

        "P": "📦",

        "D": "🚚",

        "#": "⬛",

        ".": "⬜"

    }

    print()

    print("=" * 45)

    print("     AI WAREHOUSE ROBOT (A*)")

    print("=" * 45)

    print()

    for row in grid:

        for cell in row:

            print(

                symbols[cell],

                end=" "

            )

        print()

    print()
    # ==========================================
# FIND ROBOT
# ==========================================

def find_robot(grid):

    for row in range(len(grid)):

        for col in range(len(grid[0])):

            if grid[row][col] == "R":

                return (row, col)

    return None


# ==========================================
# FIND ALL PACKAGES
# ==========================================

def find_packages(grid):

    packages = []

    for row in range(len(grid)):

        for col in range(len(grid[0])):

            if grid[row][col] == "P":

                packages.append((row, col))

    return packages


# ==========================================
# FIND DELIVERY STATION
# ==========================================

def find_delivery(grid):

    for row in range(len(grid)):

        for col in range(len(grid[0])):

            if grid[row][col] == "D":

                return (row, col)

    return None


# ==========================================
# CHECK IF ALL GOALS ARE REACHABLE
# ==========================================

def warehouse_is_valid(grid):

    robot = find_robot(grid)

    packages = find_packages(grid)

    delivery = find_delivery(grid)

    if robot is None:

        return False

    if delivery is None:

        return False

    if len(packages) == 0:

        return False


    # Every package must be reachable

    for package in packages:

        path, _ = astar(

            grid,

            robot,

            package

        )

        if path is None:

            return False


    # Delivery must also be reachable

    path, _ = astar(

        grid,

        robot,

        delivery

    )

    if path is None:

        return False


    return True


# ==========================================
# CREATE VALID RANDOM WAREHOUSE
# ==========================================

def create_valid_warehouse():

    while True:

        grid, robot, delivery, packages = generate_random_warehouse()

        if warehouse_is_valid(grid):

            return grid


# ==========================================
# MOVE ROBOT
# ==========================================

def move_robot(grid, path):

    for position in path[1:]:

        old_row, old_col = find_robot(grid)

        new_row, new_col = position


        # Restore old cell

        grid[old_row][old_col] = "."


        # If robot reaches package

        if grid[new_row][new_col] == "P":

            print("📦 Package Collected!")


        # If robot reaches delivery

        if grid[new_row][new_col] == "D":

            print("🚚 Delivery Station Reached!")


        grid[new_row][new_col] = "R"


        display_grid(grid)

        time.sleep(0.25)

class WarehouseSimulation:
    def __init__(self, width=12, height=12):
        self.width = width
        self.height = height
        self.robot_pos = (0, 0)
        self.delivery_station = (width - 1, height - 1)
        self.packages = set()  # Set of (x, y) coordinates
        self.obstacles = set() # Set of (x, y) coordinates
        
        # Statistics
        self.total_steps = 0
        self.nodes_explored = 0
        self.execution_time = 0.0
        
        # GUI callback hook (assigned by gui.py)
        self.on_update_callback = None

    def set_gui_callback(self, callback):
        """Connects the simulation to the GUI for real-time animation."""
        self.on_update_callback = callback

    def trigger_gui_update(self):
        """Helper to invoke GUI redraws if a callback is registered."""
        if self.on_update_callback:
            self.on_update_callback()

    def get_nearest_package(self):
        """Finds the Manhattan distance closest package to the robot."""
        if not self.packages:
            return None
        rx, ry = self.robot_pos
        return min(self.packages, key=lambda p: abs(p[0] - rx) + abs(p[1] - ry))

    def remove_collected_package(self, position):
        """Removes a package from the grid once the robot reaches it."""
        if position in self.packages:
            self.packages.remove(position)
            self.trigger_gui_update()

    def execute_path(self, path):
        """Moves the robot along a path, updating stats and triggering GUI."""
        if not path:
            return False
            
        for position in path[1:]:
            self.robot_pos = position
            self.total_steps += 1
            self.trigger_gui_update()
            time.sleep(0.15)
        return True

    def start_robot(self):
        """Main mission loop: collects all packages, then goes to delivery."""
        import astar  # Ensure the astar module is imported
        start_clock = time.time()
        
        # Phase 1: Collect all packages
        while self.packages:
            target = self.get_nearest_package()
            
            # CALL REAL A* PATHFINDING HERE:
            result = astar.find_path(self.robot_pos, target, self.obstacles, self.width, self.height)
            path, nodes_visited = result
            
            if not path:
                print("Error: Target package unreachable!")
                return False
                
            self.nodes_explored += nodes_visited
            if not self.execute_path(path):
                return False
                
            self.remove_collected_package(target)

        # Phase 2: Head to delivery station
        if self.robot_pos != self.delivery_station:
            # CALL REAL A* PATHFINDING HERE:
            result = astar.find_path(self.robot_pos, self.delivery_station, self.obstacles, self.width, self.height)
            path, nodes_visited = result
            
            if not path:
                print("Error: Delivery station unreachable!")
                return False
                
            self.nodes_explored += nodes_visited
            self.execute_path(path)

        self.execution_time = time.time() - start_clock
        print(f"Mission Complete! Steps: {self.total_steps}, Nodes: {self.nodes_explored}, Time: {self.execution_time:.2f}s")
        return True


if __name__ == "__main__":
    sim = WarehouseSimulation()
    sim.packages.add((2, 3))
    sim.packages.add((5, 5))
    sim.obstacles.add((1, 1))
    sim.start_robot()
