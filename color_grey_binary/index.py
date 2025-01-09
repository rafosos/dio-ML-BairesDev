import keras.utils as image
import numpy as np
import matplotlib.pyplot as plt

img = image.load_img("./Lenna.png").convert("RGB")
img = np.asarray(img)

# img[0][0] = [321, 654 ,654] array de 3 num - RGB

print()
greyscale = [ (pixel.max() + pixel.min()) / 2
             for col in img
             for pixel in col 
            ]

plt.figure(figsize=(10,20))
plt.imshow(greyscale)
# print(len(img[0]))