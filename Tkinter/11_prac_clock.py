import datetime as tm
import tkinter as tk

root = tk.Tk()
root.title("デジタル時計")
root.geometry("300x200")

buff = tk.StringVar()
buff.set("")
tk.Label(textvariable=buff, font=("FixedSys", 14, "bold")).pack()


def show_time():
    buff.set(tm.datetime.now().strftime("%Y/%m/%d %A %I:%M:%S %p"))
    root.after(1000, show_time)  # call func after 1000ms


show_time()
root.mainloop()
