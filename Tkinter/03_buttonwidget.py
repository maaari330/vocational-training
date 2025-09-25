import tkinter as tk

root = tk.Tk()
root.title("Button")
root.geometry("200x150")
default_bg = root.cget("bg")

s = tk.StringVar()
lab = tk.Label(root, textvariable=s, fg="red")
lab.pack()
s.set("NON")


# コールバック関数（イベントハンドラ）
def on(event):
    s.set("ON")
    root.configure(bg="#222")
    lab.config(bg="#222")
    txt = event.widget.cget("text")
    print(event.widget, event, txt)
    s.set(txt)


# コールバック関数（イベントハンドラ）
def off(event):  # eventは発生したイベントそのもの
    s.set("OFF")
    root.configure(bg=default_bg)
    lab.config(bg=default_bg)
    txt = event.widget.cget(
        "text"
    )  # event.widget:その出来事が起きた ウィジェット実体（Button/Label/Entry などのインスタンス）
    print(event.widget, txt)
    s.set(txt)


btn_on = tk.Button(root, text="ON", cursor="heart")
btn_on.bind(
    "<Button-1>", on
)  # マウスの左クリックをした瞬間（Buttonはマウスのボタンのこと）に on を呼ぶ」規則を登録
# on関数にevent引数を渡す（※）
btn_on.pack()

btn_off = tk.Button(root, text="OFF", cursor="mouse")
btn_off.bind("<Button-1>", off)
btn_off.pack()

root.mainloop()

# （※）
# event 引数（tkinter.Event）をコールバックへ渡します。中には
# event.widget（発生元ウィジェット）
# event.x, event.y（ウィジェット内座標）
# event.num（マウスボタン番号 1/2/3）
# event.type, event.keysym など
# が入っています。
