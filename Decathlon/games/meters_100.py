from games.dice.GUI_die import *


class Decathlon100Meters(Frame):
    def __init__(self, master, player_name):
        Frame.__init__(self, master)
        self.grid()
        self.name = player_name
        master.title('100 meters')
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
        self.roll_button.grid(row=2, columnspan=4)
        self.keep_button = Button(self, text='Keep', state=DISABLED, command=self.keep)
        self.keep_button.grid(row=3, columnspan=4)

    def roll(self):
        # roll both dice
        for i in range(4):
            self.dice[4 * self.game_round + i].roll()
        score_temp = 0
        for i in range(4):
            score_temp += self.dice[4 * self.game_round + i].get_top()
        self.score_label['text'] = score_temp

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
        for i in range(4):
            self.score += self.dice[4 * self.game_round + i].get_top()
        self.score_label['text'] = 'Score: ' + str(self.score)
        self.game_round += 1

        if self.game_round < 2:  # move buttons to next pair of dice
            self.roll_button.grid(row=2, column=4 * self.game_round, columnspan=4)
            self.keep_button.grid(row=3, column=4 * self.game_round, columnspan=4)
            self.roll_button['state'] = ACTIVE
            self.keep_button['state'] = DISABLED
        else:
            self.keep_button.grid_remove()
            self.roll_button.grid_remove()
            self.reroll_label['text'] = 'Game Over'
