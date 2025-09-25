import datetime
import os
import tkinter as tk

from PIL import Image, ImageDraw, ImageTk

W = H = 300
m = 8


class Clock(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.cv = tk.Canvas(self)
        self.cv.pack(expand=True, fill="both")
        self.create_widget()
        self.update()

    def create_widget(self):
        # 時計の文字盤描画
        canvas = Image.new(
            "RGBA", (W * m, H * m), (255, 255, 255, 0)
        )  # 背景はA=0で貼られない。(Aは透明度)

        # 文字盤分の描画
        for i in range(60):
            draw = ImageDraw.Draw(canvas)

            draw.line(
                (290 * m, H // 2 * m, W * m, H // 2 * m), fill="red", width=1 * m
            )  # "black"はA=255（不透明）なので貼られる。
            canvas = canvas.rotate(6)

        for i in range(1, 13):
            draw = ImageDraw.Draw(canvas)
            draw.line(
                (280 * m, H // 2 * m, W * m, H // 2 * m), fill="red", width=2 * m
            )  # "black"はA=255（不透明）なので貼られる。
            canvas = canvas.rotate(30)
        self.canvas = canvas

        # 時針の描画
        self.imhour = Image.new("RGBA", (W * m, H * m), (255, 255, 255, 0))
        drawhour = ImageDraw.Draw(self.imhour)
        drawhour.polygon(
            (W // 2 * m, H // 2 * m)
            + (175 * m, 140 * m)
            + (250 * m, H // 2 * m)
            + (175 * m, 160 * m),
            fill="red",
        )

        # 分針の描画
        self.imminute = Image.new("RGBA", (W * m, H * m), (255, 255, 255, 0))
        drawminute = ImageDraw.Draw(self.imminute)
        drawminute.polygon(
            (W // 2 * m, H // 2 * m)
            + (180 * m, 145 * m)
            + (270 * m, H // 2 * m)
            + (180 * m, 155 * m),
            fill="blue",
        )

        # 秒針の描画
        self.imsecond = Image.new("RGBA", (W * m, H * m), (255, 255, 255, 0))
        drawsecond = ImageDraw.Draw(self.imsecond)
        drawsecond.line(
            (W // 2 * m, H // 2 * m) + (270 * m, H // 2 * m), fill="red", width=2 * m
        )

        # 背景の描画
        fname = os.path.dirname(__file__) + "/cat_face.png"
        mickey_img = Image.open(fname).convert("RGB")
        self.mickey_img = mickey_img.resize(size=(W * m, H * m))
        bg = self.mickey_img.copy()
        bg.paste(canvas, (0, 0), canvas)

        self.base = bg

    def clock_move(self):
        tm = datetime.datetime.now()
        tmhour = tm.hour
        tmminute = tm.minute
        tmsecond = tm.second + tm.microsecond / 1000000

        # create_widgetで作成したものを複製
        canvas = self.base.copy()

        # 時針の描画
        imhour = self.imhour.rotate(-(tmhour * 30 + tmminute // 2 - 90))
        canvas.paste(imhour, (0, 0), imhour)

        # 分針の描画
        imminute = self.imminute.rotate(-(tmminute * 6 - 90))
        canvas.paste(imminute, (0, 0), imminute)

        # 秒針の描画
        imsecond = self.imsecond.rotate(-(tmsecond * 6 - 90))
        canvas.paste(imsecond, (0, 0), imsecond)

        return canvas

    def update(self):
        self.cv.delete("all")
        w = self.cv.winfo_width()
        h = self.cv.winfo_height()
        size = w if w < h else h
        clock_img = self.clock_move()
        clock_img = clock_img.resize((size, size), resample=Image.Resampling.LANCZOS)
        self.clock = ImageTk.PhotoImage(clock_img)
        self.cv.create_image(w // 2, h // 2, image=self.clock)
        self.after(20, self.update)


root = tk.Tk()
root.title("analog clock")
app = Clock(master=root)
app.mainloop()
