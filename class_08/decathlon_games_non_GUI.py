import random


class Die:
    def __init__(self,sides_param=6):
        # if an integer, create a die with sides
        #  from 1 to sides
        self.top = 0
        if isinstance(sides_param,int):
            sides_param = range(1,sides_param+1)
        self.sides = list(sides_param)
        self.numSides = len(self.sides)
        # roll the die to get a random side on top to start
        self.roll()

    def __str__(self):
        return str(self.numSides)+'-sided die with '+str(self.top)+' on top'

    def roll(self):
        # pick a random side and put it on top
        self.top = self.sides[random.randrange(self.numSides)]

    def get_top(self):
        return self.top


class Player:
    def __init__(self, player):
        self.name = player
        self.score = 0
        self.rerolls = 5

    def __str__(self):
        return "name: " + self.name + ", score: " + str(self.score) + ", rerolls left: " + str(self.rerolls)

    def take_turn(self):
        # roll the dice
        d1 = Die()
        d2 = Die()
        _ = input("Press enter to roll.")
        d1.roll()
        d2.roll()
        roundscore = d1.get_top() + d2.get_top()
        print("You rolled " + str(d1.get_top()) + " and " + \
              str(d2.get_top()) + " for a total of " + str(roundscore))
        boolean = False
        while True:
            if boolean:
                break
            # if the player has no rerolls, they're stuck with this
            if self.rerolls == 0:
                print("You're out of rerolls so you have to keep this.")
                break
            # see if they want to reroll
            response = 'x'
            while response.lower() not in ['y','n']:
                response = input("Do you want to reroll (y/n)? ")
                if response.lower() == 'n':
                    boolean = True
                    break  # keeping this roll, move on the the next roll
                # they're using a reroll
                self.rerolls -= 1
                print("OK, you have " + str(self.rerolls) + " rerolls left.")
                d1.roll()
                d2.roll()
                roundscore = d1.get_top() + d2.get_top()
                print("You rolled " + str(d1.get_top()) + " and " + \
                      str(d2.get_top()) + " for a total of " + str(roundscore))

        self.score += roundscore  # update the score


def print_scores(player_list):
    for player in player_list:
        print(player)


def decathlon_400_meters():
    num_players = int(input('Enter number of players: '))
    player_list = []
    for i in range(num_players):
        name = input('Player ' + str(i+1) + ', enter your name: ')
        player_list.append(Player(name))
    # play the game
    for turn in range(1, 5):
        print("Round " + str(turn))
        for i in range(num_players):
            print_scores(player_list)
            player_list[i].take_turn()
    print_scores(player_list)


def decathlon_100_meters():
    print('hi')
    pass


def game_arsenal():
    games = {
        1: 'decathlon 100 meters,',
        2: 'decathlon 400 meters.'
    }
    for i in range(1, len(games) + 1):
        print(str(i) + ': ' + games[i])

    choice = len(games) + 1
    while 1 <= choice <= len(games):
        choice = int(input('Which game would you like to play? '))

game_arsenal()

