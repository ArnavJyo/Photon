import matplotlib.pyplot as plt
import numpy as np
import random, math, time
from PIL import Image as image
def euclidian_distance(img_path):
    n = 2054    # number of points 
    BG = (0, 0, 0) # background color
    img = image.open(img_path)
    imx = img.size[0]
    imy = img.size[1]
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
    imgOut = image.new('RGB', img.size, BG)


    cx = np.random.randint(0, imx, n)
# print(cx)
    cy = np.random.randint(0, imy, n)
# print(cy)
    pop = np.array([cx, cy]).T
# print(pop)

    for y in range(imy):
        for x in range(imx):
            d = np.sum(((x, y) - pop)**2, axis=1)**0.5
            NP = pop[np.argmin(d)]
            cd = imgIn.getpixel((int(NP[0]), int(NP[1])))
            imgOut.putpixel((x, y), cd)
    img_array = np.array(imgOut)

    return img_array
def minkowski_distance(img_path):
    n = 512        # number of points 
    p = 0.5        # minkowski's parameter
    BG = (0, 0, 0) # background color

    # init
    img = image.open(img_path)
    imx = img.size[0]
    imy = img.size[1]

    if imx > 100 and imy > 100:
    # Resize the image to 100x100
        img = img.resize((500, 500))
        print("Resized Size - Width:", 100, "Height:", 100)
    imgIn = image.new('RGB', img.size)
    imgIn.paste(img)
    imgOut = image.new('RGB', img.size, BG)
    imx = img.size[0]
    imy = img.size[1]
# execution
    cx = np.random.randint(0, imx, n)
    cy = np.random.randint(0, imy, n)
    pop = np.array([cx, cy]).T

    for y in range(imy):
        for x in range(imx):
            d = np.sum(abs((x, y) - pop)**p, axis=1)**(1/p)
            NP = pop[np.argmin(d)]
            cd = imgIn.getpixel((int(NP[0]), int(NP[1])))
            imgOut.putpixel((x, y), cd)
    img_array = np.array(imgOut)

    return img_array
def manhattan_distance(img_path):
    n = 1024       # number of points c
    sb = 4         # space between slices
    BG = (0, 0, 0) # background color

# init
    img = image.open(img_path)
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
    imgOut = image.new('RGB', img.size, BG)

# execution
    cx = np.random.randint(0, imx, n)
    cy = np.random.randint(0, imy, n)
    pop = np.array([cx, cy]).T

    for y in range(imy):
        for x in range(imx):
            d = np.sum(abs((x, y) - pop), axis=1)
            NP = pop[np.argmin(d)]
            cd = imgIn.getpixel((int(NP[0]), int(NP[1])))
            imgOut.putpixel((x, y), cd)
    img_array = np.array(imgOut)

    return img_array
def chebyshev_distance(img_path):
    n = 1024       # number of points c
    BG = (0, 0, 0) # background color
# init
    img = image.open(img_path)
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
    imgOut = image.new('RGB', img.size, BG)

# execution
    cx = np.random.randint(0, imx, n)
    cy = np.random.randint(0, imy, n)
    pop = np.array([cx, cy]).T

    for y in range(imy):
        for x in range(imx):
            d = abs((x, y) - pop).max(axis=1)
            NP = pop[np.argmin(d)]
            cd = imgIn.getpixel((int(NP[0]), int(NP[1])))
            imgOut.putpixel((x, y), cd)
    img_array = np.array(imgOut)

    return img_array
