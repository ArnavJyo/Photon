import matplotlib.pyplot as plt
import numpy as np
import random, math
from PIL import Image as image
def setRange(value, smin, smax, dmin, dmax):
    '''
    Linear interpolation
    '''
    value = float(value)
    smin, smax = float(smin), float(smax)
    dmin, dmax = float(dmin), float(dmax)
    out = dmin + ((value - smin)/(smax - smin))*(dmax - dmin)
    return int(out)
class PointAdd:
    def __init__(self, tx, ty, cd,imgOut):
        self.tx = tx
        self.ty = ty
        self.cd = cd
        self.imgOut = imgOut
        self.sb = 8            # space between the center of the points
        self.minSize = 2        # minimum size
        self.maxSize = 6     # maximum size
        self.dispMult = 1.0     # channel dispersion
        self.cnorm = False      # switch for color normalization
        self.antAlsg = 1        # circle antialiasing
    
    
    def setRad(self, ioc):
        '''
        Radius definition
        '''
        self.rad = setRange(self.cd[ioc], 0, 255, self.minSize, self.maxSize)
    
    def circle(self, ioc):
        '''
        Draw a circle
        '''
        r1 = self.rad
        r2 = self.rad + self.antAlsg
        disp = (self.sb*0.5 - self.rad)*self.dispMult
        dispx = int(random.uniform(- disp, disp))
        dispy = int(random.uniform(- disp, disp))
        tx = self.tx + dispx
        ty = self.ty + dispy
        for y in range(ty - r2, ty + r2):
            for x in range(tx - r2, tx + r2):
                try:
                    dx = math.pow(tx - x, 2.0)
                    dy = math.pow(ty - y, 2.0)
                    r = math.sqrt(dx + dy)
                    if r <= r1:
                        ca = 1
                    elif r > r2:
                        ca = 0
                    else:
                        ca = (r2 - r)/(r2 - r1)
                    cdt = self.imgOut.getpixel((x, y))
                    if(self.cnorm == True):
                        cc = int(255*ca + cdt[ioc])
                    else:
                        cc = int(self.cd[ioc]*ca + cdt[ioc])
                    if(ioc == 0):
                        self.imgOut.putpixel((x, y), (cc, cdt[1], cdt[2]))
                    elif(ioc == 1):
                        self.imgOut.putpixel((x, y), (cdt[0], cc, cdt[2]))
                    else:
                        self.imgOut.putpixel((x, y), (cdt[0], cdt[1], cc))
                except:
                    continue
class PointSub:
    def __init__(self, tx, ty, cd,imgOut):
        self.tx = tx
        self.ty = ty
        self.cd = cd
        self.imgOut = imgOut
        self.sb = 8               # space between the center of points
        self.minSize = 2           # minimum size
        self.maxSize = 6          # maximum size
        self.dispMult = 0.75       # channel dispersion
        self.cnorm = True          # switch for color normalization
        self.antAlsg = 1           # circle antialiasing
    
    def setRad(self, ioc):
        '''
        Radius definition
        '''
        self.rad = setRange(self.cd[ioc], 0, 255, self.maxSize, self.minSize)
    
    def circle(self, ioc):
        '''
        Draw circle
        '''
        r1 = self.rad
        r2 = self.rad + self.antAlsg
        disp = (self.sb*0.5 - self.rad)*self.dispMult
        dispx = int(random.uniform(- disp, disp))
        dispy = int(random.uniform(- disp, disp))
        tx = self.tx + dispx
        ty = self.ty + dispy
        for y in range(ty - r2, ty + r2):
            for x in range(tx - r2, tx + r2):
                try:
                    dx = math.pow(tx - x, 2.0)
                    dy = math.pow(ty - y, 2.0)
                    r = math.sqrt(dx + dy)
                    if r <= r1:
                        ca = 1
                    elif r > r2:
                        ca = 0
                    else:
                        ca = (r2 - r)/(r2 - r1)
                    cdt = self.imgOut.getpixel((x, y))
                    if(self.cnorm == True):
                        cc = int(cdt[ioc] - 255*ca)
                    else:
                        cc = int(cdt[ioc] - self.cd[ioc]*ca)
                    if(ioc == 0):
                        self.imgOut.putpixel((x, y), (cc, cdt[1], cdt[2]))
                    elif(ioc == 1):
                        self.imgOut.putpixel((x, y), (cdt[0], cc, cdt[2]))
                    else:
                        self.imgOut.putpixel((x, y), (cdt[0], cdt[1], cc))
                except:
                    continue
def halftone_add(img_path):
    sb = 12            # space between the center of the points
    minSize = 2        # minimum size
    maxSize = 4        # maximum size
    dispMult = 1.0     # channel dispersion
    cnorm = False      # switch for color normalization
    antAlsg = 1        # circle antialiasing
    BG = (10, 15, 20)  # background color

# init 
    img = image.open(img_path)
    imx = img.size[0]
    imy = img.size[1]
    if imx > 100 and imy > 100:
    # Resize the image to 500x500
        img = img.resize((500, 500))
        print("Resized Size - Width:", 500, "Height:", 500)
    imx = img.size[0]
    imy = img.size[1]
    imgIn = image.new('RGB', img.size)
    imgIn.paste(img)
    imgOut = image.new('RGB', img.size, BG)
    imgIn = image.new('RGB', img.size)
    imgIn.paste(img)
    imgOut = image.new('RGB', img.size, BG)

# execution
    lpt = []
    y, i = 0, 0
    while(y < imy):
        x = int(sb*0.5)*(i % 2)     # shifting points in the even lines
        while(x < imx):
            cd = imgIn.getpixel((x, y))
            temp = PointAdd(x, y, cd,imgOut)
            lpt.append(temp)
            x += sb
        i += 1
        y += sb
    for channel in range(3):
        for point in lpt:
            point.setRad(channel)
            point.circle(channel)
    img_array = np.array(imgOut)

    return img_array
def halftone_sub(img_path):
    sb = 12               # space between the center of points
    minSize = 2           # minimum size
    maxSize = 6           # maximum size
    dispMult = 0.75       # channel dispersion
    cnorm = True          # switch for color normalization
    antAlsg = 1           # circle antialiasing
    BG = (220, 220, 220)  # background color

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
    imgIn = image.new('RGB', img.size)
    imgIn.paste(img)
    imgOut = image.new('RGB', img.size, BG)

# execution
    lpt = []
    y, i = 0, 0
    while(y < imy):
        x = int(sb*0.5)*(i % 2)     # shifting points in the even lines
        while(x < imx):
            cd = imgIn.getpixel((x, y))
            temp = PointSub(x, y, cd,imgOut)
            lpt.append(temp)
            x += sb
        i += 1
        y += sb
    for channel in range(3):
        for point in lpt:
            point.setRad(channel)
            point.circle(channel)
    img_array = np.array(imgOut)

    return img_array