def print_board(board):
    """function that prints the game board returns None"""

    # print the header (column numbers so to speak)
    print('0 1 2 3 4 5 6')

    # print the content of the board
    for row in board:
        print(' '.join(row))


def get_diagonals(board):
    """Helper function that returns all of the diagonals of our board from top-left to bottom-right
    and from top-right to bottom-left.
    """

    # create an empty list of diagonals
    diagonals = []

    # --go from top-left to bottom-right--
    for row in range(3):
        # col it goes from 6, 5, 4. We create a empty list diagonal
        diagonal = []
        for col in range(6 - row):
            diagonal.append(board[row + col][col])

        # add the current diagonal
        diagonals.append(diagonal)

    for col in range(1, 4):
        # row goes from 6, 5, 4
        diagonal = []
        for row in range(6 - col + 1):
            diagonal.append(board[row][col + row])

        # add the current diagonal
        diagonals.append(diagonal)

    # # --go from top-right to bottom-left--
    # # for this we just "reverse" the above loops
    # for row in range(3, 6):
    #     # col it goes from 0 to 3, 4, 5, 6. We create a empty list diagonal
    #     diagonal = []
    #     for col in range(row):
    #         diagonal.append(board[row - col][col])
    #
    #     # add the current diagonal
    #     diagonals.append(diagonal)
    #
    # diagonals.append([board[5][1], board[4][2], board[3][3], board[2][4], board[1][5]])

    # return the diagonals
    return diagonals


def move_piece(board, col, player):
    """Three parameters:
    1) board -> 2d array that stores all of the values for our connect 4 board
    2) col -> integer ranging from 0 -> 6 inclusive indicating which column the player wants to place their piece in
    3) player -> integer either 0 or 1 indicates the player 0 => player 'X' and 1 => player 'O'

    move_piece(board, col, player) -> returns an updated board with the new piece in its location or it returns
    None if there is a "full column error"
    """

    # move down the column that the player has chosen and when there is no available space (meaning there is a
    # piece in that position) place a piece on unit above (unless no more space in the column)
    for row in range(6):
        # check that the current piece isn't blank
        if board[row][col] in ['X', 'O']:
            # there is a piece in this location now we must check that it isn't in the top row because if so
            # then there isn't anymore space in the column
            if row - 1 < 0:
                # no space in column therefore we throw an error "full column error" and return none
                print('There is no more space in this column')
                return None
            else:
                # we set the piece one higher to the player's piece and break out of our loop
                board[row - 1][col] = ['X', 'O'][player]
                break
        # if the piece was blank we check if it is the bottom piece in our grid. If it is we must place it no
        # matter what
        elif row == 5:
            # last row and from the above check we know that this is a blank space
            board[row][col] = ['X', 'O'][player]

    # return the updated board
    return board


