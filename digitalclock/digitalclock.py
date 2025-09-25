import datetime as dtm
import os
import tkinter as tk

root = tk.Tk()
root.title("Canvas")

# width, height
W = 1024
H = 464
cen_w = W // 2
cen_h = H // 2

# canvas
c1 = tk.Canvas(width=W, height=H)
c1.pack()

# map img
map = os.path.dirname(__file__) + "/worldmap.png"
image_data = tk.PhotoImage(file=map)

# locale
tokyo = (cen_w - 100, cen_h - 90, 0)
london = (cen_w - 500, cen_h - 150, -9)
newyork = (cen_w + 300, cen_h - 90, -13)


def show_clock(locale):
    # c1.delete('all')
    x, y, dif = locale
    dt = dtm.datetime.now()
    delta = dtm.timedelta(hours=dif)
    dt = dt + delta

    id1 = c1.create_text(
        x + 1, y, text="", font=("Helvetica", 12, "bold"), fill="white"
    )  # whitebase letter
    id2 = c1.create_text(x, y, text="", font=("Helvetica", 12, "bold"))
    tmstr = dt.strftime("%H:%M:%S")
    c1.itemconfig(id2, text=tmstr)
    c1.itemconfig(id1, text=tmstr)


def show_img():
    # canvas image
    c1.delete("all")
    c1.create_image(cen_w, cen_h, image=image_data)

    show_clock(tokyo)
    show_clock(london)
    show_clock(newyork)

    root.after(1000, show_img)


show_img()
root.mainloop()
