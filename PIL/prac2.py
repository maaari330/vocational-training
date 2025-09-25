from pathlib import Path

from matplotlib import pyplot as plt

from PIL import Image, ImageDraw, ImageFilter, ImageOps

basepath = Path(__file__).resolve().parent
img1 = Image.open(basepath / "data" / "img1.jpg")
img2 = Image.open(basepath / "data" / "Lenna.jpg")

# paste img2 to img1
bg_img = img1.copy()
bg_img.paste(img2, (400, 400))
fig, ax = plt.subplots(2, 3)
ax[0][0].imshow(bg_img)


# mask image round
base = Image.new("1", img2.size, color=0)
b1 = base.copy()
d1 = ImageDraw.Draw(b1)
d1.ellipse((10, 10, 245, 245), fill=255)
# mask add
bg_img2 = img1.copy()
bg_img2.paste(img2, (400, 400), b1)
ax[0][1].imshow(bg_img2)

# mask image heart
b2 = Image.open(basepath / "data" / "heart.png")
print(b2.mode, b2.size)
b2 = b2.convert("L").resize(img2.size)
# mask add
bg_img3 = img1.copy()
bg_img3.paste(img2, (400, 400), b2)
ax[0][2].imshow(bg_img3)

# mask image invert heart
b3 = ImageOps.invert(b2)
# mask add
bg_img4 = img1.copy()
bg_img4.paste(img2, (400, 400), b3)
ax[1][0].imshow(bg_img4)

# mask image invert heart blur
b4 = ImageOps.invert(b2)
b4 = b4.filter(ImageFilter.GaussianBlur())
# mask add
bg_img5 = img1.copy()
bg_img5.paste(img2, (400, 400), b4)
ax[1][1].imshow(bg_img5)

plt.show()