def find_winner(board):
    """
    There are three possible ways a person can win
    1) he or she wins horizontally
    2) he or she wins vertically
    3) he or she wins diagonally

    The function find_winner returns 'X', 'O', 'draw', or None : (either X or O won, its a draw between
    the two of them, or the game is still going)
    """

    # checking if someone won horizontally (by rows)
    for row in board:
        # there are a total of 4 winning combos in a row. If the row is [0, 1, 2, 3, 4, 5, 6]
        # [0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], and [3, 4, 5, 6]
        for col in range(4):
            # we check that the combination is equal to itself and that it isn't a blank space or '.'
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] != '.':
                # someone won the current game. Since they are equal we can just return the id of the player that won
                return dict({'X': 0, 'O': 1})[row[col]]

    # checking if someone won vertically (by columns)
    for col in range(7):
        # same situation as the rows except vertical columns therefore we reverse the loops. There are
        # 3 winning combinations for the column if the column is [0, 1, 2, 3, 4, 5] then the winning combos
        # are : [0, 1, 2, 3], [1, 2, 3, 4], and [2, 3, 4, 5]
        for row in range(3):
            # check if the combination is equal to itself and not to a blank space in our case '.'
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != '.':
                # someone won the current game therefore we return the id f the player that won
                return dict({'X': 0, 'O': 1})[board[row][col]]

    # checking if someone won diagonally (we have to check from top-left to bottom-right
    # and bottom-left to top-right). The best way to do this is to write a helper function that returns
    # all the values of the diagonals of our connect4 board
    for diagonal in get_diagonals(b):
        # looping through all the diagonals of our board len(diagonal) - 3 (so we can grab sections of length 4)
        for element in range(len(diagonal) - 3):
            # going through each starting element
            if diagonal[element] == diagonal[element + 1] == diagonal[element + 2] == diagonal[element + 3] != '.':
                # we return the player that won
                return dict({'X': 0, 'O': 1})[diagonal[element]]

    # checking if the game was a draw because if we got this far into the function nobody has won
    draw = True

    # search every row in the board
    for row in board:
        for space in row:
            # we found an empty space therefore there is still a game in progress
            if space == '.':
                # we set draw to false because there is still possible moves that can be made
                draw = False

    # draw is True then we return 'draw' else we are just gonna return none
    if draw:
        return 'draw'

    # if we got this far into the function that means that nobody won and there was no draw. Therefore
    # we just return None because the game is still in progress
    return None


# create a blank 2d array that is a blank connect 4 grid
b = [['.' for i in range(7)] for j in range(6)]

# receive player names that aren't empty
player0 = input('Player X, enter your name: ')

# check that the name isn't blank (that includes enters, blank spaces, and tabs)
while player0.strip() == '':
    # ask for a name again
    player0 = input('Player X, enter your name again: ')

# do the same for player one
player1 = input('Player O, enter your name: ')

while player1.strip() == '':
    # ask for a name again
    player1 = input('Player O, enter your name again: ')

# players is a dictionary that holds the information about our players (makes the code easier to read later on)
players = {
    # key: id (0 or 1) -> value: dictionary that holds the player name and player piece through the keys
    # 'name': player name,
    # 'piece': player piece (either X or O)
    0: {'name': player0, 'piece': 'X'},
    1: {'name': player1, 'piece': 'O'},
}

# create
current_player = 0
do_we_print_board = True

# main game loop
while True:
    # at the start of each turn print the current board unless we are told not to
    if do_we_print_board:
        # We print the board meaning that there was no "full column error" and it is the next person's turn
        print()
        print_board(b)
        print()
    else:
        # There was a "full column error" therefore we just reset the do_we_print_board
        do_we_print_board = True

    # ask the current player which column he or she would like to place his or her piece in
    player_column = int(
        input("{}, you're {}. What column do you want to play in? ".format(players[current_player]['name'],
                                                                           players[current_player]['piece'])))

    # check that the player has entered a valid column if not ask again
    while player_column < 0 or player_column > 6:
        print('INVALID COLUMN')
        player_column = int(
            input("{}, you're {}. What column do you want to play in? ".format(players[current_player]['name'],
                                                                               players[current_player]['piece'])))

    # we have a valid column therefore we move add a piece
    result = move_piece(b, player_column, current_player)

    # check if player has placed in a full column
    if result:
        # there is a result (no errors) so we update our board, check if someone won, and/or switch moves
        b = result

        who_won = find_winner(b)

        # we check that if it is the value None or not (if None we continue) since our find_winner
        # function return 0, 1, draw, or None we need to use the function isinstance() because
        # 0 classifies as None so we need isinstance
        if isinstance(who_won, int) or isinstance(who_won, str):
            print()
            print_board(b)
            print()

            # we display who won or if it is a draw
            if isinstance(who_won, int):
                # someone won
                print(f'Congratulations, {players[who_won]["name"]}, you won!')
            else:
                # it was a draw
                print('It is a draw!')

            # break out of the main game loop
            break

        current_player = (current_player + 1) % 2
    else:
        # there was an error (full column error) therefore
        do_we_print_board = False
