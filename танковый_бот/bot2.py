import random


def make_choice(x, y, field):
    actions = ["fire_up", "fire_down", "fire_left", "fire_right", "go_up", "go_down", "go_left", "go_right"]

    weights = [[0, 0]] * 8

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

    movements, coordinates = search_movement(field, [x, y])
    paths = search_nearby_tanks(field, x, y)

    for i in range(4, 8):
        # movement weights
        weights[i][0] += movements[i - 4]

    # check tank locations
    for loc in coordinates:
        if paths.count(loc) > 0:
            weights[coordinates.index(loc)][0] -= 15

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
    possible_choices = ['go_left', 'go_right', 'go_up', 'go_down']
    weights.sort()
    val = weights[-1][0]

    for i in range(8):
        if val != weights[i][0]:
            break
        if len(possible_choices) == 0:
            possible_choices = []
        possible_choices.append(actions[weights[i][1]])

    return random.choice(possible_choices)


def search_movement(array, loc):
    # we create a cushion in-case we are on the border
    array.insert(0, ['#'] * (2 + len(array)))
    array.append(['#'] * (2 + len(array)))

    for i in range(1, len(array) - 1):
        array[i].insert(0, '#')
        array[i].append('#')

    # we search possible sectors
    weights = [0, 0, 0, 0]
    coordinates = [(loc[0], loc[1] + 1), (loc[0], loc[1] - 1), (loc[0] - 1, loc[1]), (loc[0] + 1, loc[1])]

    if array[loc[0], loc[1] + 1] in [0, 1]:
        if array[loc[0], loc[1] + 1] == 1:
            weights[0] += 50
    else:
        weights[0] -= 100

    if array[loc[0], loc[1] - 1] in [0, 1]:
        if array[loc[0], loc[1] - 1] == 1:
            weights[0] += 50
    else:
        weights[0] -= 100

    if array[loc[0] - 1, loc[1]] in [0, 1]:
        if array[loc[0] - 1, loc[1]] == 1:
            weights[0] += 50
    else:
        weights[0] -= 100

    if array[loc[0] + 1, loc[1]] in [0, 1]:
        if array[loc[0] + 1, loc[1]] == 1:
            weights[0] += 50
    else:
        weights[0] -= 100

    return weights, coordinates


def search_nearby_tanks(grid, x, y):
    width = len(grid)
    length = len(grid[0])

    # list of tanks that we can shoot. If we can shoot then we have True else False
    sides = [[] * 4]

    # searching left, right, down, and up
    ranges = [range(x - 1, -1, -1), range(x + 1, width), range(0, y), range(y + 1, length)]

    # searching left and right
    for i in range(2):
        for j in ranges[i]:
            if grid[j][y] == -1:
                break
            else:
                sides[i].append((j, y))

    for i in range(2, 4):
        for j in ranges[i]:
            if grid[x][j] == -1:
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
