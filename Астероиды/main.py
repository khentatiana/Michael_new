from tkinter import *
import random


class Ship:
    def __init__(self, master=None):
        self.master = master

        # to take care movement in x direction
        self.x = 1
        # to take care movement in y direction
        self.y = 0

        # canvas object to create shape
        self.canvas = Canvas(master)
        # creating rectangle
        self.rectangle = self.canvas.create_rectangle(5, 5, 25, 25, fill="black")
        self.canvas.pack()

        # calling class's movement method to
        # move the rectangle
        self.movement()

    def movement(self):
        # This is where the move() method is called
        # This moves the rectangle to x, y coordinates
        self.canvas.move(self.rectangle, self.x, self.y)

        self.canvas.after(100, self.movement)

        # for motion in negative x direction

    def left(self, event):
        print(event.keysym)
        self.x = -5
        self.y = 0

    # for motion in positive x direction
    def right(self, event):
        print(event.keysym)
        self.x = 5
        self.y = 0

    # for motion in positive y direction
    def up(self, event):
        print(event.keysym)
        self.x = 0
        self.y = -5

    # for motion in negative y direction
    def down(self, event):
        print(event.keysym)
        self.x = 0
        self.y = 5


class Asteroid:
    def __init__(self, master=None):
        self.master = master

        self.canvas = Canvas(master)
        self.asteroid = self.canvas.create_oval(0, 0, 5, 5, 'white')

        self.x = random.randrange(0, 100)
        self.y = 0

        self.movement()
        del self

    def __del__(self):
        self.canvas.delete()

    def movement(self):
        # This is where the move() method is called
        # This moves the rectangle to x, y coordinates
        self.canvas.move(self.asteroid, self.x, self.y)
        if self.y == -300:
            return
        self.canvas.after(100, self.movement)


if __name__ == "__main__":
    # object of class Tk, resposible for creating
    # a tkinter toplevel window
    root = Tk()
    root.title('Астероиды.')
    ship = Ship(root)

    # This will bind arrow keys to the tkinter
    # toplevel which will navigate the image or drawing
    root.bind("<KeyPress-Left>", lambda e: ship.left(e))
    root.bind("<KeyPress-Right>", lambda e: ship.right(e))
    root.bind("<KeyPress-Up>", lambda e: ship.up(e))
    root.bind("<KeyPress-Down>", lambda e: ship.down(e))

    for i in range(8):
        Asteroid(root)

    # Infinite loop breaks only by interrupt
    mainloop()
