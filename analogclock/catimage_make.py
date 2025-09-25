import tkinter as tk

from PIL import Image, ImageDraw

W = H = 300
# scale
s = 4

canvas = Image.new("RGBA", (W * s, H * s), "white")
d = ImageDraw.Draw(canvas)

# ear
left_ear = [(50 * s, 150 * s), (95 * s, 20 * s), (130 * s, 135 * s)]
right_ear = [(170 * s, 135 * s), (205 * s, 20 * s), (250 * s, 150 * s)]
d.polygon(left_ear, fill="black")
d.polygon(right_ear, fill="black")

# face
cx, cy = 150, 170
r = 110
circle_dot = [cx - r, cy - r, cx + r, cy + r]
d.ellipse([d * s for d in circle_dot], fill="black")

# bear
line_w = 6 * s  # 太さを上げて視認性UP
# 左2本（頬の少し外側へ）
d.line(
    [((cx - 55) * s, (cy - 5) * s), ((cx - 140) * s, (cy - 15) * s)],
    fill="black",
    width=line_w,
)
d.line(
    [((cx - 55) * s, (cy + 15) * s), ((cx - 140) * s, (cy + 5) * s)],
    fill="black",
    width=line_w,
)
# 右2本
d.line(
    [((cx + 55) * s, (cy - 5) * s), ((cx + 140) * s, (cy - 15) * s)],
    fill="black",
    width=line_w,
)
d.line(
    [((cx + 55) * s, (cy + 15) * s), ((cx + 140) * s, (cy + 5) * s)],
    fill="black",
    width=line_w,
)

final = canvas.resize((W, H))
final.save("cat_silhouette.png")
