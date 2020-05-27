from tkinter import *
from tkinter import messagebox
import random


class Tile(Label):
    def __init__(self, master, loc, top_num, main):
        """Tile() -> creates a tile object that is press able and is either a bomb or not"""
        # creating the tile object through a label widget
        Label.__init__(self, master, relief=RAISED, height=1, width=2, text='', bd=3, bg='white', font=('Arial', 24))

        # saving the master and the game
        self.master = master
        self.game = main

        # label x and y using the variable loc
        self.x = loc[0]
        self.y = loc[1]

        # top_num -> 0 blank, 1-8 number of bombs around it, -1 is a bomb
        self.top_num = top_num
        self.exploded = False

        # colors for each amount of bombs around the tile
        self.colors = ['blue', 'darkgreen', 'red', 'purple', 'maroon', 'cyan', 'black', 'dim gray']

        # we bind keys for clicking on the tile
        self.bind('<Button-1>', self.expose)
        self.bind('<Button-2>', self.flag)

    def is_exploded(self):
        """Returns if the tile has been exploded"""
        return self.exploded

    def is_exposed(self):
        """Returns if the tile is exposed or not"""
        return self['bg'] == 'light gray' or self['bg'] == 'red'

    def is_flagged(self):
        """Returns if the tile is flagged or not"""
        return self['text'] == '*' and self['bg'] == 'white'

    def flag(self, event):
        """Flags a tile with an asterisk symbol"""
        # we can flag/unflag the tile
        if self['text'] == '':
            # flag the tile
            if self.game.number_of_flags == 0:
                # we can't flag anything
                messagebox.showerror("Minesweeper!", "Can't place any more flags you ran out!", parent=self.master)
            else:
                # we can plant a flag
                self['text'] = '*'
                self.game.number_of_flags -= 1
                self.game.update_flag_value()
        elif self['text'] == '*':
            # unflag the tile
            self['text'] = ''
            self.game.number_of_flags += 1
            self.game.update_flag_value()

        # complete a sweep
        self.game.complete_sweep()

    def expose(self, event):
        """exposes the tile and if it's a blank tile we need to auto click"""
        # change its appearance
        if not self.is_exposed():
            self.reveal()

            # launch auto click if we revealed a blank tile
            if self.top_num == 0:
                self.game.auto_click(self.x, self.y)

            # check if it was a bomb or if the player has won
            self.game.complete_sweep()

    def reveal(self, special=False):
        """reveals the tile by changing its appearance"""
        if special:
            # the tile was flagged
            if self.top_num == -1:
                # it was marked properly therefore we show it correct flag
                self['text'] = '*'
                self['bg'] = 'light green'
                self['relief'] = SUNKEN
            else:
                # the tile was marked incorrectly therefore we must show it as a bad flag
                if self.top_num == 0:
                    self['text'] = ''
                else:
                    self['text'] = self.top_num

                self['bg'] = 'cyan'
                self['relief'] = SUNKEN
        else:
            # we just expose the tile normally
            if self.is_flagged():
                # the tile is flagged so we can't reveal it until it has been unflagged
                pass
            else:
                # the tile isn't flagged therefore we can expose it and we need to check if it is exposed or not
                if self.top_num == -1:
                    # this is a bomb therefore we have to explode it
                    self['text'] = '*'
                    self['bg'] = 'red'
                    self.exploded = True
                elif self.top_num == 0:
                    # this is a blank tile therefore we just make it blank
                    self['bg'] = 'light gray'
                    self['relief'] = SUNKEN
                else:
                    # it has bombs around it therefore we reveal the number
                    self['text'] = str(self.top_num)
                    self['fg'] = self.colors[self.top_num - 1]
                    self['bg'] = 'light gray'
                    self['relief'] = SUNKEN


