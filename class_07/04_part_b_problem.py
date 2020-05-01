from tkinter import *


class C_F_Conversions(Frame):
    """Converts temperatures from Fahrenheit ot Celsius"""

    def __init__(self, master):
        """Setting up widgets for a f->c converter"""
        # Creating a frame and a grid For the Tk() frame
        Frame.__init__(self, master)
        self.grid()
        # we set up variables as double vars since they are doubles
        self.f = DoubleVar()
        self.c = DoubleVar()
        # setting up widgets and displays
        Label(self, text="Fahrenheit").grid(row=0, column=0)
        Label(self, text="Celsius").grid(row=0, column=1)
        Entry(self, textvariable=self.f).grid(row=1, column=0)
        Entry(self, textvariable=self.c).grid(row=1, column=1)
        Button(self, text=">>>>>", command=self.f_to_c).grid(row=2, column=0)
        Button(self, text="<<<<<", command=self.c_to_f).grid(row=2, column=1)

    def f_to_c(self):
        """update the output_value"""
        self.c.set(5/9 * (self.f.get() - 32))

    def c_to_f(self):
        """update the output_value"""
        self.f.set(9/5 * (self.c.get()) + 32)

root = Tk()
root.title('Temperature Conversion')
temps = C_F_Conversions(root)
temps.mainloop()
