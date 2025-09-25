import os
import tkinter as tk

if os.environ.get("DISPLAY", "") == "":
    print("no display found. Using :0.0")
    os.environ.__setitem__("DISPLAY", ":0.0")


class App(tk.Frame):  # self=app()
    def __init__(self, master=None):
        self.n = 0
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="LABEL")
        self.Button = tk.Button(self, text="Button", command=self.btn_pushed)
        self.label.pack()
        self.Button.pack()

    def btn_pushed(self):
        self.n += 1
        #        self.label.configure(text="button_pushed %d" % self.n)
        self.label.configure(text=f"button_pushed {self.n}")


root = tk.Tk()
root.wm_title("Tkinter Class")
app = App(master=root)  # root上にApp(tk.Frame)を作成している
root.geometry(
    "200x100"
)  # geometory: トップレベルウィンドウ（tk.Tk または tk.Toplevel）にだけあるメソッド
app.mainloop()
