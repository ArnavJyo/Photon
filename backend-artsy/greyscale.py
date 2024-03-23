import numpy as np
from PIL import Image as image
import random

def grayscale(image_path):
    # Open the image using PIL
    img = image.open(image_path)

    # Convert the image to RGB mode (if it's not already in that mode)
    img = img.convert('RGB')
    imx = img.size[0]
    imy = img.size[1]
    if imx > 100 and imy > 100:
    # Resize the image to 100x100
        img = img.resize((500, 500))
        print("Resized Size - Width:", 100, "Height:", 100)
    imx = img.size[0]
    imy = img.size[1]
    imgIn = image.new('RGB', img.size)
    imgIn.paste(img)

    # Create a new blank grayscale image
    gray_img = image.new('L', (imx,imy))

    # Iterate over each pixel of the original image
    for y in range(imy):
        for x in range(imx):
            # Get the RGB values of the current pixel
            r, g, b = img.getpixel((x, y))

            # Calculate luminance using the formula: Y = 0.299*R + 0.587*G + 0.114*B
            luminance = int(0.299 * r + 0.587 * g + 0.114 * b)

            # Set the grayscale pixel value in the new image
            gray_img.putpixel((x, y), luminance)
    img_array = np.array(gray_img)
    return img_array
