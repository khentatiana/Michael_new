import turtle
import random


class MisbehavingTurtle(turtle.Turtle):
    """
    Inherits Turtle class and then we override the values left and right

    """
    def left(self, angle):
        misbehave = random.randrange(1, 5) # picks a number from one to four
        if misbehave == 1:
            return turtle.Turtle.right(self, angle)
        return turtle.Turtle.left(self, angle)

    def right(self, angle):
        misbehave = random.randrange(1, 5) # picks a number from one to four
        if misbehave == 1:
            return turtle.Turtle.left(self, angle)
        return turtle.Turtle.left(self, angle)


# test case
# drawing an octagon and a square
def drawing_test(t):
    '''drawing_test(t)
     draws an octagon and square with t'''
    for i in range(8):
        t.forward(30)
        t.left(45)
    t.right(45)
    for i in range(4):
        t.forward(50)
        t.right(90)


# one nice turtle and one not-so-nice turtle
wn = turtle.Screen()
sugar = turtle.Turtle()
sugar.color('green')
drawing_test(sugar)
spice = MisbehavingTurtle()
spice.color('red')
drawing_test(spice)
wn.mainloop()
