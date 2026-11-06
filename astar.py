import heapq

def heuristic(a, b):
    """Calculates Manhattan distance between two coordinate tuples (x, y)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(start, goal, obstacles, width, height):
    """
    Finds the shortest path from start to goal using the A* algorithm.
    Returns a tuple: (path as a list of coordinates, number of nodes explored)
    """
    # Priority queue storing elements as: (f_score, current_node)
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    # Track where each node came from to reconstruct the path later
    came_from = {}
    
    # g_score: cost from start to current node (defaults to infinity)
    g_score = {start: 0}
    
    # f_score: estimated total cost from start to goal through current node
    f_score = {start: heuristic(start, goal)}
    
    # Track nodes that have been evaluated to avoid duplicate work
    closed_set = set()
    nodes_explored = 0
    while open_set:
        _, current = heapq.heappop(open_set)

        # Skip stale duplicates of nodes that were already expanded
        if current in closed_set:
            continue
        nodes_explored += 1

        # If goal is reached, reconstruct and return the optimal path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, nodes_explored

        closed_set.add(current)

        # 4-way movement directions: Up, Down, Left, Right
        neighbors = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1)
        ]

        for neighbor in neighbors:
            nx, ny = neighbor
            
            # Boundary check
            if not (0 <= nx < width and 0 <= ny < height):
                continue
                
            # Obstacle check
            if neighbor in obstacles:
                continue
                
            # Skip if already fully evaluated
            if neighbor in closed_set:
                continue

            # Every valid step costs exactly 1 unit
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                
                # Always push the improved score. Older, worse entries for the
                # same node are skipped later because it will already be closed.
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # Return None if no valid path exists through the maze
    return None, nodes_explored
