import turtle
import random
import time


class TheCookie(turtle.Turtle):
    def __init__(self, x, y):
        # initialize a new turtle
        turtle.Turtle.__init__(self)
        # make it cookie-shaped
        self.shape('circle')
        self.turtlesize(13)
        self.color('#ad7623')
        # move into position
        self.speed(0)
        self.penup()
        self.goto(x, y)
        self.x = x
        self.y = y

        self.chocolate_list = [(44, 139), (53, 214), (68, 175), (83, 57), (86, 216), (91, 102), (31, 62), (100, 161),
                               (113, 46), (123, 20), (128, 124), (131, 203), (159, 141), (171, 50), (89, 129), (211, 175),
                               (213, 93)]

        for i in range(random.randrange(10, 17)):
            Chocolate(self.chocolate_list[i][0], self.chocolate_list[i][1])

    def was_it_clicked(self, x, y):
        return (abs(x - self.x))**2 + (abs(y - self.y))**2 <= 16000


class Chocolate(turtle.Turtle):
    """ No importance just an asthetic turtle"""
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape('circle')
        self.speed(0)
        self.width(20)
        self.penup()
        self.goto(x, y)
        print(x, y)


class CookieClicker:
    def __init__(self):
        # set up window
        self.window = turtle.Screen()
        self.window.title('Cookie Clicker!')
        # set up game data
        self.clicks = 0
        self.cash = 0
        self.click_amount = 1
        self.cookie = TheCookie(120, 120)

        # set up turtle to write game messages
        self.messenger = turtle.Turtle()
        self.messenger.hideturtle()
        self.messenger.penup()
        self.messenger.goto(-600, 150)

        self.buy_mouse = ItemBox(self, 'buy a mouse', -600, 0)

        self.print_clicks()
        # start the game
        self.window.onclick(self.update_cash)  # listen for clicks
        self.window.onclick(self.buy_mouse.buy_item, 2)
        self.window.onkey(self.quit_game, "q")

        self.window.listen()
        self.window.mainloop()

    def print_clicks(self):
        self.messenger.clear()
        self.messenger.write("You have solved " + str(self.clicks) + ' problems!\n'
                                                'And you have $' + str(self.cash),move=False, font=("Arial", 30, "bold"))

    def quit_game(self):
        self.window.bye()

    def update_cash(self, x, y):
        if self.cookie.was_it_clicked(x, y):
            self.clicks += 1
            self.cash += self.click_amount
            self.print_clicks()


class ItemBox(turtle.Turtle):
    def __init__(self, game, action, x, y):
        """
        :param action: an index from the list actions. [action1, action2, action3] etc...
        """
        turtle.Turtle.__init__(self)
        self.game = game
        self.speed(0)
        self.penup()
        self.goto(x, y)
        self.pendown()
        self.hideturtle()
        self.loc = (x, y)
        self.actions = {
            'upgrade mouse': [100, 1000, 10000, 'max'],
            'buy a mouse': [50],
            'buy a worker': [250],
            'buy a factory': [1000],
            'buy a company': [10000]
        }
        self.count_of_each_item = [0 for i in range(4)]

        self.price = self.actions[action][0]
        self.upgrade_mouse = 0
        self.action = action
        self.mouse_upgrades = [10, 50, 100]

        for i in range(2):
            self.forward(150)
            self.left(90)
            self.forward(50)
            self.left(90)
        self.messenger = turtle.Turtle()
        self.messenger.hideturtle()
        self.messenger.penup()
        self.messenger.goto(x, y + 25)
        self.messenger.clear()
        self.write_message()

    def if_clicked(self, x, y):
        return (self.loc[0] <= x <= self.loc[0] + 150) and (self.loc[1] <= y <= self.loc[1] + 50)

    def write_message(self):
        self.messenger.clear()
        if self.action == 'upgrade mouse':
            self.messenger.write("   >>Buy a mouse upgrade for $" + str(self.price) + "<<", move=False,
                                 font=("Arial", 12, "normal"))
        if self.action == 'buy a mouse':
            self.messenger.write("   >>Buy a mouse for $" + str(self.price) + "<<", move=False,
                                 font=("Arial", 12, "normal"))
        if self.action == 'buy a worker':
            self.messenger.write("   >>Buy a worker for $" + str(self.price) + "<<", move=False,
                                 font=("Arial", 12, "normal"))
        if self.action == 'buy a factory':
            self.messenger.write("   >>Buy a factory for $" + str(self.price) + "<<", move=False,
                                 font=("Arial", 12, "normal"))
        if self.action == 'buy a company':
            self.messenger.write("   >>Buy a company for $" + str(self.price) + "<<", move=False,
                                 font=("Arial", 12, "normal"))

    def adequate_funds(self, game):
        if game.cash - self.price >= 0:
            return True
        return False

    def buy_item(self, x, y):
        self.each_item = {
            'buy a mouse': 0,
            'buy a worker': 1,
            'buy a factory': 2,
            'buy a company': 3
        }
        self.production_values  ={
            # action: [amount produce, time]
            'buy a mouse': [1, 0.5],
            'buy a worker': [10, 1],
            'buy a factory': [100, 2],
            'buy a company': [1000, 1]
        }
        if not self.adequate_funds(self.game):
            self.messenger.clear()
            self.messenger.color('red')
            self.messenger.write(" >>NOT ENOUGH FUNDS!<<", move=False, font=("Arial", 12, "bold"))
            time.sleep(1)
            self.messenger.color('black')
            self.write_message()
        else:
            if self.action == 'upgrade mouse':
                if self.price == 'max':
                    pass
                else:
                    self.game.cash -= self.price
                    self.upgrade_mouse += 1
                    self.price = self.actions[self.action][self.upgrade_mouse]
                    self.game.click_amount = self.mouse_upgrades[self.upgrade_mouse - 1]
            else:
                self.game.cash -= self.price
                self.price += 50
                self.count_of_each_item[self.each_item[self.action]] += 1
                Item(self.game, self.production_values[self.action][0], self.production_values[self.action][1])


class Item:
    def __init__(self, game, amount_produced, time_per_click):
        time.sleep(time_per_click)
        game.cash += amount_produced
        game.clicks += amount_produced
        self.initiate(game, amount_produced, time_per_click)

    def initiate(self, game, amount_produced, time_per_click):
        time.sleep(time_per_click)
        game.cash += amount_produced
        game.clicks += amount_produced
        self.initiate(game, amount_produced, time_per_click)


gm = CookieClicker()
