import rembg
import numpy as np
from PIL import Image

def removebg(img_path):
    input_image = Image.open(img_path)
    input_image = input_image.resize((800,300))
    input_array = np.array(input_image)
    
    output_array = rembg.remove(input_array,bgcolor=(255, 255, 255, 255))

    return output_array