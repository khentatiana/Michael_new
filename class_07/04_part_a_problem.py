from tkinter import *


class EntryDemo(Frame):
    """demo of Entry widget"""
    def __init__(self, master):
        """EntryDemo(master) -> new EntryDemo frame"""
        Frame.__init__(self, master)
        self.grid()

        # set up control variables
        self.inputValue = IntVar()
        self.outputValue = IntVar()

        # set up widgets
        Label(self, text='Input').grid(row=0, column=0)
        Label(self, text='Input Value').grid(row=0, column=1)
        Label(self, text='Result').grid(row=0, column=3)
        Entry(self, width=5, textvariable=self.inputValue).grid(row=1, column=0)
        Label(self, textvariable=self.inputValue).grid(row=1, column=1)
        Button(self, text='>>>>>', command=self.set_output_value).grid(row=1, column=2)
        Label(self, textvariable=self.outputValue).grid(row=1, column=3)

    def set_output_value(self):
        """update the output value"""
        self.outputValue.set(5 * self.inputValue.get())


root = Tk()
root.title('Control Variable Demo')
demo = EntryDemo(root)
demo.mainloop()
