import numpy as np
import random, math, time
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
def average(vec3):
    '''
    Returns the mean value between axes
    '''
    avr = int((vec3[0] + vec3[1] + vec3[2])/3.0)
    return avr

def midHigh(img):
    '''
    Returns the median and the maximum value of the input image
    '''
    imx = img.size[0]
    imy = img.size[1]
    mid = [0.0, 0.0, 0.0]
    high = [0.0, 0.0, 0.0]
    for y in range(imy):
        for x in range(imx):
            pix = img.getpixel((x, y))
            mid[0] += pix[0]
            mid[1] += pix[1]
            mid[2] += pix[2]
            if average(pix) > average(high): high = pix
            else: continue
    mid[0] = int(mid[0]/(imx*imy))
    mid[1] = int(mid[1]/(imx*imy))
    mid[2] = int(mid[2]/(imx*imy))
    return (tuple(mid), tuple(high))
class Point:
    def __init__(self, tx, ty, cd, lvl,imgOut):
        self.tx = tx
        self.ty = ty
        self.cd = tuple(cd)
        self.lod = 8         # level of detail
        self.minSamp = 0.001 # minimum probability
        self.maxSamp = 0.01  # maximum probability
        self.imgOut = imgOut
        self.minSize = 8     # minimum size
        self.maxSize = 32    # maximum size
        self.varSize = 0.5   # size deviation
        self.antAlsg = 1     # circle antialising level
        rad = setRange(lvl, self.lod - 1, 0, self.minSize, self.maxSize)
        self.rad = int(random.uniform(rad - rad*self.varSize, rad + rad*self.varSize))
    def circle(self):
        '''
        Draw a circle
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
def circle_scatter(imgpath):
    
# parameters
    lod = 8         # level of detail
    minSamp = 0.001 # minimum probability
    maxSamp = 0.01  # maximum probability
# init
    img = image.open(imgpath)
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
    midPix, highPix = midHigh(imgIn)
    highPixMax = max(highPix)
    imgOut = image.new('RGB', img.size, midPix)

# execution

    imgArr = np.asarray(imgIn)
    imgArrM = imgArr.max(axis=2)
    lpt = []
    for lvl in range(lod):
        mmin = int(lvl*highPixMax/lod)
        mmax = int((lvl + 1)*highPixMax/lod)
        sel = np.argwhere(np.logical_and(imgArrM > mmin,
                                     imgArrM <= mmax))
        sel = np.argwhere(imgArrM > mmin)
        np.random.shuffle(sel)
        lim = np.linspace(minSamp, maxSamp, lod)[lvl]
        lim = int(lim*len(sel))
        for py, px in sel[:lim]:
            cd = imgArr[py, px]
            lpt.append(Point(px, py, cd, lvl,imgOut))
        
    for point in lpt:
        point.circle()
    img_array = np.array(imgOut)

    return img_array


