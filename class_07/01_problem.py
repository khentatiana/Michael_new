import turtle
import random

# you should add handlers

# set up window and turtles
turtle.setup(400, 500)
wn = turtle.Screen()
wn.title("Problem 1")
wn.bgcolor("lightblue")
tRed = turtle.Turtle()
tRed.color('red')
tBlue = turtle.Turtle()
tBlue.color('blue')
tGreen = turtle.Turtle()
tGreen.color('green')

# listeners
# you should add


def all_turtle_forward():
    tRed.forward(random.randrange(1, 51))
    tBlue.forward(random.randrange(1, 51))
    tGreen.forward(random.randrange(1, 51))


def all_turtle_right():
    tRed.right(15)
    tBlue.right(30)
    tGreen.right(40)


def all_turtle_left():
    tRed.left(15)
    tBlue.left(30)
    tGreen.left(40)


def quit():
    wn.bye()


wn.onkey(all_turtle_forward, "Up")
wn.onkey(all_turtle_right, "Right")
wn.onkey(all_turtle_left, "Left")
wn.onkey(quit, "q")

wn.listen()
wn.mainloop()
