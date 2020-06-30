from tkinter import *
import random


class Tile(Label):
    def __init__(self, master, loc, top_num, main):
        Label.__init__(self, master, relief=RAISED, height=1, width=2, text='', bd=3, bg='white', font=('Arial', 24))

        self.master = master
        self.game = main

        self.x = loc[0]
        self.y = loc[1]

        self.top_num = top_num
        self.exploded = False

        self.colors = ['blue', 'darkgreen', 'red', 'purple', 'maroon', 'cyan', 'black', 'dim gray']
        self.bind('<Button-1>', self.expose)
        self.bind('<Button-2>', self.flag)
        self.bind('<Button-3>', self.flag)

    def flag(self, event):
        pass

    def expose(self, event):
        pass

    def is_flagged(self):
        return self['text'] == '*' and self['bg'] == 'white'

    def is_exposed(self):
        return self['bg'] == 'red' and self['bg'] == 'light gray'


root = Tk()
game = Frame(root)
game.grid()
Tile(root, [0, 0], 0, None).grid()
game.mainloop()
