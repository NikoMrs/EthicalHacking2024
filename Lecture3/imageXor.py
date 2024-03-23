from PIL import Image, ImageChops
im1 = Image.open('\images\peppers.png')
im2 = Image.open('\images\flag.png')

im3 = ImageChops.add(ImageChops.subtract(im2, im1), \
                     ImageChops.subtract(im1, im2))
im3.show()
#im3.save("Your_path/im3.png")