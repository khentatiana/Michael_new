import random
from copy import deepcopy
from queue import *


def make_choice(x, y, field):
    weights = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    for i in range(8):
        weights[i][1] = i

    width = len(field)
    length = len(field[0])
    # list of tanks that we can shoot. If we can shoot then we have True else False
    tanks_near_me = [False] * 4

    # searching left, right, down, and up
    ranges = [range(x - 1, -1, -1), range(x + 1, width), range(0, y), range(y + 1, length)]

    # searching left and right
    for i in range(2):
        for j in ranges[i]:
            if field[j][y] == -1:
                break
            elif type(field[j][y]) == dict:
                # we found a tank
                tanks_near_me[i] = True

    for i in range(2, 4):
        for j in ranges[i]:
            if field[x][j] == -1:
                break
            elif type(field[x][j]) == dict:
                # we found a tank
                tanks_near_me[i] = True

    for i in range(4):
        if tanks_near_me[i]:
            # we can shoot
            weights[i][0] += 20

    actions = {
        "fire_up": 0,
        "fire_down": 1,
        "fire_left": 2,
        "fire_right": 3,
        "go_up": 4,
        "go_down": 5,
        "go_left": 6,
        "go_right": 7
    }

    movements, coordinates = search_movement(field, [x, y])
    paths = search_nearby_tanks(field, x, y)
    move_to_nearest_coin, steps = bfs(field, x, y)

    for i in range(4, 8):
        # movement weights
        weights[i][0] += movements[i - 4]

    # check tank locations
    for loc in coordinates:
        if paths.count(loc) > 0:
            weights[coordinates.index(loc)][0] -= 15

    weights[actions[move_to_nearest_coin]][0] = 50 / steps

    actions = {
        0: "fire_up",
        1: "fire_down",
        2: "fire_left",
        3: "fire_right",
        4: "go_up",
        5: "go_down",
        6: "go_left",
        7: "go_right"
    }
    weights.sort()
    val = weights[-1][0]
    possible_choices = [actions[weights[-1][1]]]

    for i in range(6, -1, -1):
        if val != weights[i][0]:
            break
        possible_choices.append(actions[weights[i][1]])

    return random.choice(possible_choices)


def bfs(grid, x, y):
    array = deepcopy(grid)

    q = Queue()
    q.put((x + 1, y, "go_right", 1))
    q.put((x - 1, y, "go_left", 1))
    q.put((x, y + 1, "go_down", 1))
    q.put((x, y - 1, "go_up", 1))

    # build a cushion of walls
    array.insert(0, [-1] * (2 + len(array)))
    array.append([-1] * (1 + len(array)))

    for i in range(1, len(array) - 1):
        array[i].insert(0, -1)
        array[i].append(-1)

    visited = []

    while not q.empty():
        # complete BFS search
        val = q.get()

        # check if we have been at this point before
        if tuple([val[0], val[1]]) in list(filter(lambda e: e[0] == val[0] and e[1] == val[1], visited)):
            continue

        if type(array[val[0]][val[1]]) == dict:
            # we found a tank
            visited.append(val)
            continue
        elif array[val[0]][val[1]] == - 1:
            # we found a wall
            visited.append(val)
            continue
        elif array[val[0]][val[1]] == 1:
            # we found a coin
            return val[2], val[3]
        else:
            # we add the neighbors

            q.put((val[0] + 1, val[1], val[2], val[3] + 1))
            q.put((val[0] - 1, val[1], val[2], val[3] + 1))
            q.put((val[0], val[1] + 1, val[2], val[3] + 1))
            q.put((val[0], val[1] - 1, val[3], val[3] + 1))

    return None, None


def search_movement(grid, loc):
    array = deepcopy(grid)
    # we create a cushion in-case we are on the border11
    array.insert(0, ['#'] * (2 + len(array)))
    array.append(['#'] * (2 + len(array)))

    for i in range(1, len(array) - 1):
        array[i].insert(0, '#')
        array[i].append('#')

    # we search possible sectors
    weights = [0, 0, 0, 0]
    coordinates = [(loc[0], loc[1] + 1), (loc[0], loc[1] - 1), (loc[0] - 1, loc[1]), (loc[0] + 1, loc[1])]

    if array[loc[0]][loc[1] + 1] in [0, 1]:
        if array[loc[0]][loc[1] + 1] == 1:
            weights[0] += 50
    else:
        weights[0] -= 100

    if array[loc[0]][loc[1] - 1] in [0, 1]:
        if array[loc[0]][loc[1] - 1] == 1:
            weights[1] += 50
    else:
        weights[1] -= 100

    if array[loc[0] - 1][loc[1]] in [0, 1]:
        if array[loc[0] - 1][loc[1]] == 1:
            weights[2] += 50
    else:
        weights[2] -= 100

    if array[loc[0] + 1][loc[1]] in [0, 1]:
        if array[loc[0] + 1][loc[1]] == 1:
            weights[3] += 50
    else:
        weights[3] -= 100

    return weights, coordinates


def search_nearby_tanks(grid, x, y):
    array = deepcopy(grid)
    width = len(array)
    length = len(array[0])

    # list of tanks that we can shoot. If we can shoot then we have True else False
    sides = [[], [], [], []]

    # searching left, right, down, and up
    ranges = [range(x - 1, -1, -1), range(x + 1, width), range(0, y), range(y + 1, length)]

    # searching left and right
    for i in range(2):
        for j in ranges[i]:
            if array[j][y] == -1:
                break
            else:
                sides[i].append((j, y))

    for i in range(2, 4):
        for j in ranges[i]:
            if array[x][j] == -1:
                break
            else:
                sides[i].append((x, j))

    # returns the paths where the tank shoots
    return sides


if __name__ == '__main__':
    T = {"life": 10}
    my_field = [
        [0, 0, 0, 0],
        [0, T, 0, 1],
        [0, 0, T, 0],
        [0, 0, 0, 0]
    ]
    my_x = 1
    my_y = 1
    res = make_choice(my_x, my_y, my_field)
    print(res)
