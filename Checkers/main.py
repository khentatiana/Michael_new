from tkinter import *


class Tile(Canvas):
    def __init__(self, master, color, x, y, game):
        """Makes a 60x60 tile with a background color of beige or brown"""
        Canvas.__init__(self, master, bg=color, width=60, height=60, highlightthickness=5)
        self.grid(row=x, column=y)
        self['highlightbackground'] = color

        # storing information about our tile
        self.x = x
        self.y = y
        self.color = color

        # binding keys
        self.bind('<Button-1>', game.get_click)

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

    def get_position(self):
        """returns the location of our tile"""
        return tuple([self.x, self.y])


class PaperBoard:
    """Stores locations of checker pieces and has a function that returns all possible legal moves for a checker of a
    color"""
    def __init__(self, grid=None):
        """Creates a 2d array that store all of the checkers in the form of:
         'W' -> white,
         'B' -> black,
         '_' -> blank
         """

        if grid:
            # we were given a set grid (for debugging purposes and testing)
            self.array = grid
        else:
            self.array = {}

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
                                self.array[(r, c)] = curr_range[1]
                            else:
                                # we set it as a blank space
                                self.array[(r, c)] = '_'
                        else:
                            # the row is even
                            if c % 2 == 1:
                                # we place a checker
                                self.array[(r, c)] = curr_range[1]
                            else:
                                # we set it as a blank space
                                self.array[(r, c)] = '_'

            # we fill the middle section with blank spaces
            for r in range(3, 5):
                # we loop through the current row
                for c in range(8):
                    self.array[(r, c)] = '_'

        self.c_t = 0

    def current_turn(self):
        """returns the color of the persons turn"""
        return ['W', 'B'][self.c_t]

    def switch_turn(self):
        """switches the current turn to black if white and visa versa"""
        self.c_t = (self.c_t + 1) % 2

    def create_flipped_grid(self):
        """creates a flipped copy of self.array"""
        # we create a new dict for our grid
        new_grid = {}

        # loop through all the rows backward
        for r in range(7, -1, -1):
            # loop through the current row normally
            for c in range(8):
                # add the checker to the location opposite of where it would be
                new_grid[(7 - r, c)] = self.array[(r, c)]

        # return the new_grid
        return new_grid

    def get_legal_moves(self, white=False):
        """returns legal moves for black pieces (by default) unless otherwise specified. We do this because when moving
        a black piece we add and moving a white piece we must subtract"""

        # when searching for the checkers we need the color and we need to flip the grid depending on the color
        if white:
            new_array = self.create_flipped_grid()
            search_color = 'W'
        else:
            new_array = self.array
            search_color = 'B'

        # we find the locations of all of the white and black pieces of the NEW array
        white_locations = []
        black_locations = []

        # create an empty list that store all legal move in the form of [start location, end location]
        legal_moves_for_color = []

        # loop through all of the rows
        for r in range(8):
            # loop through the current row
            for c in range(8):
                if self.array[(r, c)] == 'B':
                    # black checker
                    black_locations.append((r, c))
                elif self.array[(r, c)] == 'W':
                    # white checker
                    white_locations.append((r, c))
                else:
                    # we have a blank space therefore we just ignore it
                    pass

        if search_color == 'B':
            # we must find every legal move for the black pieces
            # the easiest way to do this would be to loop through every black piece location and add 1 if its a simple
            # move or add 2 if its a jump over a white piece
            for location in black_locations:
                # we search every location of a black checkers and add 1 for a simple move or add 2 for a jump

                # searching "simple moves"
                for tx, ty, direction in ((1, 1, 'R'), (1, -1, 'L')):
                    if self.legal_move(location, (location[0] + tx, location[1] + ty), new_array, search_color,
                                       direction, jump=False):
                        # the move is legal therefore we add it to our legal moves
                        legal_moves_for_color.append([location, (location[0] + tx, location[1] + ty)])

                # searching jumps
                for tx, ty, direction in ((2, 2, 'R'), (2, -2, 'L')):
                    if self.legal_move(location, (location[0] + tx, location[1] + ty), new_array, search_color,
                                       direction, jump=True):
                        # the move is legal therefore we add it to our legal moves
                        legal_moves_for_color.append([location, (location[0] + tx, location[1] + ty)])
        else:
            # we must find every legal move for the white pieces
            # this is pretty similar to finding black pieces just inverted locations since with white checkers we have
            # to move uphill so to speak
            for location in white_locations:
                # we search every single white location and add jumps and steps. Since we are searching through all of
                # the original positions from the original array we must reverse them during our search
                flipped_location = (7 - location[0], location[1])

                # searching "simple moves"
                for tx, ty, direction in ((1, 1, 'R'), (1, -1, 'L')):
                    if self.legal_move(flipped_location, (flipped_location[0] + tx, flipped_location[1] + ty),
                                       new_array, search_color, direction, jump=False):
                        # the move is legal therefore we add it to our legal moves
                        legal_moves_for_color.append([location, (location[0] - tx, location[1] + ty)])

                # searching jumps
                for tx, ty, direction in ((2, 2, 'R'), (2, -2, 'L')):
                    if self.legal_move(flipped_location, (flipped_location[0] + tx, flipped_location[1] + ty),
                                       new_array, search_color, direction, jump=True):
                        # the move is legal therefore we add it to our legal moves
                        legal_moves_for_color.append([location, (location[0] - tx, location[1] + ty)])

        return legal_moves_for_color

    @staticmethod
    def in_grid(location):
        """returns if a given location is within the boundaries of the grid or not"""
        return 0 <= location[0] < 8 and 0 <= location[1] < 8

    def legal_move(self, start, end, grid, color, direction, jump=True):
        """checks if a move is legal or not"""
        legal = False
        if self.in_grid(end):
            if grid[end] == '_':
                # the move is in the grid therefore we are safe to assume all actions are within the confines of our
                # grid
                if jump:
                    # the move is a jump therefore we need to check if its jumping over a checker of the opposite color
                    if color == 'B':
                        # we need to check if we are jumping over a white color
                        jump_color = 'W'
                    else:
                        # we need to check if we are jumping over a black color
                        jump_color = 'B'

                    # we need to know the direction so we can check if that we can check if there is a checker there
                    if direction == 'L':
                        # we check one unit lower and 1 unit left
                        loc = (start[0] + 1, start[1] - 1)
                    else:
                        # we check one unit lower and 1 unit right
                        loc = (start[0] + 1, start[1] + 1)

                    # now that we have our color we must check if we are jumping over it
                    if grid[loc] == jump_color:
                        # jump is legal
                        legal = True
                    else:
                        legal = False
                else:
                    # the move isn't a jump its a step. Since we already check that the end location is not a checker
                    # the move must be legal because we also check that the location is inside the grid
                    legal = True

        # to start we need to check if the move color even is the current turn
        if color != self.current_turn():
            # white is trying to move when black's turn or visa versa
            legal = False
        return legal

    def move_checker(self, start, finish, color):
        """moves the location of the checker in our array checking the legality of the move etc..."""
        if color == 'W':
            legal_moves = self.get_legal_moves(True)
        else:
            legal_moves = self.get_legal_moves()

        if [start, finish] in legal_moves:
            print('The move is legal!')
            # switch to the new location
            self.array[start], self.array[finish] = '_', self.array[start]
            return True
        else:
            print('The move is not legal')
            return False

    def remove(self, loc):
        """removes and eaten piece(doesn't check if there is a piece or not it is assumed that this move is legal)"""
        self.array[loc] = '_'


