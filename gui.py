import tkinter as tk
import random
import time
import astar
from main import WarehouseSimulation
class WarehouseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Logistics Automation Dashboard")
        
        # Hardcoded Permanent Dark Mode Palette
        self.palette = {
            "bg": "#1A252F", 
            "header": "#11171D", 
            "text": "#ECF0F1", 
            "canvas": "#233241",
            "grid_line": "#2C3E50", 
            "empty_cell": "#2C3E50", 
            "obstacle": "#4A5768"
        }
        self.cell_size = 40
        self.sim = WarehouseSimulation(12, 12)
        self.sim.set_gui_callback(self.draw_warehouse)
        self.root.configure(bg=self.palette["bg"])
        self.control_frame = tk.Frame(root, bg=self.palette["header"])
        self.control_frame.pack(side=tk.TOP, fill=tk.X, ipady=8)
        button_style = {"font": ("Segoe UI", 10, "bold"), "fg": "white", "bd": 0, "padx": 12, "pady": 6, "activebackground": "#1A252F"}
        self.start_btn = tk.Button(self.control_frame, text="START MISSION", bg="#2ECC71", **button_style, command=self.run_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        self.regen_btn = tk.Button(self.control_frame, text="REGENERATE", bg="#3498DB", **button_style, command=self.generate_warehouse)
        self.regen_btn.pack(side=tk.LEFT, padx=5)
        self.stats_label = tk.Label(self.control_frame, text="Steps: 0  |  Nodes: 0  |  Time: 0.00s", font=("Segoe UI", 11, "bold"), fg=self.palette["text"], bg=self.palette["header"])
        self.stats_label.pack(side=tk.RIGHT, padx=15)
        self.canvas = tk.Canvas(root, width=12*self.cell_size, height=12*self.cell_size, bg=self.palette["canvas"], highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)
        self.generate_warehouse()
    def generate_warehouse(self):
        """Randomly places obstacles and packages, retrying until every
        package and the delivery station are reachable from the robot."""
        while True:
            self.sim.packages.clear()
            self.sim.obstacles.clear()
            self.sim.robot_pos = (0, 0)
            self.sim.total_steps = 0
            self.sim.nodes_explored = 0
            self.sim.execution_time = 0.0
            while len(self.sim.obstacles) < 15:
                pos = (random.randint(0, 11), random.randint(0, 11))
                if pos != (0, 0) and pos != self.sim.delivery_station:
                    self.sim.obstacles.add(pos)
            while len(self.sim.packages) < 5:
                pos = (random.randint(0, 11), random.randint(0, 11))
                if pos != (0, 0) and pos != self.sim.delivery_station and pos not in self.sim.obstacles:
                    self.sim.packages.add(pos)
            if self._all_targets_reachable():
                break
        self.draw_warehouse()

    def _all_targets_reachable(self):
        """Checks that A* can reach every package and the delivery station."""
        targets = list(self.sim.packages) + [self.sim.delivery_station]
        for target in targets:
            path, _ = astar.find_path(
                self.sim.robot_pos, target,
                self.sim.obstacles, self.sim.width, self.sim.height
            )
            if path is None:
                return False
        return True

    def draw_warehouse(self):
        """Renders grid tiles using the emoji icons inside the dark theme window."""
        self.canvas.delete("all")  
        for y in range(self.sim.height):
            for x in range(self.sim.width):
                x1, y1 = x * self.cell_size, y * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.palette["empty_cell"], outline=self.palette["grid_line"])              
                pos = (x, y)
                cx, cy = x1 + self.cell_size // 2, y1 + self.cell_size // 2                
                if pos in self.sim.obstacles:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.palette["obstacle"], outline=self.palette["grid_line"])
                    self.canvas.create_text(cx, cy, text="🚧", font=("Segoe UI", 14))
                elif pos == self.sim.delivery_station:
                    self.canvas.create_text(cx, cy, text="🏢", font=("Segoe UI", 18))
                elif pos in self.sim.packages:
                    self.canvas.create_text(cx, cy, text="📦", font=("Segoe UI", 18))
                if pos == self.sim.robot_pos:
                    self.canvas.create_text(cx, cy, text="🤖", font=("Segoe UI", 18))
        self.stats_label.config(
            text=f"Steps: {self.sim.total_steps}  |  Nodes: {self.sim.nodes_explored}  |  Time: {self.sim.execution_time:.2f}s"
        )
        self.root.update_idletasks() 
    def run_simulation(self):
        """Disables controls and runs the logic loop safely inside the main thread."""
        self.start_btn.config(state=tk.DISABLED, bg="#7F8C8D")
        self.regen_btn.config(state=tk.DISABLED, bg="#7F8C8D")
        
        original_sleep = time.sleep
        time.sleep = lambda seconds: (self.root.update(), original_sleep(seconds))     
        self.sim.start_robot()     
        time.sleep = original_sleep
        self.start_btn.config(state=tk.NORMAL, bg="#2ECC71")
        self.regen_btn.config(state=tk.NORMAL, bg="#3498DB")
        self.draw_warehouse()
if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseGUI(root)
    root.mainloop()
