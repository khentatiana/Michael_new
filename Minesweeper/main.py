from tkinter import *
from tkinter import messagebox
import random
import threading


class Tile(Label):
    def __init__(self, master, top_num, loc):
        Label.__init__(self, master, height=1, width=2, text='', bd=3, relief=RAISED, bg='white', font=('Arial', 24))
        self.top_num = top_num
        self.master = master
        self.loc = loc
        self.exploded = False
        self.colors = ['blue','darkgreen','red','purple', 'maroon', 'cyan', 'black', 'dim gray']
        self.bind('<Button-1>', self.expose)
        self.bind('<Button-2>', self.flag)

    def is_bomb(self):
        return self.top_num == -1

    def location(self):
        return self.loc[0], self.loc[1]

    def return_location(self):
        return self.loc[0], self.loc[1]

    def expose(self, event=None):
        global array, process
        if self.top_num == 0:
            self['text'] = ''
            self['relief'] = SUNKEN
            self['bg'] = 'gray'
            x, y = self.location()
            if not process:
                auto_click(x, y, array)
        else:
            if self.top_num == -1:
                self['text'] = '*'
                self['bg'] = 'red'
                self.exploded = True
            else:
                self['relief'] = SUNKEN
                self['bg'] = 'gray'
                self['text'] = self.top_num
                self['fg'] = self.colors[self.top_num - 1]

    def is_exposed(self):
        return self['bg'] == 'dim gray'

    def is_flagged(self):
        return self['text'] == '*'

    def flag(self, event):
        # unflagging
        if self['text'] == '*':
            self['text'] = ''
        # unflagging
        elif self['text'] == '':
            self['text'] = '*'


class GameBoard(Frame):
    def __init__(self, master, x, y, num_bombs):
        global array
        Frame.__init__(self, master)
        self.grid()

        self.array = []
        for i in range(y):
            val = []
            for j in range(x):
                val.append(Tile(master, 0, (j, i)))
                val[j].grid(row=j, column=i)
            self.array.append(val)

        self.visited_points = []

        self.bomb_positions = []
        for i in range(num_bombs):
            rx = random.randrange(0, x)
            ry = random.randrange(0, y)

            if (rx, ry) not in self.bomb_positions:
                self.bomb_positions.append((rx, ry))
                # we set it up as a bomb
                self.array[ry][rx].top_num = -1
            else:
                i -= 1

        for i in range(y):
            for j in range(x):
                self.array[i][j].top_num = self.search_nearby(j, i, self.array)
        array = self.array

    def search_nearby(self, x, y, grid):
        if grid[y][x].top_num == -1:
            return -1
        else:
            val = 0
            for tx, ty in ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)):
                if in_grid(x + tx, y + ty, grid):
                    if grid[y + ty][x + tx].top_num == -1:
                        val += 1
            return val


global visited_points, array, process
process = False


def in_grid(x, y, grid):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def auto_click(x, y, grid):
    global process
    process = False
    q = [(x, y)]
    while q:
        for tx, ty in ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)):
            if in_grid(x + tx, y + ty, grid):
                if grid[y + ty][x + tx].is_exposed():
                    continue
                else:
                    # not exposed
                    if grid[y + ty][x + tx].top_num > 0:
                        grid[y + ty][x + tx].expose()

                    elif grid[y + ty][x + tx].top_num == 0:
                        grid[y + ty][x + tx].expose()
                        q.append((x + tx, y + ty))
    process = False


def play_minesweeper(x, y, num_bombs):
    root = Tk()
    GameBoard(root, x, y, num_bombs).mainloop()


play_minesweeper(30, 20, 100)
