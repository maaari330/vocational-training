import os
import tkinter as tk

if os.environ.get("DISPLAY", "") == "":
    print("no display found. Using :0.0")
    os.environ.__setitem__("DISPLAY", ":0.0")


class App(tk.Frame):
    def __init__(self, master=None):
        self.n = 0
        super().__init__(master)
        self.pack()


root = tk.Tk()
app = App(master=root)
app.mainloop()
