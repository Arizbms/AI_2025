import heapq

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

def is_valid(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

# --------- Heuristics ---------
def manhattan_distance(state):
    d = 0
    for i in range(3):
        for j in range(3):
            v = state[i][j]
            if v != 0:
                gx, gy = divmod(v - 1, 3)
                d += abs(i - gx) + abs(j - gy)
    return d

def misplaced_tiles(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                count += 1
    return count

# --------- A* Search ---------
def a_star(start, heuristic):
    visited = set()
    pq = []
    heapq.heappush(pq, (heuristic(start), 0, start, []))
    while pq:
        f, g, state, path = heapq.heappop(pq)
        if state == goal_state:
            return path + [state]
        visited.add(state_to_tuple(state))
        x, y = find_blank(state)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                if state_to_tuple(new_state) not in visited:
                    g2 = g + 1
                    f2 = g2 + heuristic(new_state)
                    heapq.heappush(pq, (f2, g2, new_state, path + [state]))
    return None

# --------- Solver ---------
def solve(start, method="astar_manhattan"):
    if method == "astar_misplaced":
        return a_star(start, misplaced_tiles)
    else: # default: A* Manhattan
        return a_star(start, manhattan_distance)

# --------- Example Run ---------
start_state = [[1, 2, 3],
               [0, 4, 6],
               [7, 5, 8]]

for algo in ["astar_misplaced", "astar_manhattan"]:
    print("\nMethod:", algo)
    path = solve(start_state, algo)
    if path:
        print("Solved in", len(path) - 1, "moves")
        for step in path:
            for row in step: print(row)
            print("-----")
    else:
        print("No solution found")
