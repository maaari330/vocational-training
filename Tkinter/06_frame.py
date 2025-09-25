import tkinter as tk

root = tk.Tk()
root.title("Frame")
root.geometry("200x150")

# frame
f0 = tk.Frame(root)
f1 = tk.Frame(root)


# f0にラベルとボタンの配置/ウィジェット生成時にframeに配置
tk.Label(f0, text="ボタンを押してください").pack()
tk.Button(f0, text="Button#1").pack(side="left")
tk.Button(f0, text="Button#2").pack(side="left")
tk.Button(f0, text="Button#3").pack(side="left")

# f1にボタンの配置/ジオメトリマネージャでframeに配置
tk.Button(text="Button#4").pack(in_=f1, fill="both")
tk.Button(text="Button#5").pack(in_=f1, fill="both")
tk.Button(text="Button#6").pack(in_=f1, fill="both")

# フレームの配置
f0.pack()
f1.pack(fill="both")

root.mainloop()
