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
        global array
        if self.top_num == 0:
            self['text'] = ''
            self['relief'] = SUNKEN
            self['bg'] = 'gray'
            x, y = self.location()

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
        Frame.__init__(self, master)
        self.grid()
        self.x = x
        self.y = y
        self.array = []
        for i in range(x):
            val = []
            for j in range(y):
                val.append(Tile(master, 0, [i, j]))
            self.array.append(val)

        # generating mines
        global positions
        positions = []
        for bomb in range(num_bombs):
            tx = random.randint(0, x)
            ty = random.randint(0, y)
            if (tx, ty) in positions:
                bomb -= 1
            else:
                # we mark it a a bomb
                self.array[ty][tx].top_num = -1
                positions.append((tx, ty))

        for ty in range(y):
            for tx in range(x):
                self.array[ty][tx].top_num = self.check_around(tx, ty)

        print_grid(self.array)

    def check_around(self, x, y):
        val = -1
        if self.array[y][x].top_num == -1:
            return -1
        for tx, ty in ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)):
            if 0 <= y + ty < self.y:
                if 0 <= x + tx < self.x:
                    if self.array[y + ty][x + tx].top_num == -1:
                        val += 1
        return val


def print_grid(array):
    for r in array:
        for c in r:
            c.expose()


rt = Tk()
board = GameBoard(rt, 20, 20, 50)
board.mainloop()

