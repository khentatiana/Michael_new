from games.dice.GUI_dice import GUIDie
from tkinter import *


class ShotPut(Frame):
    """Frame for the games shot put by Reiner Knizia"""
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.grid()
        self.name = name

        Label(self, text=self.name, font=('Arial', 18)).grid(columnspan=3, sticky=W)

        self.score_label = Label(self, text='Attempt #1 Score: 0', font=('Arial', 18))
        self.score_label.grid(row=0, column=3, columnspan=2)
        self.high_score_label = Label(self, text='High Score: 0', font=('Arial', 18))
        self.high_score_label.grid(row=0, column=5, columnspan=3, sticky=E)

        # initiating variables
        self.high_score = 0
        self.score = 0
        self.attempt = 0
        self.current_die = 0

        # creating our dice
        self.dice = []
        for n in range(8):
            self.dice.append(GUIDie(self, [1, 2, 3, 4, 5, 6], ['red'] + ['black'] * 5))
            self.dice[n].grid(row=1, column=n)

        # we create the roll and stop/foul buttons
        self.roll_button = Button(self, text='Roll', command=self.roll)
        self.roll_button.grid(row=2, columnspan=1)
        self.stop_button = Button(self, text='Stop', state=DISABLED, command=self.stop)
        self.stop_button.grid(row=3, columnspan=1)

    def reset_dice(self):
        # resets every single die back to its blank state and shifts the roll and stop buttons back to start
        for die in self.dice:
            die.clear()
        self.roll_button.grid()

    def stop(self):
        # refreshes the dice and updates the high score if needed
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label['text'] = 'High Score: ' + str(self.high_score)
        self.score = 0
        self.attempt += 1
        self.reset_dice()
        if self.attempt < 3:
            self.score_label['text'] = 'Attempt #' + str(self.attempt + 1) + ' Score: 0'
            self.roll_button.grid(row=2, columnspan=1)
            self.stop_button.grid(row=3, columnspan=1)
            self.roll_button['state'] = ACTIVE
            self.stop_button['state'] = DISABLED
            self.current_die = 0
        else:
            self.roll_button.grid_remove()
            self.stop_button.grid_remove()
            self.score_label['text'] = 'Game Over'

    def roll(self):
        # we roll the dice and then we check if the dice is a foul or not
        self.dice[self.current_die].roll()
        if self.current_die < 8:
            if self.dice[self.current_die].get_top() == 1:
                self.score_label['text'] = 'FOULED ATTEMPT'
                self.stop_button['text'] = 'FOUL'
                self.roll_button['state'] = DISABLED
                self.score = 0
                self.stop()
            else:
                if self.current_die == 7:



