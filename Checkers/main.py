from tkinter import *
from numpy import sign


class Tile(Canvas):
    def __init__(self, master, color, x, y, game):
        """Makes a 60x60 tile with a background color of beige or green"""
        Canvas.__init__(self, master, bg=color, width=60, height=60, highlightthickness=5)
        self.grid(row=x, column=y)
        self['highlightbackground'] = color

        # storing information about our tile
        self.x = x
        self.y = y
        self.color = color

        # storing the GameBoard file
        self.game = game

        # binding a click to highlight a tile
        self.bind('<Button-1>', self.start_move)

    def draw_checker(self, color):
        """draws a circle with a color either red or white"""
        self.create_oval(9, 9, 60, 60, fill=color)

    def delete_checker(self):
        """Removes a checker from the tile"""
        for oval in list(self.find_all()):
            self.delete(oval)

    def highlight(self):
        """
        Outlines the border of the tile with a 5pixel thick border either black (if not highlighted)
        else it sets it back to the color of the tile.
        """
        if self.is_highlighted():
            # resets the border to the color giving the effect that you have unhighlighted the tile
            self['highlightbackground'] = self.color
        else:
            # sets the border to black meaning you have highlighted the tile
            self['highlightbackground'] = 'blue2'

    def is_highlighted(self):
        """Returns if the tile has a blue border or not"""
        return self['highlightbackground'] == 'blue2'

    def do_i_have_a_checker_on_my_back(self):
        """returns if there is a checker drawn on the tile or not"""
        return len(self.find_all()) == 1

    def start_move(self, event):
        """Completes a move for a checker"""
        # if the tile is already highlighted we can unhighlight it by clicking it again
        if self.is_highlighted():
            # un highlight it
            self.highlight()
        else:
            # we need to check that no other tiles are highlighted
            highlighted_tiles = self.game.complete_sweep()

            # looping through all of the tiles in the highlighted tiles
            for tile in highlighted_tiles:
                # either there is a highlighted tile or their isn't.
                self.game.array[tile].highlight()

            self.highlight()

        # now that we have highlighted we need to check if the tile that has been highlighted has a checker
        # or not. If it does then we start a turn else we move the checker to the piece if it is a legal move.
        # need to check if there is a move in progress
        if self.game.is_there_a_move_in_progress():
            # if true we need to make sure that we don't have a checker on the tile in question
            if not self.do_i_have_a_checker_on_my_back():
                # if its true then we check if the move is legal
                if self.game.is_legal([self.x, self.y]):
                    # legal move therefore we draw a checker
                    self.draw_checker(self.game.current_turn())
                    self.game.array[self.game.loc].delete_checker()
                    self.game.progress = False
                    self.game.loc = (-1, -1)
        else:
            # We need to check if the we clicked a checker
            if self.do_i_have_a_checker_on_my_back():
                # start move
                self.game.loc = (self.x, self.y)
                self.game.progress = True
            else:
                self.game.display_label['text'] = 'NOT A LEGAL MOVE!'


class GameBoard(Frame):
    def __init__(self, master):
        """Creates a game board and positions checker pieces in their starting position"""
        # initiating a frame and snapping it to a grid
        Frame.__init__(self, master)
        self.grid()

        # we create our checkerboard
        colors = ['blanched almond', 'saddle brown']
        current_color = 0

        # a dictionary that has the key as the location of the tile and
        self.array = {}

        for row in range(8):
            for col in range(8):
                # adding a tile with its color
                self.array[(row, col)] = Tile(master, colors[current_color], row, col, self)
                # switch the color index from 0 to 1 and visa versa
                current_color = (current_color + 1) % 2
            # After creating a row since 8 is an even number we must switch the starting index from 0 to 1 or visa versa
            # to achieve a checker pattern
            current_color = (current_color + 1) % 2

        # we position our checker pieces the top 3 rows a red and the bottom three rows are white

        # positioning the red checkers
        for row in range(3):
            # we loop through the row
            for col in range(8):
                # the checkers are positioned only on dark green tiles
                if self.array[(row, col)].color == 'saddle brown':
                    # we place a checker
                    self.array[(row, col)].draw_checker('gray10')

        # positioning the white checkers
        for row in range(5, 8):
            # we loop through the row
            for col in range(8):
                # the checkers are positioned only on dark green tiles
                if self.array[(row, col)].color == 'saddle brown':
                    # we place a checker
                    self.array[(row, col)].draw_checker('white')

        # we create the turn marker on the bottom
        turn_label = Label(master, text='  Turn:', font=('Arial', 18, 'bold'))
        turn_label.grid(row=8, column=1)

        # the tile that indicates the turn
        bottom_tile = Tile(master, 'light gray', 8, 2, self)
        bottom_tile.draw_checker('white')
        self.current = 0
        self.loc = (-1, -1)
        self.progress = False

        # label showing if you need to jump, continue jump, or not a legal move
        self.display_label = Label(master, text='Hello!', font=('Arial', 18, 'bold'))
        self.display_label.grid(row=8, column=5, columnspan=3)

    def complete_sweep(self):
        """checks how many checker pieces are highlighted"""
        # number of tiles
        number_of_tiles = []
        for row in range(8):
            for col in range(8):
                if self.array[(row, col)].is_highlighted():
                    number_of_tiles.append((row, col))

        return number_of_tiles

    def current_turn(self):
        """returns the person whose turn it is currently"""
        return ['white', 'gray10'][self.current]

    def is_there_a_move_in_progress(self):
        """returns if there is a turn in progress or not"""
        return self.progress

    def is_legal(self, loc2):
        """checks if the move is legal or not"""
        for tx, ty in ((-1, -1), (-1, 1)):
            # checking if you move forward (not jumping)
            if [self.loc[0] + tx, self.loc[1] + ty] == loc2:
                # we already check if there is a checker in this location therefore we don't have to check it here
                return True
            # if not we continue

        # say that the person was not moving forward but he wanted to jump
        for tx, ty in ((-2, -2), (-2, 2)):
            # we check if the jump is inside the grid boundaries
            if 0 <= self.loc[0] + tx < 8 and 0 <= self.loc[1] + ty < 8:
                # the jump is inside the grid
                if [self.loc[0] + tx, self.loc[1] + ty] == loc2:
                    # we need to check the value before it if there is a checker there or not
                    if self.array[(self.loc[0] + (tx + sign(tx) * (-1)), self.loc[1] + 1)].\
                            do_i_have_a_checker_on_my_back():
                        # there is a checker
                        return True

        # no returns therefore we return False meaning that his move isn't legal
        return False


def play_checkers():
    rt = Tk()
    rt.title('Checkers')
    GameBoard(rt)
    rt.mainloop()


play_checkers()
