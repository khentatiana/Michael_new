import turtle


h, m = list(map(int, input().split()))

if h > 24 or m > 60:
    print("Sorry I can't draw you a clock =( ")
else:
    wn = turtle.Screen()
    wn.title('Clock')

    clock = turtle.Turtle()
    hour = turtle.Turtle()
    hour.left(90)
    hour.hideturtle()

    minute = turtle.Turtle()
    minute.left(90)
    minute.hideturtle()

    numbers = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    forwards = [5, 5, 5, 5, 8, 10, 12, 10, 8, 5, 5, 5, 5]

    # we draw the clock
    clock.left(90)
    clock.penup()
    for i in range(12):
        clock.forward(125)
        clock.stamp()
        clock.forward(forwards[i])
        clock.write(numbers[i], font=('Comic Sans MS', 15, 'bold'), align='right')
        print(i, forwards[i])
        clock.goto(0, 0)
        clock.right(30)
    clock.hideturtle()
    clock.speed(0)

    clock.goto(0, 0)
    hour.goto(0, 0)
    minute.goto(0, 0)

    for i in range(60):
        if i % 5 > 0:
            clock.forward(122)
            clock.pendown()
            clock.pensize(2)
            clock.forward(3)
            clock.penup()
            clock.goto(0, 0)
        clock.right(6)

    # we calculate the angle of the hour hand
    hour.right(30 * h + 6 * (m // 12) + 0.5 * (m % 12))
    minute.right(6 * m)

    hour.pensize(5)
    minute.pensize(5)

    # we draw the hour hand and minute hand
    hour.forward(50)
    minute.forward(75)

    wn.mainloop()
