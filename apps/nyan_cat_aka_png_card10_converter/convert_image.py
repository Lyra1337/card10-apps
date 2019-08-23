import numpy as np
from PIL import Image

IMAGE_FILE = "trim_nyan_cat.png"

# convert png to string object where each string is:
# "x,y,R,G,B"
img = Image.open(IMAGE_FILE).convert('RGB')
arr = np.array(img).tolist()

y = 1
pixels = []

for row in arr:
    x = 1
    for column in row:
        tmp_string = str(x) + ',' + str(y)
        for item in column:
            tmp_string += ',' + str(item)
        pixels.append(tmp_string)
        x += 1
    y += 1

print("NYAN = " + str(pixels))





