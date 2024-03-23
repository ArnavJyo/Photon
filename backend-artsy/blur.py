import numpy as np
from PIL import Image as image
import random

def blur(img_path, intensity=1):
    # Open the image using PIL
    img = image.open(img_path)

    # Get image size
    imx = img.size[0]
    imy = img.size[1]
    if imx > 100 and imy > 100:
    # Resize the image to 100x100
        img = img.resize((500, 500))
        print("Resized Size - Width:", 500, "Height:", 500)
    width, height = img.size

    # Create a blank image to store the blurred result
    blurred_img = image.new('RGB', (width, height))

    # Define the size of the neighborhood
    neighborhood_size = intensity * 2 + 1

    # Iterate over each pixel of the original image
    for i in range(intensity, width - intensity):
        for j in range(intensity, height - intensity):
            # Get the RGB values of the current pixel and its neighbors
            pixel_sum = [0, 0, 0]
            for x in range(-intensity, intensity + 1):
                for y in range(-intensity, intensity + 1):
                    pixel = img.getpixel((i + x, j + y))
                    pixel_sum[0] += pixel[0]
                    pixel_sum[1] += pixel[1]
                    pixel_sum[2] += pixel[2]

            # Calculate the average RGB values and set them in the new image
            blurred_pixel = (
                pixel_sum[0] // (neighborhood_size ** 2),
                pixel_sum[1] // (neighborhood_size ** 2),
                pixel_sum[2] // (neighborhood_size ** 2)
            )
            blurred_img.putpixel((i, j), blurred_pixel)
    img_array = np.array(blurred_img)

    return img_array
    
    

     


