import os
import tkinter as tk

root = tk.Tk()
root.title("Canvas")

# 「画面の座標系（GUIの座標系）は、原点が左上で y が下向きに増える」という歴史的な慣習がある。

# canvas circle
c1 = tk.Canvas(width=150, height=150)  # キャンパスいっぱいの大きさ
id = c1.create_oval(10, 10, 140, 140)  # 上記の上に円を描く（左上、右下の座標を指定）
# id: オブジェクトコンストラクタによって返される
c1.itemconfigure(id, fill="red", outline="yellow", width=10)
c1.pack()

# canvas rectangle
c2 = tk.Canvas(width=150, height=150)
id2 = c2.create_rectangle(10, 10, 140, 140, fill="yellow")
c2.pack()

# canvas line
c3 = tk.Canvas(width=150, height=150)
points: list[float] = [10, 140, 10, 10, 140, 140, 140, 10]

id3 = c3.create_line(points)
# (x0,y0),(x1,y1)...の全ての座標を通る線を作成
c3.itemconfigure(id3, width=2.0, fill="green")
c3.pack()

# canvas line smooth
c4 = tk.Canvas(width=150, height=150)
id4 = c4.create_line(points)
c4.itemconfigure(id4, smooth=True, splinesteps=24)
c4.pack()

# canvas image
c5 = tk.Canvas(width=300, height=300)
img_path = os.path.dirname(__file__) + "/cat_face.png"
img = tk.PhotoImage(file=img_path)
id5 = c5.create_image(0, 0, image=img, anchor=tk.NW)
c5.pack()

# canvas text
c6 = tk.Canvas(width=300, height=150)
id6 = c6.create_text(
    100,
    75,
    text="Hello Python",
    font=("Helvetica", 20, "bold", "italic"),
    justify=tk.CENTER,
)
c6.pack()

root.mainloop()
