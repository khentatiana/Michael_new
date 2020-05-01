import random


class Die:
    '''Die class'''

    def __init__(self,sides=6):
        """Die(sides)
        creates a new Die object
        int sides is the number of sides
        (default is 6)
        -or- sides is a list/tuple of sides"""
        # if an integer, create a die with sides
        #  from 1 to sides
        if isinstance(sides, int):
            self.numSides = sides
            self.sides = list(range(1, sides + 1))
        else:  # use the list/tuple provided
            self.numSides = len(sides)
            self.sides = list(sides)
        # roll the die to get a random side on top to start
        self.roll()

    def __str__(self):
        '''str(Die) -> str
        string representation of Die'''
        return 'A '+str(self.numSides)+'-sided die with '+\
               str(self.get_top())+' on top'

    def roll(self):
        '''Die.roll()
        rolls the die'''
        # pick a random side and put it on top
        self.top = self.sides[random.randrange(self.numSides)]

    def get_top(self):
        '''Die.get_top() -> object
        returns top of Die'''
        return self.top

    def set_top(self,value):
        '''Die.set_top(value)
        sets the top of the Die to value
        Does nothing if value is illegal'''
        if value in self.sides:
            self.top = value


class DinoDie(Die):
    '''implements one die for Dino Hunt'''
    def __init__(self, color='#', numSides=6):
        self.color = color
        self.sides = []
        self.numSides = numSides
        if self.color == 'green':
            self.sides = ['dino' for i in range(3)]
            for i in range(2):
                self.sides.append('leaf')
            self.sides.append('foot')
        elif self.color == 'yellow':
            for i in range(2):
                self.sides.append('dino')
                self.sides.append('leaf')
                self.sides.append('foot')
        else:
            # red color die
            self.sides.append('dino')
            for i in range(2):
                self.sides.append('leaf')
            for i in range(3):
                self.sides.append('foot')
        self.roll()

    def __str__(self):
        answer = 'A ' + self.color + ' Dino die with a ' + str(self.get_top()) + ' on top.'
        return answer


class DinoPlayer:
    """implements a player of Dino Hunt"""
    def __init__(self, name):
        self.name = name
        self.pts = 0
        self.status = [0, 0]

    def __str__(self):
        return self.name + ' has ' + str(self.pts) + ' points.'

    def take_turn(self, dice):
        copy_dice = dice.copy()
        print(self.name + ", it's your turn!")
        while len(copy_dice) > 0:
            print('You have ' + str(len(copy_dice)) + ' dice remaining.')

            # we calculate the amount of each color dice
            calculate_dice_status(copy_dice)

            _ = input('Press enter to select dice and roll.')
            my_dice = []
            if len(copy_dice) < 3:
                my_dice = [die for die in copy_dice]
            else:
                for i in range(3): my_dice.append(copy_dice.pop(random.randrange(0, len(copy_dice))))
            for i in range(len(my_dice)):
                my_dice[i].roll()
                print('  ' + str(my_dice[i]))
            for die in my_dice:
                if die.get_top() == 'dino':
                    self.status[0] += 1
                    copy_dice.append(die)
                elif die.get_top() == 'foot':
                    self.status[1] += 1
                    if self.status[1] >= 3:
                        print('Too bad -- you got stomped!')
                        self.status = [0, 0]
                        return
                else:
                    copy_dice.append(die)

            print('This turn so far: ' + str(self.status[0]) + ' dinos and '
                  + str(self.status[1]) + ' feet.')

            answer = '#'
            while answer.lower() not in ['y', 'n', 'yes', 'no']:
                answer = input('Do you want to roll again? (y/n) ')

            if answer.lower() in ['n', 'no']:
                self.pts += self.status[0]
                self.status = [0, 0]
                return

        # if we have reached this point that means we have run out of dice and have no feet
        # therefore we just update the points value and go onto the next person's turn
        self.pts += self.status[0]
        self.status = [0, 0]


def calculate_dice_status(dice):
    # we calculate the amount of each color dice
    dice_status = [0, 0, 0]
    for die in dice:
        if die.color == 'green':
            dice_status[0] += 1
        elif die.color == 'yellow':
            dice_status[1] += 1
        else:
            # red color
            dice_status[2] += 1

    print(str(dice_status[0]) + ' green, ' + str(dice_status[1])
          + ' yellow, ' + str(dice_status[2]) + ' red')


def play_dino_hunt(num_players, num_rounds):
    """
    play_dino_hunt(numPlayer,numRounds)
    plays a game of Dino Hunt
    numPlayers is the number of players
    numRounds is the number of turns per player"""

    dice = [DinoDie('green') for i in range(6)]
    players = []

    for i in range(4):
        dice.append(DinoDie('yellow'))

    for j in range(3):
        dice.append(DinoDie('red'))

    for k in range(1, num_players + 1):
        name = input('Player ' + str(k) + ', enter your name: ')
        players.append(DinoPlayer(name))
    print()

    for round_num in range(1, num_rounds + 1):
        print('ROUND ' + str(round_num))
        print()
        print()

        print()
        for player in players:
            print(player)
        print()

        for player in players:
            player.take_turn(dice)
            print()
            for player in players:
                print(player)
            print()

    mx_player_idx = -1
    mx_pts = -1
    for player in players:
        if player.pts > mx_pts:
            mx_player_idx = players.index(player)
            mx_pts = player.pts
        elif player.pts == mx_pts:
            print('We have a tie!')
            mx_pts = -1
            break

    if mx_pts > 0:
        print('We have a winner!')
        print(players[mx_player_idx])


player_amt = int(input('Please enter the number of players playing: '))
round_amt = int(input('Please enter the amount of rounds you would like to play: '))
print()
play_dino_hunt(player_amt, round_amt)
