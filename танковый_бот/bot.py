import random


def make_choice(x, y, field):
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

    if tanks_near_me.count(True) > 0:
        # we can shoot a tank so we shoot it or if we can shoot multiple then we choose a random one
        tanks_to_shoot = []
        actions = {
            0: 'fire_left',
            1: 'fire_right',
            2: 'fire_up',
            3: 'fire_down'
        }

        for i in range(4):
            if tanks_near_me[i]:
                tanks_to_shoot.append(actions[i])

        return random.choice(tanks_to_shoot)
    else:
        return 'go_up'


if __name__ == "__main__":
    T = {"life": 10}
    my_field = [
        [0,0,0,0],
        [0,T,0,1],
        [0,0,T,0],
        [0,0,0,0]
    ]
    my_x = 1
    my_y = 1
    res = make_choice(my_x, my_y, my_field)
    print(res)
