import numpy as np
import random, math, time
from PIL import Image as image
def add_noise(image_path, mean=0, std=25):
    # Open the image using PIL
    img = image.open(image_path)
    imx = img.size[0]
    imy = img.size[1]
    if imx > 100 and imy > 100:
    # Resize the image to 100x100
        img = img.resize((500, 500))
        print("Resized Size - Width:", 100, "Height:", 100)
 
    # Convert the image to a NumPy array
    img_array = np.array(img)
    print("adding noise")
    # Generate random Gaussian noise with the same shape as the image
    noise = np.random.normal(mean, std, img_array.shape)

    # Add the noise to the image
    noisy_img_array = img_array + noise

    # Clip pixel values to [0, 255] range
    noisy_img_array = np.clip(noisy_img_array, 0, 255)
    

    return noisy_img_array