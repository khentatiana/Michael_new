import turtle


# set up window and TT
wn = turtle.Screen()
carol = turtle.Turtle()
carol.speed(0)


def teleport_and_draw(x, y):
    carol.goto(x, y)


def teleport_and_no_draw(x, y):
    carol.penup()
    carol.goto(x, y)
    carol.pendown()


def quit():
    wn.bye()


# listeners to teleport
wn.onclick(teleport_and_draw, 1)    # left click
wn.onclick(teleport_and_no_draw, 2) # right click
wn.onkey(quit, "q")

# turn on the listeners and run
wn.listen()
wn.mainloop()
