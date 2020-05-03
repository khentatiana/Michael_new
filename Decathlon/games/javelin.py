from games.dice.GUI_die import *


class DecathlonJavelin(Frame):

    def __init__(self, master, player_name):
        Frame.__init__(self, master)
        self.grid()
        master.title('javelin')

        self.name = player_name

        Label(self, text=self.name, font=('Arial', 18)).grid(columnspan=3, sticky=W)

        # labels for score messages
        self.score_label = Label(self, text='Attempt #1 Score: 0', font=('Arial', 18))
        self.score_label.grid(row=0, column=2, columnspan=2)
        self.high_score_label = Label(self, text='High Score: 0', font=('Arial', 18))
        self.high_score_label.grid(row=0, column=5, columnspan=3, sticky=E)

        # initialize game data
        self.score = 0
        self.high_score = 0
        self.attempt = 0
        self.freezable_die_count = 0

        # creating dice
        self.dice = []
        for n in range(5):
            self.dice.append(GUIDie(self))
            self.dice[n].grid(row=1, column=n)

        # we create the roll and stop buttons
        self.roll_button = Button(self, text=' Roll ', command=self.roll)
        self.roll_button.grid(row=1, column=5, columnspan=3)
        self.stop_button = Button(self, text=' Stop ', state=DISABLED, command=self.stop)
        self.stop_button.grid(row=2, column=5, columnspan=3)
        self.bottom_text = Label(self, text='Click Roll button to start', font=('Arial', 18))
        self.bottom_text.grid(row=3, column=1, columnspan=3)

    def roll(self):
        pass

    def stop(self):
        pass

