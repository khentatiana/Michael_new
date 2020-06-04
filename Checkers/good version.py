array = {}

# we draw our checkers in their respective locations
for curr_range in [[range(0, 3), 'B'], [range(5, 8), 'W']]:
    # creates pieces in relation to the current range

    for r in curr_range[0]:
        # We check if the row is even or odd if even we must 1, 3, 5, 7 as the column locations
        # of the checker pieces else if odd we have 0, 2, 4, 6 as the checker column locations
        if r % 2 == 1:
            # odd row
            is_odd = True
        else:
            # even row
            is_odd = False

        # we loop through the current row
        for c in range(8):
            if is_odd:
                # the row is odd
                if c % 2 == 0:
                    # we place a checker
                    array[(r, c)] = curr_range[1]
                else:
                    # we set it as a blank space
                    array[(r, c)] = '_'
            else:
                # the row is even
                if c % 2 == 1:
                    # we place a checker
                    array[(r, c)] = curr_range[1]
                else:
                    # we set it as a blank space
                    array[(r, c)] = '_'

# we fill the middle section with blank spaces
for r in range(3, 5):
    # we loop through the current row
    for c in range(8):
        array[(r, c)] = '_'

print(array)

for r in range(8):
    for c in range(8):
        print(array[(r, c)], end=' ')
    print()

array = {(0, 0): '_', (0, 1): 'B', (0, 2): '_', (0, 3): 'B', (0, 4): '_', (0, 5): 'B', (0, 6): '_', (0, 7): 'B',
         (1, 0): 'B', (1, 1): '_', (1, 2): 'B', (1, 3): '_', (1, 4): 'B', (1, 5): '_', (1, 6): 'B', (1, 7): '_',
         (2, 0): '_', (2, 1): 'B', (2, 2): '_', (2, 3): 'B', (2, 4): '_', (2, 5): 'B', (2, 6): '_', (2, 7): 'B',
         (3, 0): '_', (3, 1): '_', (3, 2): '_', (3, 3): '_', (3, 4): '_', (3, 5): '_', (3, 6): '_', (3, 7): '_',
         (4, 0): '_', (4, 1): '_', (4, 2): '_', (4, 3): '_', (4, 4): '_', (4, 5): '_', (4, 6): '_', (4, 7): '_',
         (5, 0): 'W', (5, 1): '_', (5, 2): 'W', (5, 3): '_', (5, 4): 'W', (5, 5): '_', (5, 6): 'W', (5, 7): '_',
         (6, 0): '_', (6, 1): 'W', (6, 2): '_', (6, 3): 'W', (6, 4): '_', (6, 5): 'W', (6, 6): '_', (6, 7): 'W',
         (7, 0): 'W', (7, 1): '_', (7, 2): 'W', (7, 3): '_', (7, 4): 'W', (7, 5): '_', (7, 6): 'W', (7, 7): '_'}
