import tkinter as tk

root = tk.Tk()
root.title("Spinbox機能")
root.geometry("200x150")
root.option_add("*font", ("FixeSys", 14))


# spinbox
month = ("January", "February", "March", "April")
sp1 = tk.Spinbox(values=month, width=20, state="readonly")
sp2 = tk.Spinbox(from_=1, to=31, increment=1, width=20)
sp3 = tk.Spinbox(from_=1, to=5, increment=0.5, format="%05.2f", width=20)
for w in (sp1, sp2, sp3):
    w.pack(padx=5, pady=5, fill="both")
# spinbox 選択肢の設定方法：
# 1. 数値range -> from_, to　※ formatは数値rangeのみ有効 （tkinterでしか使えない表現）
# 2. 値リスト -> values=tuple() ※ values優先


def clicked():
    print(sp1.get())
    print(sp2.get())
    print(sp3.get())


# button
btn = tk.Button(text="OK", command=clicked)
btn.pack()

root.mainloop()
