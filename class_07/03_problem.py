from tkinter import *


class ButtonFrame(Frame):
    def __init__(self, master):
        '''ButtonFrame() creates a button that when clicked updates a counter'''
        Frame.__init__(self, master, )  # we set up the TK frame
        self.counter = 0
        self.grid()  # place the frame in the root window
        self.bfButton = Button(self, text='Click ME!', command=self.update_count)
        self.bfButton.grid(row=0, column=0)
        # create a text Displaying our counter
        self.bfMessageBox = Label(self, text='Number of times clicked: ' + str(0))
        self.bfMessageBox.grid(row=1, column=0)


    def update_count(self):
        '''updates the counter and prints it'''
        self.counter += 1
        self.bfMessageBox['text'] = 'Number of times clicked: ' + str(self.counter)


master = Tk()
master.title('The BUTTON!')
bf = ButtonFrame(master)
bf.mainloop()
