import tkinter as tk

root = tk.Tk()
root.title("Entry")
root.geometry("200x150")

bmi = 22

# title label
title = tk.Label(root, text="標準体重計算")


def on_click(e):
    editbox.delete(0, tk.END)


# entry
editbox = tk.Entry(width=20)
editbox.insert(tk.END, "身長(cm)を入力してください")
editbox.bind(
    "<Button-1>", on_click
)  # マウスの左クリックをeditbox上で行ったら＝Button-1
editbox.pack()

# btn
btn = tk.Button(text="OK")

# label
s = tk.StringVar()
label = tk.Label(root, textvariable=s)
s.set("結果表示")
label.pack()


# event handler
def push_ok(event):
    weight = bmi * (float(editbox.get()) / 100) ** 2
    s.set(f"{weight:.2f}Kg")


# event
btn.bind("<Button-1>", push_ok)
btn.pack()

root.mainloop()
