import tkinter as tk

WINDOWWIDTH = 400
WINDOWHEIGHT = 420


class Game(tk.Frame):
    def __init__(self, master, width=WINDOWWIDTH, height=WINDOWHEIGHT):
        super().__init__(master, width=width, height=height)
        self.pack()
        self.w = width
        self.h = height
        # ball properties
        self.x = 0
        self.y = 0
        self.vx = 7
        self.vy = 5
        self.diameter = 20
        self.MAX_ANGLE = 60
        # bar properties
        self.bar_upper_pos = self.h - 80
        self.bar_bottom_pos = self.h - 60
        self.bar_width = 60
        # interval time
        self.interval = 50
        # score
        self.score = 10
        self.create_widget()
        # ball move start
        self.after(self.interval, self.start)

    def create_widget(self):
        # canvas
        self.canvas = tk.Canvas(self, width=self.w, height=self.h, bg="white")
        self.canvas.place(x=0, y=0)
        # scale
        self.pos = tk.IntVar(self)
        self.scale = tk.Scale(
            self,
            orient=tk.HORIZONTAL,
            from_=0,
            to=self.w - self.bar_width,
            variable=self.pos,
        )
        self.scale.place(x=self.w, y=self.h, width=self.w, anchor=tk.SE)

    def start(self):
        self.canvas.delete("all")
        # update score
        self.update_score()

        # create bar
        self.bar = self.canvas.create_rectangle(
            self.pos.get(), self.h - 80, self.pos.get() + 60, self.h - 60, fill="blue"
        )
        # create score
        self.scorePanel = self.canvas.create_text(
            self.w // 2,
            self.h // 2,
            font=("Helvetica", 40, "bold"),
            text=str(self.score),
            fill="gray",
        )

        # create ball
        if (self.vx > 0 and self.x + self.diameter >= self.w) or (
            self.vx < 0 and self.x <= 0
        ):
            self.vx = -self.vx
        if (self.vy > 0 and self.y + self.diameter >= self.h) or (
            self.vy < 0 and self.y <= 0
        ):
            self.vy = -self.vy

        if (
            self.y + self.diameter == self.bar_upper_pos
            and self.pos.get() <= self.x <= self.pos.get() + self.bar_width
            and self.vy > 0
        ):
            bar_center = (self.pos.get() - self.bar_width) // 2
            ball_center = (self.x + self.diameter) // 2
            ratio = (ball_center - bar_center) // (
                self.bar_width // 2
            )  # Set the bounce angle according to the angle of collision
            self.vx = self.vx * ratio
            self.vy = -self.vy

        self.x += self.vx
        self.y += self.vy

        self.ball = self.canvas.create_oval(
            self.x, self.y, self.x + self.diameter, self.y + self.diameter, fill="red"
        )

        # recall
        self.after(self.interval, self.start)

    def update_score(self):
        if (
            self.y + self.diameter == self.bar_upper_pos
            and self.pos.get() <= self.x <= self.pos.get() + self.bar_width
            and self.vy > 0
        ):
            self.score += 1
        if self.y + self.diameter >= self.h and self.vy > 0:
            self.score -= 1


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tkinter Game")
    game1 = Game(master=root)
    game1.mainloop()
