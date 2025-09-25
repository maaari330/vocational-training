import tkinter as tk

root = tk.Tk()
root.title("packer")
root.geometry("200x150")
color = ("red", "blue", "green", "yellow")

# pack, grid, placeは共存できない

# pack,gridで座標表示
# for i, col in enumerate(color):
#     label = tk.Label(root, text=f"Label{i}", bg=col)
#     label.grid(column=i % 2, row=i // 2)
# label.pack(fill="both")
# label.pack(side="bottom")

# placeで細かく座標指定
color1 = ("red", "blue", "green")
for i, col in enumerate(color1):
    label = tk.Label(root, text=f"Label{i}", bg=col)
    label.place(relx=0.25 * i, rely=0.25 * i)  # 相対値での指定
    label.place(x=50 * i, y=40 * i)  # 絶対値での指定

# イベント待ち
root.mainloop()
