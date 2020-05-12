from tkinter import *


class ChatWindowFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        master.geometry('400x800')



rt = Tk().title('Chat window')
ChatWindowFrame(rt).mainloop()
