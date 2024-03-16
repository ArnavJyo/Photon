import imageio
import numpy as np
from tqdm import tqdm
from PIL import Image as image
def get_shape(image_path):
    img =image.open(image_path)
    shape = image.shape
    if len(shape)==3 or len(shape)==2:
        return shape
    else:
        raise Exception("Sorry, something is wrong!")

def is_grayscale(image):
    if len(get_shape(image))==3:
        return False
    elif len(get_shape(image))==2:
        return True
    else:
        raise Exception("Sorry, something is wrong!")

def get_luminance(image):
    return 0.299*image[:, :, 0] + 0.587*image[:, :, 1] + 0.114*image[:, :, 2]

def zeros(height, width, depth=None):
    return np.zeros((height, width)) if depth is None else np.zeros((height, width, depth))

def convert_grayscale(image):
    if not is_grayscale(image):
        height, width, _ = get_shape(image)
        gray_image       = zeros(height, width)
        gray_image = get_luminance(image)
        return gray_image
    else:
        return image