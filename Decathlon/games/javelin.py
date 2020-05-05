from games.dice.GUI_die import *


class DecathlonJavelin(Frame):
    """
    Javelin game frame from Decathlon dice games
    Javelin() -> GUI game of Javelin
    """
    def __init__(self, master, player_name):
        # initiating the Tk frame and snapping it to a grid
        Frame.__init__(self, master)
        self.grid()
        master.title('Javelin')

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
        self.last_attempt = 0

        # creating dice
        self.dice = []
        for n in range(6):
            self.dice.append(GUIFreezeDie(self, [1, 2, 3, 4, 5, 6], ['black', 'red'] * 3))
            self.dice[n].grid(row=1, column=n)

        # creating all 5 freeze buttons
        self.freeze_buttons = []
        for i in range(6):
            self.freeze_buttons.append(Button(self, text=' Freeze ', command=self.dice[i].toggle_freeze,
                                              state=DISABLED))
            self.freeze_buttons[i].grid(row=2, column=i)

        # we create the roll and stop buttons
        self.roll_button = Button(self, text=' Roll ', command=self.roll)
        self.roll_button.grid(row=1, column=7, columnspan=3)
        self.stop_button = Button(self, text=' Stop ', state=DISABLED, command=self.stop)
        self.stop_button.grid(row=2, column=7, columnspan=3)
        self.bottom_text = Label(self, text='Click Roll button to start', font=('Arial', 18))
        self.bottom_text.grid(row=3, column=1, columnspan=3)

    def roll(self):
        val = 0
        for i in range(6):
            if self.dice[i].is_frozen():
                val += 1

        if val == 6:
            self.roll_button['state'] = DISABLED
            return

        freeze = 0
        self.bottom_text['text'] = 'Click Stop button to keep'
        for i in range(6):
            if self.dice[i].get_top() % 2 == 1:
                if not self.dice[i].is_frozen():
                    freeze += 1
        if self.freezable_die_count == freeze and freeze != 0 and self.last_attempt == self.attempt:
            self.bottom_text['text'] = 'You must freeze a die to reroll'
            return
        else:
            self.last_attempt = self.attempt

        self.freezable_die_count = 0

        self.stop_button['state'] = ACTIVE
        for freeze_button in range(6):
            self.freeze_buttons[freeze_button]['state'] = DISABLED

        for die in self.dice:
            die.roll()

        for i in range(6):
            if not self.dice[i].is_frozen():
                if self.dice[i].get_top() % 2 == 1:
                    self.freeze_buttons[i]['state'] = ACTIVE
                    self.freezable_die_count += 1

        if self.freezable_die_count == 0:
            self.stop_button['text'] = ' FOUL '
            self.roll_button['state'] = DISABLED
            self.score_label['text'] = 'FOULED ATTEMPT'
            self.bottom_text['text'] = 'Click FOUL button to continue'
            self.score = 0
        else:
            for i in range(6):
                if self.dice[i].get_top() % 2 == 1:
                    if self.dice[i].is_frozen():
                        self.score += 0
                    else:
                        self.score += self.dice[i].get_top()
            self.score_label['text'] = 'Attempt #' + str(self.attempt + 1) + ' Score: ' + str(self.score)

    def stop(self):
        for die in self.dice:
            die.clear()

        if self.high_score < self.score:
            self.high_score = self.score

        for freeze_button in self.freeze_buttons:
            freeze_button['state'] = DISABLED

        self.score = 0
        self.attempt += 1

        if self.attempt < 3:
            self.roll_button['state'] = ACTIVE
            self.stop_button['state'] = DISABLED
            self.stop_button['text'] = ' Stop '
            self.bottom_text['text'] = 'Click Roll button to start'
            self.score_label['text'] = 'Attempt #' + str(self.attempt + 1) + ' Score: ' + str(self.score)
            self.high_score_label['text'] = 'High Score: ' + str(self.high_score)
        else:
            self.score_label['text'] = 'Game Over'
            self.roll_button.grid_remove()
            self.stop_button.grid_remove()
            self.bottom_text.grid_remove()
