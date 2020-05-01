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


class Decathlon400Meters(Frame):
    def __init__(self, master, player_name):
        Frame.__init__(self, master)
        self.grid()
        self.name = player_name
        Label(self, text=self.name, font=('Arial', 18)).grid(columnspan=3, sticky=W)

        # labels for score messages
        self.score_label = Label(self, text='Score: 0', font=('Arial', 18))
        self.score_label.grid(row=0, column=3, columnspan=2)
        self.reroll_label = Label(self, text='Rerolls: 5', font=('Arial', 18))
        self.reroll_label.grid(row=0, column=5, columnspan=3, sticky=E)

        # initialize game data
        self.score = 0
        self.rerolls = 5
        self.game_round = 0

        # creating dice
        self.dice = []
        for n in range(8):
            self.dice.append(GUIDie(self, [1, 2, 3, 4, 5, -6], ['black'] * 5 + ['red']))
            self.dice[n].grid(row=1, column=n)

        # we create the roll button and the keep button
        self.roll_button = Button(self, text='Roll', command=self.roll)
        self.roll_button.grid(row=2, columnspan=2)
        self.keep_button = Button(self, text='Keep', state=DISABLED, command=self.keep)
        self.keep_button.grid(row=3, columnspan=2)

    def roll(self):
        # roll both dice
        self.dice[2 * self.game_round].roll()
        self.dice[2 * self.game_round + 1].roll()
        self.score_label['text'] = self.dice[2 * self.game_round].get_top() + self.dice[
            2 * self.game_round + 1].get_top()
        if self.keep_button['state'] == DISABLED:
            if self.rerolls == 0:
                self.roll_button['state'] = DISABLED
            self.keep_button['state'] = ACTIVE
        else:
            self.rerolls -= 1
            self.reroll_label['text'] = 'Rerolls: ' + str(self.rerolls)
            if self.rerolls == 0:
                self.roll_button['state'] = DISABLED

    def keep(self):
        self.score += self.dice[2 * self.game_round].get_top() + self.dice[2 * self.game_round + 1].get_top()
        self.score_label['text'] = 'Score: ' + str(self.score)
        self.game_round += 1

        if self.game_round < 4:  # move buttons to next pair of dice
            self.roll_button.grid(row=2, column=2 * self.game_round, columnspan=2)
            self.keep_button.grid(row=3, column=2 * self.game_round, columnspan=2)
            self.roll_button['state'] = ACTIVE
            self.keep_button['state'] = DISABLED
        else:
            self.keep_button.grid_remove()
            self.roll_button.grid_remove()
            self.reroll_label['text'] = 'Game Over'


name = input("Enter your name: ")
root = Tk()
root.title('400 Meters')
game = Decathlon400Meters(root, name)
game.mainloop()

