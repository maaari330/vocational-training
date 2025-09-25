import tkinter as tk

root = tk.Tk()
root.title("Scale")
root.geometry("200x150")

# label
color_label = tk.Label(root, text="COLOR", bg="#000", fg="#fff")  # #000: black
color_label.pack(fill="both")


def change_col(n):
    color = f"#{s1.get():02x}{s2.get():02x}{s3.get():02x}"
    color_label.configure(bg=color)


# scale
s1 = tk.Scale(
    root,
    label="red",
    orient="horizontal",
    length=300,
    from_=0,
    to=255,
    command=change_col,
)  # command: scaleウィジェットの状態が変化するたびに呼び出される関数
s2 = tk.Scale(
    root,
    label="green",
    orient="horizontal",
    length=300,
    from_=0,
    to=255,
    command=change_col,
)

s3 = tk.Scale(
    root,
    label="blue",
    orient="horizontal",
    length=300,
    from_=0,
    to=255,
    command=change_col,
)

s1.pack(fill="both")
s2.pack(fill="both")
s3.pack(fill="both")
root.mainloop()
