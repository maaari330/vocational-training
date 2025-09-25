import tkinter as tk

root = tk.Tk()
root.title("Raidobutton機能")
root.geometry("300x200")


# 選択されたラジオボタン以外を無効にする
def state1():
    btn = v1.get()
    if btn == 1:
        radio12.configure(state="disabled")
    elif btn == 2:
        radio11.configure(state="disabled")
    elif btn == 0:
        pass
    else:
        print("Error", btn)


def state2():
    btn = v2.get()
    if btn == 1:
        radio22.configure(state="disabled")
    elif btn == 2:
        radio21.configure(state="disabled")
    elif btn == 0:
        pass
    else:
        print("Error", btn)


# 選択ボタンのリセット
def reset():
    radio11.configure(state="normal")
    radio12.configure(state="normal")
    radio21.configure(state="normal")
    radio22.configure(state="normal")
    v1.set(0)
    v2.set(0)


v1 = tk.IntVar()
v1.set(0)
v2 = tk.IntVar()
v2.set(0)

# Frame1
frame1 = tk.LabelFrame(root, text="Group1", bg="green")
frame1.pack()
# radio button(Frame1)
radio11 = tk.Radiobutton(
    frame1, text="選択項目#1", variable=v1, value=1, command=state1
)  # valueはradio button固有、variableに代入する値
radio11.pack()

radio12 = tk.Radiobutton(
    frame1, text="選択項目#2", variable=v1, value=2, command=state1
)
radio12.pack()

# frame2
frame2 = tk.LabelFrame(root, text="Group2", bg="blue")
frame2.pack()
# radio button(Frame2)
radio21 = tk.Radiobutton(
    frame2, text="選択項目#1", variable=v2, value=1, command=state2
)
radio21.pack()

radio22 = tk.Radiobutton(
    frame2, text="選択項目#2", variable=v2, value=2, command=state2
)
radio22.pack()


# button
restbtn = tk.Button(text="RESET", command=reset)
restbtn.pack()

root.mainloop()
