import heapq
from collections import deque
import math

class WarehouseProblem:
    def __init__(self, map_str):
        self.grid = [list(line) for line in map_str.strip().split('\n')]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.start = None
        self.goal = None
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'S':
                    self.start = (r, c)
                elif self.grid[r][c] == 'G':
                    self.goal = (r, c)
                    
    def get_neighbors(self, state):
        r, c = state
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != '#':
                neighbors.append((nr, nc))
        return neighbors

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def astar_search(problem, heuristic_func):
    start = problem.start
    goal = problem.goal
    
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    g_score = {start: 0}
    states_expanded = 0
    expanded = set()
    
    while frontier:
        _, current = heapq.heappop(frontier)
        if current in expanded:
            continue
        expanded.add(current)
        states_expanded += 1
        
        if current == goal:
            return reconstruct_path(came_from, current), states_expanded
            
        for neighbor in problem.get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic_func(neighbor, goal)
                heapq.heappush(frontier, (f_score, neighbor))
                
    return None, states_expanded

def bfs_search(problem):
    start = problem.start
    goal = problem.goal
    
    frontier = deque([start])
    came_from = {}
    visited = {start}
    states_expanded = 0
    
    while frontier:
        current = frontier.popleft()
        states_expanded += 1
        
        if current == goal:
            return reconstruct_path(came_from, current), states_expanded
            
        for neighbor in problem.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                frontier.append(neighbor)
                
    return None, states_expanded

def h_manhattan(state, goal):
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

def h_zero(state, goal):
    return 0

def h_euclidean(state, goal):
    return math.sqrt((state[0] - goal[0])**2 + (state[1] - goal[1])**2)

def h_manhattan_x2(state, goal):
    return 2 * h_manhattan(state, goal)

def run_tests():
    map_original = """
#################
#S....#.........#
#.###.#.#######.#
#...#.#.......#.#
###.#.#######.#.#
#...#.........#.#
#.###########.#.#
#.............#G#
#################
"""
    map_trivial = """
#####
#SG##
#####
"""
    map_no_solution = """
#######
#S....#
###.###
#...#G#
#######
"""
    map_alternative = """
#######
#S....#
#.#.#.#
#....G#
#######
"""

    tests = [
        ("Test 1: Original", map_original),
        ("Test 2: Trivial", map_trivial),
        ("Test 3: No Solution", map_no_solution),
        ("Test 4: Alternative Paths", map_alternative)
    ]
    
    for name, m in tests:
        print(f"--- {name} ---")
        problem = WarehouseProblem(m)
        path, expanded = astar_search(problem, h_manhattan)
        if path:
            print(f"Path found! Length: {len(path)-1}, States Expanded: {expanded}")
        else:
            print(f"No path found. States Expanded: {expanded}")

    print("\n--- BFS vs A* (Original Map) ---")
    problem = WarehouseProblem(map_original)
    bfs_path, bfs_exp = bfs_search(problem)
    astar_path, astar_exp = astar_search(problem, h_manhattan)
    print(f"BFS: Length {len(bfs_path)-1}, Expanded {bfs_exp}")
    print(f"A* : Length {len(astar_path)-1}, Expanded {astar_exp}")
    
    print("\n--- Heuristic Investigation (Original Map) ---")
    heuristics = [
        ("h(n) = 0 (Uniform Cost)", h_zero),
        ("h(n) = Manhattan", h_manhattan),
        ("h(n) = Euclidean", h_euclidean),
        ("h(n) = 2 * Manhattan", h_manhattan_x2)
    ]
    for h_name, h_func in heuristics:
        path, exp = astar_search(problem, h_func)
        length = len(path)-1 if path else "N/A"
        print(f"{h_name:25s} | Length: {length} | Expanded: {exp}")

if __name__ == "__main__":
    run_tests()
