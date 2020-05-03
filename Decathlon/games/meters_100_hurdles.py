from games.dice.GUI_die import *


class Decathlon100MeterHurdles(Frame):
    def __init__(self, master, player_name):
        Frame.__init__(self, master)
        self.grid()
        master.title('100 meter hurdles')
        self.name = player_name

        self.rethrows = 6
        self.score = 0

        self.score_label = Label(self, text='Score: 0', font=('Arial', 18))
        self.score_label.grid(row=0, column=2, columnspan=2)
        self.rethrow_label = Label(self, text='Rethrows: 5', font=('Arial', 18))
        self.rethrow_label.grid(row=0, column=5, columnspan=3, sticky=E)

        # initialize game data
        self.score = 0

        # creating dice
        self.dice = []
        for n in range(5):
            self.dice.append(GUIDie(self))
            self.dice[n].grid(row=1, column=n)

        # we create the roll and stop buttons
        self.roll_button = Button(self, text=' Roll ', command=self.roll)
        self.roll_button.grid(row=1, column=5, columnspan=1)
        self.stop_button = Button(self, text=' Stop ', state=DISABLED, command=self.stop)
        self.stop_button.grid(row=1, column=6, columnspan=1)

    def stop(self):
        self.roll_button.grid_remove()
        self.stop_button.grid_remove()
        self.rethrow_label['text'] = 'Game Over'

    def roll(self):
        if self.stop_button['state'] == DISABLED:
            self.stop_button['state'] = ACTIVE
        if self.rethrows > 0:
            self.score = 0
            for i in range(5):
                self.dice[i].roll()
                self.score += self.dice[i].get_top()

            self.score_label['text'] = 'Score: ' + str(self.score)
            self.rethrows -= 1
            self.rethrow_label['text'] = 'Rethrows: ' + str(self.rethrows)
        else:
            self.roll_button['state'] = DISABLED
