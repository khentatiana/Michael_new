from copy import deepcopy
import random


def make_choice(x, y, field):
    can_we_shoot = search_nearby_tanks(field, x, y)

    weights = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(can_we_shoot)):
        if can_we_shoot[i]:
            weights[i] += 20

    can_we_move = find_coin(x, y, field)
    for i in range(4, 8):
        if can_we_move[i - 4]:
            weights[i] += 50 / can_we_move[i - 4]

    # find which direction we need to go
    action = {
        0: 'fire_up',
        1: 'fire_down',
        2: 'fire_left',
        3: 'fire_right',
        4: 'move_up',
        5: 'move_down',
        6: 'move_left',
        7: 'move_right'
    }

    for i in range(8):
        weights[i] = [weights[i], action[i]]
    weights.sort(key=lambda val1, val2: val1[0] < val2[0])
    maximum = weights[-1]
    values = [maximum[1]]
    for i in range(6, -1, -1):
        if weights[i][0] == maximum[0]:
            values.append(weights[i][1])

    return random.choices(values)


def find_coin(row, col, array):
    d_grid = create_bfs_grid(row, col, array)
    min_path = 10000000
    loc = (-1, -1)

    for r in range(len(array)):
        for c in range(len(array[0])):
            if array[r][c] == 1:
                # we found a coin
                direct = direction(r, c, d_grid)
                if d_grid[r][c] < min_path:
                    min_path = d_grid[r][c]
                    loc = tuple(direct)
    # weights for the movement Up, Down, Left, and Right
    weights = [0, 0, 0, 0]
    locations = {
        (0, 1): 0,
        (0, -1): 1,
        (1, 0): 2,
        (-1, 0): 3
    }
    weights[locations[loc]] += 50 / min_path
    return weights


def create_bfs_grid(row, col, array):
    d_grid = [[-2] * len(array[0]) for _ in range(len(array))]

    d_grid[row][col] = 0
    # add starting search point to a queue
    q = [(row, col)]

    while len(q) > 0:
        # get new cell from the queue
        r, c = q.pop(0)
        # expand search to 4 adjacent neighbors
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):

            # if new cell out of bounds -> do not process
            if 0 <= nr < len(d_grid):
                if 0 <= nc < len(d_grid[0]):
                    # destination is either wall (-1) or has been visited then we ignore it
                    if type(array[nr][nc]) == dict:
                        continue
                    if d_grid[nr][nc] > -2:
                        continue
                    if array[nr][nc] == -1:
                        # if destination is wall mark it
                        d_grid[nr][nc] = -1
                    else:
                        # if destination is available - record number of steps to it
                        d_grid[nr][nc] = d_grid[r][c] + 1
                        q.append((nr, nc))
    return d_grid


def direction(r, c, d_grid):
    num_rows, num_cols = len(d_grid), len(d_grid[0])
    v = d_grid[r][c]
    prev = (r, c)
    while v > 0:
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= r + dr < num_rows:
                if 0 <= c + dc < num_cols:
                    if d_grid[r + dr][c + dc] == v - 1:
                        prev = (r, c)
                        r, c, v = r + dr, c + dc, v - 1
                        break

    return prev[0] - r, prev[1] - c


def search_nearby_tanks(grid, x, y):
    array = deepcopy(grid)
    width = len(array)
    length = len(array[0])

    # list of tanks that we can shoot. If we can shoot then we have True else False
    shooting_values = [False for _ in range(4)]

    # searching left, right, down, and up
    ranges = [range(x - 1, -1, -1), range(x + 1, width), range(0, y), range(y + 1, length)]

    # searching left and right
    for i in range(2):
        for j in ranges[i]:
            if array[j][y] == -1:
                break
            else:
                if type(array[j][y]) == dict:
                    shooting_values[i] = True

    for i in range(2, 4):
        for j in ranges[i]:
            if array[x][j] == -1:
                break
            else:
                if type(array[x][j]) == dict:
                    shooting_values[i] = True
    # returns the paths where the tank shoots and return which possible moves we can complete
    return shooting_values


grid = [
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0]
]

print(find_coin(2, 2, grid))

