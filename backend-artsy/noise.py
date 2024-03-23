import numpy as np
import random, math, time
from PIL import Image as image
def add_noise(image_path, mean=0, std=25):
    # Open the image using PIL
    img = image.open(image_path)
    width, height = img.size

    # Create a blank image to store the blurred result
    imgOut = image.new('RGB', (width, height))
    # Convert the image to a NumPy array
    img_array = np.array(imgOut)
    print("adding noise")
    # Generate random Gaussian noise with the same shape as the image
    noise = np.random.normal(mean, std, img_array.shape)

    # Add the noise to the image
    noisy_img_array = img_array + noise

    # Clip pixel values to [0, 255] range
    noisy_img = np.clip(noisy_img_array, 0, 255)
    output_img = np.array(noisy_img)
    return output_img
