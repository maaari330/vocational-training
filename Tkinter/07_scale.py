import tkinter as tk

root = tk.Tk()
root.title("Scale")
root.geometry("300x200")

# IntVar
red = tk.IntVar()
red.set(0)
green = tk.IntVar()
green.set(0)
blue = tk.IntVar()
blue.set(0)

# label
color_label = tk.Label(root, text="COLOR", bg="#000", fg="#fff")  # #000: black
color_label.pack(fill="both")


def change_col(n):
    color = f"#{red.get():02x}{green.get():02x}{blue.get():02x}"
    color_label.configure(bg=color)


# scale
s1 = tk.Scale(
    root,
    label="red",
    orient="horizontal",
    length=300,
    from_=0,
    to=255,
    variable=red,
    command=change_col,
)  # command: scaleウィジェットの状態が変化するたびに呼び出される関数
s2 = tk.Scale(
    root,
    label="green",
    orient="horizontal",
    length=300,
    from_=0,
    to=255,
    variable=green,  # variable: 制御変数
    command=change_col,
)

s3 = tk.Scale(
    root,
    label="blue",
    orient="horizontal",
    length=300,
    from_=0,
    to=255,
    variable=blue,
    command=change_col,
)

s1.pack(fill="both")
s2.pack(fill="both")
s3.pack(fill="both")
root.mainloop()
