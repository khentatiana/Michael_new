from games.meters_100 import *
from games.meters_400 import *
from games.meters_1500 import *
from games.shot_put import *
from games.discus import *


class InitiateGameFrame(Frame):
    """
    Creates a Window where you have a list of games
    """
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.grid()
        self.name = name
        self.master = master

        Label(self, text='Which game would you like to play, ' + self.name + '?', font=('Arial', 18)).grid(columnspan=3,
                                                                                                           sticky=W)
        Button(self, text='>>Play decathlon 100!<<', command=self.initiate_game1, font=('Comic Sans MS', 18)).grid(
            columnspan=3, sticky=N)
        Button(self, text='>>Play decathlon 400!<<', command=self.initiate_game2, font=('Comic Sans MS', 18)).grid(
            columnspan=3, sticky=N)
        Button(self, text='>>Play decathlon 1500!<<', command=self.initiate_game3, font=('Comic Sans MS', 17)).grid(
            columnspan=3, sticky=N)
        Button(self, text='    >>Play shot put!<<    ', command=self.initiate_game4, font=('Comic Sans MS', 18)).grid(
            columnspan=3, sticky=N)
        Button(self, text='     >>Play Discus!<<     ', command=self.initiate_game5, font=('Comic Sans MS', 18)).grid(
            columnspan=3, sticky=N)

    def initiate_game1(self):
        """
        Plays Decathlon 100 Meters
        """
        self.destroy()
        Decathlon100Meters(self.master, self.name)

    def initiate_game2(self):
        """
        Plays Decathlon 400 Meters
        """
        self.destroy()
        Decathlon400Meters(self.master, self.name)

    def initiate_game3(self):
        """
        Plays Decathlon 1500 Meters
        """
        self.destroy()
        Decathlon1500Meters(self.master, self.name)

    def initiate_game4(self):
        """
        Plays Decathlon shot put
        """
        self.destroy()
        ShotPut(self.master, self.name)

    def initiate_game5(self):
        """
        Plays Decathlon discus
        """
        self.destroy()
        Discus(self.master, self.name)


player_name = input('Please enter you name: ')
root = Tk()
root.title('Main Menu')
game = InitiateGameFrame(root, player_name)
game.mainloop()
