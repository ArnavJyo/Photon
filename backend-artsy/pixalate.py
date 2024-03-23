import numpy as np

from PIL import Image as image

def pixelate(image_path, block_size):
    # Open the image using PIL
    img = image.open(image_path)

    # Convert the image to RGB mode (if it's not already in that mode)
    img = img.convert('RGB')

    # Get image size
    imx = img.size[0]
    imy = img.size[1]

    if imx > 100 and imy > 100:
    # Resize the image to 100x100
        img = img.resize((500, 500))
        print("Resized Size - Width:", 100, "Height:", 100)
    width, height = img.size

    # Calculate the number of blocks in each dimension
    num_blocks_x = width // block_size
    num_blocks_y = height // block_size

    # Create an empty array to store the pixelated image
    pixelated_img = np.zeros((height, width, 3), dtype=np.uint8)

    # Iterate over each block
    for i in range(num_blocks_x):
        for j in range(num_blocks_y):
            # Calculate the boundaries of the current block
            x_start = i * block_size
            y_start = j * block_size
            x_end = x_start + block_size
            y_end = y_start + block_size

            # Extract the pixels of the current block
            block_pixels = np.array(img.crop((x_start, y_start, x_end, y_end)))

            # Calculate the average color of the block
            average_color = np.mean(block_pixels, axis=(0, 1)).astype(np.uint8)

            # Fill the block with the average color
            pixelated_img[y_start:y_end, x_start:x_end, :] = average_color

    return pixelated_img