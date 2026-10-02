from collections import deque

def run_agent():
    warehouse_map = [
        "#####################",
        "#S....#............G#",
        "#.##....##########..#",
        "#....##.............#",
        "#.######.###.#.###..#",
        "#........#..........#",
        "#####################",
    ]
    grid = [list(row) for row in warehouse_map]
    rows = len(grid)
    cols = len(grid[0])
    start = None
    goal = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "G":
                goal = (r, c)
    frontier = deque([start])
    came_from = {start: None}
    visited = {start}
    moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
    found = False
    while frontier:
        curr = frontier.popleft()
        if curr == goal:
            found = True
            break
        r, c = curr
        for dr, dc, name in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                nxt = (nr, nc)
                if nxt not in visited:
                    visited.add(nxt)
                    came_from[nxt] = (curr, name)
                    frontier.append(nxt)
    if not found:
        print("No path exists.")
        return
    path = []
    actions = []
    curr = goal
    while curr != start:
        prev, move_name = came_from[curr]
        path.append(curr)
        actions.append(move_name)
        curr = prev
    path.append(start)
    path.reverse()
    actions.reverse()
    print("Path found!")
    print(f"Path coordinates: {path}")
    print(f"Actions taken: {actions}")

if __name__ == "__main__":
    run_agent()