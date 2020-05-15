# we need three classes SudokuCell, SudokuBoard, and 3x3 square
from tkinter import *
from tkinter import filedialog


class SudokuCell(Label):
    def __init__(self, master, loc):
        """SudokuCell(master, loc) -> SudokuCell
        creates a blank new SudokuCell
        """
        Label.__init__(self, master, height=1, width=2, text='', bg='white', font=('Arial', 24))

        # initiating variables
        self.loc = loc  # (row,column) coordinate tuple
        self.number = 0  # 0 represents an empty cell
        self.read_only = False  # starts as changeable
        self.highlighted = False

        self.bind('<Button-1>', self.highlight)
        self.bind('<Key>', self.change)

    def get_loc(self):
        """SudokuCell.get_coord() -> tuple
        returns the (row,column) coordinate of the cell"""
        return self.loc

    def get_number(self):
        """SudokuCell.get_number() -> int
        returns the number in the cell (0 if empty)"""
        return self.number

    def is_read_only(self):
        """SudokuCell.is_read_only() -> boolean
        returns True if the cell is read-only, False if not"""

        return self.read_only

    def is_highlighted(self):
        """SudokuCell.is_highlighted() -> boolean
        returns True if the cell is highlighted, False if not"""
        return self.highlighted

    def set_number(self, number, read_only=False):
        """SudokuCell.set_number(number,[readonly])
        sets the number in the cell and unhighlights
        readOnly=True sets the cell to be read-only"""
        self.number = number
        self.read_only = read_only
        self.un_highlight()
        self.master.update_cells()

    def update_display(self, bad_cell=False):
        """SudokuCell.update_display()
        displays the number in the cell
        displays as:
          empty if its value is 0
          black if user-entered and legal
          gray if read-only and legal
          red when badCell is True"""
        if self.number == 0:  # cell is empty
            self['text'] = ''
        else:  # cell has a number
            self['text'] = str(self.number)
            if self.read_only:
                self['fg'] = 'dim gray'
            elif bad_cell:
                self['fg'] = 'red'
            else:
                self['fg'] = 'black'

    def highlight(self, event):
        """SudokuCell.highlight(event)
        handler function for mouse click
        highlights the cell if it can be edited (non-read-only)"""
        if not self.read_only:  # only act on non-read-only cells
            self.master.un_highlight_all()  # unhighlight any other cells
            self.focus_set()  # set the focus so we can capture key presses
            self.highlighted = True
            self['bg'] = 'lightgrey'

    def un_highlight(self):
        """SudokuCell.un_highlight()
        un highlights the cell (changes background to white)"""
        self.highlighted = False
        self['bg'] = 'white'

    def change(self, event):
        """SudokuCell.change(event)
        handler function for key press
        only works on editable (non-read-only) and highlighted cells
        if a number key was pressed: sets cell to that number
        if a backspace/delete key was pressed: deletes the number"""
        if not self.read_only and self.highlighted:
            if '1' <= event.char <= '9':  # number press -- set the cell
                self.set_number(int(event.char))

        elif event.keysym in ['BackSpace','Delete']:
            # delete the cell's contents by setting it to 0
            self.set_number(0)


class SudokuUnit:
    """represents a Sudoku unit (row, column, or box)"""

    def __init__(self, cells):
        """SudokuUnit(cells) -> SudokuUnit
        creates a new SudokuUnit with the SudokuCells in dict cells"""
        self.cells = cells  # store dict of SudokuCells

    def get_coord_list(self):
        """SudokuUnit.get_coord_list() -> list
        returns list of (row, column) tuples for cells"""
        return list(self.cells.keys())

    def get_cell_list(self):
        """SudokuUnit.get_cell_list() -> list
        returns list of SudokuCells"""
        return list(self.cells.values())

    def contains_coord(self, loc):
        """SudokuUnit.contains_coord(coord) -> bool
        returns True if (row, column) tuple is in unit, otherwise False"""
        return loc in self.cells  # looks for coord in keys


