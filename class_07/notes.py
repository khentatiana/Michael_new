class Square:
    def __init__(self, n, x):
        self.magic_square = [
            [n + 7 * x, n + 10 * x, n + 13 * x, n],
            [n + 12 * x, n + x, n + 6 * x, n + 11 * x],
            [n + 2 * x, n + 15 * x, n + 8 * x, n + 5 * x],
            [n + 9 * x, n + 4 * x, n + 3 * x, n + 14 * x]
        ]

    def magic_number(self):
        return sum(self.magic_square[0])

    def print_square(self):
        # we decrease by 1 because otherwise we would have a | b | c | d | which is not what we want
        for row in range(3):
            for col in range(3):
                print(str(self.magic_square[row][col]), end=' | ')
            print(str(self.magic_square[row][3]))
            print("_ _ _ _ _")

            for i in range(3):
                print(str(self.magic_square[3][i]), end=' | ')
            print(str(self.magic_square[3][3]))


n = float(input("Enter your starting value: "))
x = float(input("Enter your scale factor: "))
magic_sqr = Square(n, x)
magic_sqr.print_square()
print("The magic number is: " + str(magic_sqr.magic_number()))