class GameBoard(Frame):
    def __init__(self, master, rows, cols, num_bombs):
        """GameBoard() -> creates a game board full of tiles in the form of rows x cols"""
        # initiating the frame
        Frame.__init__(self, master)
        self.grid()

        # creating the game board with just blank tiles
        # its in the form of [[col], [col], [col], [col]] -> 4 rows, c cols
        self.array = []
        self.rows = rows
        self.cols = cols
        self.num_bombs = num_bombs
        for r in range(rows):
            # we create a row for each element
            row = []
            for c in range(cols):
                row.append(Tile(master, [r, c], 0, self))
                row[c].grid(row=r, column=c)
            # appending a row to self.array
            self.array.append(row)

        # we generate the bombs at random locations
        bombs = 0
        self.locations = []
        while bombs < num_bombs:
            # increase the bomb number
            bombs += 1

            # generate the position for the bomb
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)

            # check if the bomb is overlapping an existing bomb
            if (row, col) in self.locations:
                # we have to roll back one more time
                bombs -= 1
            else:
                # we add the bomb
                self.array[row][col].top_num = -1
                self.locations.append((row, col))

        # now we generate the numbers (pre-make the grid) by searching the locations nearby
        for r in range(rows):
            for c in range(cols):
                self.array[r][c].top_num = self.check_around(r, c)

        # set the number of flags that you have left at the bottom of the screen
        self.number_of_flags = num_bombs

        # make a number of flags label
        self.flags_label = Label(master, text='Number of flags left: ' + str(self.number_of_flags),
                                 font=('Arial', 18, 'bold'))
        self.flags_label.grid(row=2, column=self.cols)

        # make a reset game button
        self.reset_button = Button(master, text="Reset the game?", font=('Arial', 18, 'bold'), command=self.reset)
        self.reset_button.grid(row=0, column=self.cols)

        # make a quit game button
        self.reset_button = Button(master, text="Quit the game? ", font=('Arial', 18, 'bold'), command=self.quit)
        self.reset_button.grid(row=1, column=self.cols)

        # game description
        # creating the widgets required
        self.text_widget = Text(master, height=6, width=30, font=('Arial', 15, 'italic'))
        self.text_scroll = Scrollbar(master)

        # packing to the grid
        self.text_widget.grid(row=4, column=self.cols, sticky=W, rowspan=6)
        self.text_scroll.grid(row=4 // 2 + 2, column=self.cols, sticky=E, rowspan=6)

        # configuring the widgets
        self.text_widget.config(yscrollcommand=self.text_scroll.set)
        self.text_scroll.config(command=self.text_widget.yview)

        # the game description
        game_description = """Game Description:
Try to reveal every single non bomb tile
    &    
Try to correctly flag every single bomb 
on the field.


Say you lose...
The flags that you have placed correctly will light up as light green.

And the Flags improperly placed will 
become their corresponding number 
with a background of blue.


Say you win...
Congratulations you now have bragging 
rights!
=P"""

        # adding the game description
        self.text_widget.insert(END, game_description)
        self.text_widget.config(state=DISABLED)

    def update_flag_value(self):
        self.flags_label['text'] = 'Number of flags left: ' + str(self.number_of_flags)

    def in_grid(self, x, y):
        """returns if the point in question is inside of the array or not"""
        return 0 <= x < len(self.array) and 0 <= y < len(self.array[0])

    def check_around(self, row, col):
        """returns the number of bombs around the tile"""
        if self.array[row][col].top_num == -1:
            # this is a bomb therefore we need to ignore it by just returning its value
            return -1
        else:
            # the tile is not a bomb therefore we count the amount of bombs around the tile (row, col)
            # tuples with what we add in the form of (Up, UpRight, Right, DownRight, Down, DownLeft, Left, UpLeft)
            top_number = 0
            for tr, tc in ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)):
                if self.in_grid(row + tr, col + tc):
                    if self.array[row + tr][col + tc].top_num == -1:
                        # we have to increase the number of bombs around
                        top_number += 1

            return top_number

    def complete_sweep(self):
        """Checks if any bombs have been detonated or if all of the passive square
        (non bombs) have been exposed in which case the person won else if blown up he lost"""
        endgame = False

        # we check every single tile
        for row in range(self.rows):
            for col in range(self.cols):
                if self.array[row][col].is_exploded():
                    messagebox.showerror('Minesweeper', 'KABOOM! You lose.', parent=self)
                    endgame = True

        # if the game ended reveal all of the tiles else we check if the person has won
        if endgame:
            # we expose every tile and in the process we blow up the bombs
            wrong_flags = 0
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.array[row][col].is_flagged():
                        # the tile is flagged so we must check if it is a bomb or not
                        if self.array[row][col].top_num == -1:
                            # its a bomb therefore it was marked correctly and we must ignore it
                            self.array[row][col].reveal(True)
                            continue
                        else:
                            # not a bomb and since its flagged it has been flagged improperly this also means that we
                            # must reveal it as an improper flag
                            wrong_flags += 1
                            self.array[row][col].reveal(True)
                    else:
                        self.array[row][col].reveal()

            # displays the number of flags that were flagged wrong
            messagebox.showerror('Minesweeper', 'You have marked ' + str(wrong_flags) + ' wrong flags.', parent=self)
        else:
            # we check if the player has won
            player_won = True
            for row in range(self.rows):
                for col in range(self.cols):
                    # we check if the tile is exposed if not we continue checking
                    if self.array[row][col].is_exposed():
                        # not all tiles are exposed but if its flagged we must ignore it
                        # since the bombs can't be exposed
                        continue
                    else:
                        if self.array[row][col].is_flagged():
                            # its a flagged tile therefore we ignore it (we count it as an exposed tile)
                            continue
                        else:
                            # to win a player must expose all tiles that are not mines
                            player_won = False

            # we check if the player has won or not
            if player_won:
                messagebox.showinfo('Minesweeper', 'Congratulations -- you won!', parent=self)

                # Reveal all the flags as green (just because I feel like it)
                for bomb in self.locations:
                    self.array[bomb[0]][bomb[1]].reveal(True)

    def auto_click(self, x, y):
        # we can use a bfs search algorithm to reveal all adjacent units
        # add starting search point to a queue
        q = [(x, y)]

        while len(q) > 0:
            # get new cell from the queue
            r, c = q.pop(0)
            # expand search to 8 adjacent neighbors
            for tr, tc in ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)):

                # if new cell out of bounds -> do not process
                if self.in_grid(r + tr, c + tc):
                    # destination is either exposed, blank or a number
                    if self.array[r + tr][c + tc].is_exposed():
                        # already exposed
                        continue
                    if self.array[r + tr][c + tc].is_flagged():
                        # we count it as an exposed tile
                        continue
                    if self.array[r + tr][c + tc].top_num > 0:
                        # number classified as a wall
                        self.array[r + tr][c + tc].reveal()
                    else:
                        # if destination is available - expose it and add it to our queue
                        self.array[r + tr][c + tc].reveal()
                        q.append((r + tr, c + tc))

    def quit(self):
        """quits the game by deleting the frame"""
        self.master.destroy()

    def reset(self):
        """reset the game"""
        play_minesweeper(self.rows, self.cols, self.num_bombs)


def play_minesweeper(rows, cols, num_bombs):
    """Plays the game mine-sweeper, to win you must flag all mines and expose all tiles"""
    root = Tk()
    root['bg'] = 'black'
    root.title('Minesweeper: ' + str(rows) + ' * ' + str(cols) + ' with ' + str(num_bombs) + ' bombs.')
    game_board = GameBoard(root, cols, rows, num_bombs)
    game_board.mainloop()


rows, cols, num_bombs = list(map(int, input('Enter the number of rows, columns, and the number of bombs: ').split()))
play_minesweeper(rows, cols, num_bombs)
