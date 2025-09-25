import tkinter as tk

root = tk.Tk()
root.title("Python Tkinter")
root.geometry("200x150")
root.option_add("*font", "Meiryo")

# Button
btn = tk.Button(root, text="OK", cursor="heart")
btn.pack()
# Label
lb = tk.Label(
    root, text="Python Tkinter", font=("Helvetica", 14, "bold italic")
)  # ignore E501
lb.pack()
lb.configure(text="Tkinter Python")
print(lb.cget("font"))
# StringVar() : ウィジェット（部品）と値を結びつける“コントロール変数
lab_str = tk.StringVar()
lab_str.set("Hello")
lab = tk.Label(textvariable=lab_str, bg="yellow").pack()
lab2 = tk.Label(textvariable=lab_str, bg="green").pack()
print(lab_str.get())

# root.mainloop()
print("Tkinter end")
