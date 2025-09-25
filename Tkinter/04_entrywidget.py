import tkinter as tk

root = tk.Tk()
root.title("Entry")
root.geometry("200x150")

# Entryの作成、文字の追加
editbox = tk.Entry(width=20)
first = "名前の入力"
editbox.insert(tk.END, first)

s = tk.StringVar()
label = tk.Label(root, textvariable=s)
label.pack(pady=6)


# enter keyを押したらラベルを更新
def out(event):
    s.set(event.widget.get())


editbox.bind("<Return>", out)


# editboxにカーソルを置いたら（=focus）初期値を削除
def on_focus_in(e):
    if editbox.get() == "名前の入力":
        editbox.delete(0, tk.END)


editbox.bind("<FocusIn>", on_focus_in)


# マウスの左クリックをしたら　editbox：初期値表示、label表示
def on_focus_out(e):
    txt = editbox.get()
    s.set(txt)
    editbox.delete(0, tk.END)
    editbox.insert(0, first)


editbox.bind("<FocusOut>", on_focus_out)
editbox.pack()

btn = tk.Button(root, text="OK")
btn.bind("<Button-1>", on_focus_out)
btn.pack(pady=6)

root.mainloop()