class SudokuGrid(Frame):
    """object for a Sudoku grid"""
    def __init__(self, master):
        Frame.__init__(self, master, bg='black')
        self.grid()
        # put in lines between the cells
        # (odd numbered rows and columns in the grid)
        for n in range(1, 17, 2):
            self.rowconfigure(n, minsize=1)
            self.columnconfigure(n, minsize=1)
        # thicker lines between 3x3 boxes and at the bottom
        self.columnconfigure(5, minsize=3)
        self.columnconfigure(11, minsize=3)
        self.rowconfigure(5, minsize=3)
        self.rowconfigure(11, minsize=3)
        self.rowconfigure(17, minsize=1)  # space at the bottom
        # create buttons
        self.buttonFrame = Frame(self, bg='white')  # new frame to hold buttons
        Button(self.buttonFrame, text='Load Grid', command=self.load_grid).grid(row=0, column=0)
        Button(self.buttonFrame, text='Save Grid', command=self.save_grid).grid(row=0, column=1)
        Button(self.buttonFrame, text='Solve', command=self.solve).grid(row=0, column=2)
        Button(self.buttonFrame, text='Reset', command=self.reset).grid(row=0, column=3)
        self.buttonFrame.grid(row=18, column=0, columnspan=17)

        self.cells = {}

        for row in range(9):
            for col in range(9):
                coord = (row, col)
                self.cells[coord] = SudokuCell(self, coord)
                # cells go in even-numbered rows/columns of the grid
                self.cells[coord].grid(row=2 * row, column=2 * col)

        self.units = []

        for m in range(9):
            row_cells = {}  # dict of cells in row m
            column_cells = {}  # dict of cells in column m
            for n in range(9):  # loop through each row/column
                row_cells[(m, n)] = self.cells[(m, n)]
                column_cells[(n, m)] = self.cells[(n, m)]
            self.units.append(SudokuUnit(row_cells))  # add row unit
            self.units.append(SudokuUnit(column_cells))

        for row in [0, 3, 6]:
            for column in [0, 3, 6]:
                box_cells = {}
                for i in range(3):
                    for j in range(3):
                        box_cells[(row + i, column + j)] = self.cells[(row + i, column + j)]
                self.units.append(SudokuUnit(box_cells))  # add box unit
        # main loop for the game

    def update_cells(self):
        for coord in self.cells:
            cell = self.cells[coord]
            number = cell.get_number()
            found_bad = False
            if number == 0:
                cell.update_display(False)
                continue
            for unit in self.find_units(coord):
                # loop through each cell in the unit
                for other_coord in unit.get_coord_list():
                    if other_coord == coord:  # skip this cell
                        continue
                    if self.cells[other_coord].get_number() == number:
                        found_bad = True

            cell.update_display(found_bad)

    def un_highlight_all(self):
        for cell in self.cells:
            self.cells[cell].un_highlight()

    def find_units(self, coord):
        return [unit for unit in self.units if unit.contains_coord(coord)]

    def load_grid(self):
        '''SudokuGrid.load_grid()
        loads a Sudoku grid from a file'''
        # get filename using tkinter's open file pop-up
        filename = filedialog.askopenfilename(defaultextension='.txt')
        # make sure they chose a file and didn't click "cancel"
        if filename:
            # open the file and read rows into a list
            sudokufile = open(filename,'r')
            rowList = sudokufile.readlines()
            sudokufile.close()
            # process file data
            for row in range(9):
                for column in range(9):
                    # get column'th character from line row
                    value = int(rowList[row][column])
                    # set the cell
                    # if value is nonzero, cell is read-only
                    self.cells[(row,column)].set_number(value, value != 0)

    def save_grid(self):
        '''SudokuGrid.save_grid()
        saves the Sudoku grid to a file'''
        # get filename using tkinter's save file pop-up
        filename = filedialog.asksaveasfilename(defaultextension='.txt')
        # make sure they chose a file and didn't click "cancel"
        if filename:
            sudokufile = open(filename, 'w') # open file for writing
            for row in range(9):
                for column in range(9):
                    # add cell to file
                    sudokufile.write(str(self.cells[(row,column)].get_number()))
                sudokufile.write('\n')  # new row
            sudokufile.close()

    def reset(self):
        '''SudokuGrid.reset()
        clears all non-read-only cells'''
        for cell in self.cells.values():
            # only clear non-read-only cells
            if not cell.is_read_only():
                cell.set_number(0)

    def valid(self, loc, num):
        for i in range(9):
            if self.cells[(loc[0], i)].number == num and loc[1] != i:
                return False

            # Check column
        for i in range(9):
            if self.cells[(i, loc[1])].number == num and loc[0] != i:
                return False

            # Check box
        box_x = loc[1] // 3
        box_y = loc[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.cells[(i, j)].number == num and (i, j) != loc:
                    return False

        return True

    def solve(self):
        find = None
        for row in range(9):
            for col in range(9):
                if self.cells[(row, col)].number == 0:
                    find = (row, col)

        if not find:
            return True

        for digit in range(1, 10):
            if self.valid(find, digit):
                self.cells[find].number = digit

                if self.solve():
                    self.update_cells()
                    return True

                self.cells[find].number = 0

        return False


def sudoku():
    """sudoku()
    plays sudoku"""
    root = Tk()
    root.title('Sudoku')
    SudokuGrid(root)
    root.mainloop()


sudoku()
