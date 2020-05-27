from tkinter import *


class ReversiSquare(Canvas):
    """displays a square in the Reversi game"""

    def __init__(self, master, r, c):
        """ReversiSquare(master,r,c)
        creates a new blank Reversi square at coordinate (r,c)"""
        # create and place the widget
        Canvas.__init__(self, master, width=50, height=50, bg='medium sea green')
        self.grid(row=r, column=c)
        # set the attributes
        self.position = (r, c)
        # bind button click to placing a piece
        self.bind('<Button>', master.get_click)

    def get_position(self):
        """ReversiSquare.get_position() -> (int,int)
        returns (row,column) of square"""
        return self.position

    def make_color(self, color):
        """ReversiSquare.make_color(color)
        changes color of piece on square to specified color"""
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)
        self.create_oval(10, 10, 44, 44, fill=color)
        print('🍉CHANGED TO MY WATERMELON🍉')


class ReversiBoard:
    """represents a board of Reversi"""

    def __init__(self):
        """ReversiBoard()
        creates a ReversiBoard in starting position"""
        self.board = {}  # dict to store position
        # create opening position
        for row in range(8):
            for column in range(8):
                coords = (row, column)
                if coords in [(3, 3), (4, 4)]:
                    self.board[coords] = 1  # player 1
                elif coords in [(3, 4), (4, 3)]:
                    self.board[coords] = 0  # player 0
                else:
                    self.board[coords] = None  # empty
        self.currentPlayer = 0  # player 0 starts

    def get_piece(self, coords):
        """ReversiBoard.get_piece(coords) -> int
        returns the piece at coords"""
        return self.board[coords]

    def get_player(self):
        """ReversiBoard.get_player() -> int
        returns the current player"""
        return self.currentPlayer

    def get_scores(self):
        '''ReversiBoard.get_scores() -> tuple
        returns a tuple containing player 0's and player 1's scores'''
        pieces = list( self.board.values() )  # list of all the pieces
        # count the number of pieces belonging to both players
        return pieces.count(0), pieces.count(1)

    def get_legal_moves(self):
        '''ReversiBoard.get_legal_moves() -> list
        returns a list of the current player's legal moves'''
        return []


class ReversiGame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.colors = ('black', 'white')

        self.board = ReversiBoard()
        self.squares = {}

        for row in range(8):
            for col in range(8):
                self.squares[(row, col)] = ReversiSquare(self, row, col)

        self.rowconfigure(8, minsize=3)

        self.turnSquares = []  # to store the turn indicator squares
        self.scoreLabels = []

        for i in range(2):
            self.turnSquares.append(ReversiSquare(self, 9, 7 * i))
            self.turnSquares[i].unbind("<Button>")
            self.turnSquares[i].make_color(self.colors[i])
            self.scoreLabels.append(Label(self, text='2', font=('Arial', 18)))
            self.scoreLabels[i].grid(row=9,column=1+5*i)

        self.passButton = Button(self, text='Pass', command=self.pass_move, state=DISABLED)
        self.passButton.grid(row=9, column=3, columnspan=2)
        self.update_display()

    def update_display(self):
        # update squares
        for row in range(8):
            for column in range(8):
                rc = (row, column)
                piece = self.board.get_piece(rc)
                if piece is not None:
                    self.squares[rc].make_color(self.colors[piece])

        newPlayer = self.board.get_player()
        oldPlayer = 1 - newPlayer
        self.turnSquares[newPlayer]['highlightbackground'] = 'blue'
        self.turnSquares[oldPlayer]['highlightbackground'] = 'white'

        scores = self.board.get_scores()
        for i in range(2):
            self.scoreLabels[i]['text'] = scores[i]

        # enable or disable the Pass button
        if len(self.board.get_legal_moves()) == 0:  # if no legal moves
            self.passButton.config(state=NORMAL)  # enable button
        else:  # if there are legal moves
            self.passButton.config(state=DISABLED)

    def pass_move(self):
        pass

    def get_click(self, event):
        pass


ReversiGame(Tk()).mainloop()
