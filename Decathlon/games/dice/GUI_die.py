from tkinter import *
import random


class GUIDie(Canvas):
    def __init__(self, master, value_list=[1, 2, 3, 4, 5, 6], color_list=['black' for i in range(6)]):
        """GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)"""

        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self, master, width=60, height=60, bg='white', bd=5, relief=GROOVE)
        # store the value_list and color_list
        self.value_list = value_list
        self.color_list = color_list
        # initialize the top side
        self.top = 1

    def get_top(self):
        return self.value_list[self.top - 1]

    def clear(self):
        pip_list = self.find_all()
        for pip in pip_list:
            self.delete(pip)

    def roll(self):
        self.top = random.randrange(1, 7)
        self.clear()
        self.draw()

    def draw(self):
        pip_list = \
            [
                [(1, 1)],
                [(0, 0), (2, 2)],
                [(0, 0), (1, 1), (2, 2)],
                [(0, 0), (0, 2), (2, 0), (2, 2)],
                [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
                [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)]
            ]

        for location in pip_list[self.top - 1]:
            self.draw_pip(location, self.color_list[self.top - 1])

    def draw_pip(self, location, color):
        (center_x, center_y) = (15 + 20 * location[0], 15 + 20 * location[1])
        self.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill=color)


class GUIFreezeDie(GUIDie):
    def __init__(self, master, value_list=[i for i in range(1, 7)], color_list=['black'] * 6):
        """
        GUIFreezeDie(master, values_list, color_list)
        We inherit a GUIDie giving us the ability to initiate it with our new values
        """
        GUIDie.__init__(self, master, value_list, color_list)

    def is_frozen(self):
        return self['bg'] == 'gray'

    def toggle_freeze(self):
        self['bg'] = 'gray'

    def roll(self):
        if not self.is_frozen():
            GUIDie.roll(self)

    def clear(self):
        if self.is_frozen():
            self['bg'] = 'white'
        GUIDie.clear(self)


