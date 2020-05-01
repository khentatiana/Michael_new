import turtle


class SuperAwesomeTurtle(turtle.Turtle):
    """a super awesome turtle!"""
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.turtle_speed = 0
        self.speed(50)
        self.getscreen().onkey(self.stop, 's')
        self.getscreen().onkey(self.increase_speed, 'Up')
        self.getscreen().onkey(self.decrease_speed, 'Down')
        self.getscreen().onkey(self.quit, 'q')
        self.getscreen().onkey(self.right, 'Right')
        self.getscreen().onkey(self.left, 'Left')
        self.go_forward()

    def go_forward(self):
        self.forward(self.turtle_speed)
        self.getscreen().ontimer(self.go_forward, 1000)

    def quit(self):
        wn.bye()

    def stop(self):
        self.turtle_speed = 0
        self.speed(self.turtle_speed)

    def increase_speed(self):
        self.turtle_speed += 25
        self.speed(self.turtle_speed)

    def decrease_speed(self):
        self.turtle_speed -= 25

    def right(self):
        turtle.Turtle.right(self, 90)

    def left(self):
        turtle.Turtle.left(self, 90)


wn = turtle.Screen()
pete = SuperAwesomeTurtle()
wn.listen()
wn.mainloop()
