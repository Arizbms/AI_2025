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
