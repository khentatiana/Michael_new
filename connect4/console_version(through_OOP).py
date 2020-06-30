# a program that plays a game of connect 4 in the python console using OOP
class Board:
    """Represents the game board for our connect 4 game. Includes methods
    1) self.__init__(self) -> creates our game board
    2) self.drop_piece(self, col, player_id) -> adds a piece (the current players piece) into the
    column where it was requested to be dropped or returns a full column error
    3) self.print(self) -> displays the board in the console using prints and format returns : None
    4) self.get_rows(self) -> returns a list of all the rows in our board
    5) self.get_cols(self) -> returns a list of all the columns in our board
    6) self.get_diagonals(self) -> returns a list of all the diagonals
    7) self.get_winner(self) -> returns one of the following: 0, 1, 'draw', None. 0, 1 are the ids of the players
    0 -> 'X' and 1 -> 'O', 'draw' is returned when the game ends in a draw, and None is returned if
    the game is still in progress
    """
    def __init__(self):
        """In our init function we must initiate the board. RETURNS : None"""
        pass

    def print(self):
        """Displays the board in our python console"""
        pass

    def get_rows(self):
        """This function finds all of the rows. RETURNS : List of rows"""
        pass

    def get_cols(self):
        """This function finds all of the columns. RETURNS : List of columns"""
        pass

    def get_diagonals(self):
        """This function finds all of the diagonals. RETURNS : List of diagonals"""
        pass

    def drop_piece(self, col, player_id):
        """In this function we drop a piece into the selected column or we return a 'full column error'
        otherwise. RETURNS : 'success' -> if there were no problems, NONE -> if a full column error
        occurred"""
        pass

    def find_winner(self):
        """Finds the winner (if there is one) or checks for a draw. RETURNS : 0, 1 -> player ids,
        'draw' -> if the game ends in a draw, None -> if the game is still in progress"""
        pass


class Player:
    """represents a connect 4 player. Includes methods
    1) self.__init__(self, name, piece, game_board) -> stores the information given to us
    2) self.make_move(self) -> complete one game move for the player and displays board
    """
    def __init__(self, name, piece, game_board):
        """stores the given data"""
        self.name = name                         # a string that holds the player's name
        self.id = dict({'X': 0, 'O': 1})[piece]  # either 0 or 1
        self.game_board = game_board             # game board is a object BOARD

    def make_move(self):
        """completes on full game move for the player"""
        pass


def play(player1, player2):
    """Plays a game of connect 4. RETURNS : None"""

    # initiating and printing the board
    board = Board()
    board.print()

    # creating both players and the variable current_turn
    players = [Player(player1, 'X', board), Player(player2, 'O', board)]
    current_turn = 0

    # begin main game loop
    while True:
        # one iteration in the game loop
        pass
