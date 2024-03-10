import numpy as np
import random, math, time
from PIL import Image as image

def averColor(color):
    '''
    Returns the mean value between channels
    '''
    cr = float(color[0])
    cg = float(color[1])
    cb = float(color[2])
    cd = (cr + cg + cb)/3
    return cd

def setRange(value, smin, smax, dmin, dmax):
    '''
    Linear interpolation
    '''
    value = float(value)
    smin, smax = float(smin), float(smax)
    dmin, dmax = float(dmin), float(dmax)
    out = dmin + ((value - smin)/(smax - smin))*(dmax - dmin)
    return int(out)

class Point:
    def __init__(self, tx, ty,imgIn,imgOut):
        self.tx = tx
        self.ty = ty
        self.imgIn = imgIn
        self.imgOut = imgOut
        self.sb = 8             # space between strings
        self.minSize = 0        # minimum size
        self.maxSize = 5        # maximum size
        self.antAlsg = 1  
    
    def setColor(self):
        '''
        Color defining
        '''
        self.cd = self.imgIn.getpixel((self.tx, self.ty))
    
    def setRad(self):
        '''
        Radius defining
        '''
        try:
            apix = averColor(self.cd)
            self.rad = setRange(apix, 0, 255, self.minSize, self.maxSize)
        except:
            self.rad = self.minSize
    
    def circle(self):
        '''
        Draw circle
        '''
        r1 = self.rad
        r2 = self.rad + self.antAlsg
        for y in range(self.ty - r2, self.ty + r2):
            for x in range(self.tx - r2, self.tx + r2):
                try:
                    dx = math.pow(self.tx - x, 2.0)
                    dy = math.pow(self.ty - y, 2.0)
                    r = math.sqrt(dx + dy)
                    if r <= r1:
                        self.imgOut.putpixel((x, y), self.cd)
                    elif r > r2:
                        cdt = self.imgOut.getpixel((x, y))
                        self.imgOut.putpixel((x, y), cdt)
                    else:
                        cdt = self.imgOut.getpixel((x, y))
                        ca = (r2 - r)/(r2 - r1)
                        cr = int(self.cd[0]*ca + cdt[0]*(1 - ca))
                        cg = int(self.cd[1]*ca + cdt[1]*(1 - ca))
                        cb = int(self.cd[2]*ca + cdt[2]*(1 - ca))
                        self.imgOut.putpixel((x, y), (cr, cg, cb))
                except:
                    continue
def strings(img_path):
    
    # parameters
    sb = 8             # space between strings
    minSize = 0        # minimum size
    maxSize = 5        # maximum size
    antAlsg = 1        # circle antialising level
    BG = (100, 0, 100) # background color

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

    # ececution
    lpt = []
    for x in range(0, imx - 1, sb):
        for y in range(imy - 1):
            p = Point(x, y,imgIn,imgOut)
            lpt.append(p)

    for point in lpt:
        point.setColor()
        point.setRad()
        point.circle()

    img_array = np.array(imgOut)

    return img_array