class GUIBoard(Frame):
    def __init__(self, master):
        """Creates a game board and positions checker pieces in their starting position"""
        # initiating a frame and snapping it to a grid
        Frame.__init__(self, master)
        self.grid()

        # we crete the backend of our program
        self.paper_board = PaperBoard()

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
        self.bottom_tile = Tile(master, 'light gray', 8, 2, self)
        self.bottom_tile.draw_checker('white')
        self.current = 0
        self.loc = (-1, -1)
        self.progress = False

        # label showing if you need to jump, continue jump, or not a legal move
        self.display_label = Label(master, text='', font=('Arial', 18, 'bold'))
        self.display_label.grid(row=8, column=5, columnspan=3)

    def get_click(self, event):
        """completes a move"""
        tile = event.widget
        location = tile.get_position()
        color = self.paper_board.array[location]
        print(location, color)

        # instead of tracking whether a move is in progress we can just check the number of tiles highlighted
        if len(self.complete_sweep()) > 0:
            # there is another highlighted tile therefore a move is already in progress meaning we must end
            # the current move

            self.display_label['text'] = ''

            colors = {
                'W': 'white',
                'B': 'black'
            }
            new_loc = self.complete_sweep()[0]

            # we get the color of the clicked checker in question and then check if the move is legal
            # if the move is legal the paper board will have moved the checker and will return True
            color1 = self.paper_board.array[new_loc]
            is_move_legal = self.paper_board.move_checker(new_loc, location, color1)

            if is_move_legal:
                # The move is legal therefore we redraw the checker in a new location
                self.array[location].draw_checker(colors[color1])
                self.array[new_loc].delete_checker()
                self.paper_board.switch_turn()
                self.bottom_tile.draw_checker(colors[self.paper_board.current_turn()])

                values = self.is_jump(new_loc, location, color1)
                if values[0]:
                    # it was a jump therefore we need to remove the checker we have jumped over
                    self.array[values[1]].delete_checker()
                    self.paper_board.remove(values[1])

            else:
                self.display_label['text'] = 'NOT A LEGAL MOVE'

            self.array[new_loc].highlight()
        else:
            # we simply highlight the clicked tile
            tile.highlight()

    @staticmethod
    def is_jump(start, end, color):
        """Returns whether if the move is a jump or not (assuming it is legal)"""
        if color == 'B':
            # move was black therefore we have to add 2 instead of subtract when moving
            if start[0] + 2 == end[0]:
                # we return true and it is a jump
                if start[1] + 2 == end[1]:
                    loc = (start[0] + 1, start[1] + 1)
                else:
                    loc = (start[0] + 1, start[1] - 1)
                return [True, loc]
            return [False, None]
        else:
            # move was white therefore we have to subtract 2 instead of adding when moving
            if start[0] - 2 == end[0]:
                # we return true and it is a jump and the location of the tile that was eaten
                if start[1] + 2 == end[1]:
                    loc = (start[0] - 1, start[1] + 1)
                else:
                    loc = (start[0] - 1, start[1] - 1)
                return [True, loc]
            return [False, None]

    def complete_sweep(self):
        """returns the locations of all highlighted checkers"""

        highlighted = []
        # loop through all rows
        for r in range(8):
            # loop through every unit in the row
            for c in range(8):
                if self.array[(r, c)].is_highlighted():
                    highlighted.append((r, c))

        return highlighted


root = Tk()
root.title('checkers')
GUIBoard(root)
root.mainloop()
