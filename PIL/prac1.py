import os

from matplotlib import pyplot as plt

from PIL import Image, ImageDraw, ImageFilter

# PIL open and pyplot show
IMGPATH = os.path.dirname(__file__) + "/data/Lenna.jpg"
img = Image.open(IMGPATH)
fig, ax = plt.subplots(2, 5)
ax[0][0].imshow(img)  # img on axis
print(
    img.format,
    img.size,
    img.mode,
    img.getbands(),
    img.getextrema(),
    img.getpixel((255, 255)),
)  # band: getbands, extrema, pixcel


# convert, rotate, filter
gray_img = img.convert(mode="L")  # gray scale mode
ax[0][1].imshow(gray_img, cmap="gray")
pixel_img = img.convert(mode="I")  # pixel mode
ax[0][2].imshow(pixel_img, cmap="pink")
rotate_img = img.rotate(180)  # rotate
ax[0][3].imshow(rotate_img)
blur_img = img.filter(ImageFilter.GaussianBlur())  # blur filter
ax[0][4].imshow(blur_img)

# resize, crop
resize_img = img.resize(size=(120, 300))
ax[1][0].imshow(resize_img)
crop_img = img.crop(box=(0, 0, 200, 200))
ax[1][1].imshow(crop_img)

# show
plt.show()

# save
gray_img.save("GrayLenna.jpg", format="JPEG", quality=90)


# diagram( return None)
imgs = []
base = Image.new("RGB", (300, 300), color=(192, 192, 192))
b1 = base.copy()
d1 = ImageDraw.Draw(b1)
d1.ellipse((10, 10, 290, 290), fill=(0, 0, 255), outline=(0, 0, 0))
imgs.append(b1)

b2 = base.copy()
d2 = ImageDraw.Draw(b2)
d2.rectangle((10, 10, 290, 290), fill=(0, 0, 255), outline=(0, 0, 0))
imgs.append(b2)

b3 = base.copy()
d3 = ImageDraw.Draw(b3)
d3.line((10, 10, 290, 290), fill=(0, 0, 255))
imgs.append(b3)

b4 = base.copy()
d4 = ImageDraw.Draw(b4)
d4.polygon(
    [(150, 10), (290, 150), (150, 290), (10, 150)], fill=(0, 0, 255), outline=(0, 0, 0)
)
imgs.append(b4)

fig2, ax2 = plt.subplots(1, 4)
for ax, img in zip(ax2, imgs):
    ax.imshow(img)

plt.tight_layout()
plt.show()
