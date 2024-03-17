import numpy as np
import random
from PIL import Image as image
class Segment:
    def __init__(self, tx, ty, width, offset, orient,size):
        self.size = size
        self.tx = tx + int(self.size*0.5)
        self.ty = ty + int(self.size*0.5)
        self.width = int(self.size*width)
        self.offset = int(self.size*offset) - int(self.size*0.5)
        self.orient = orient
    
    def kernel(self):
        '''
        Kernel definition
        '''
        self.xmin = self.tx - int(self.size*0.5)
        self.xmax = self.tx + int(self.size*0.5)
        self.ymin = self.ty - int(self.size*0.5)
        self.ymax = self.ty + int(self.size*0.5)
    
    def getColor(self,imgIn):
        '''
        Segment color
        '''
        cr, cg, cb = 0, 0, 0
        count = 0
        for y in range(self.ymin, self.ymax):
            for x in range(self.xmin, self.xmax):
                try:
                    c = imgIn.getpixel((x, y))
                    cr += c[0]
                    cg += c[1]
                    cb += c[2]
                    count += 1
                except:
                    continue
        if count !=0:
            cr = int(cr/count)
            cg = int(cg/count)
            cb = int(cb/count)
            self.cd = (cr, cg, cb)
    
    def draw(self,imgOut):
        '''
        Draw a segment
        '''
        for y in range(self.ymin, self.ymax):
            for x in range(self.xmin, self.xmax):
                try:
                    lim = max(self.xmax + self.ymin + self.offset, self.xmin + self.ymax + self.offset)
                    if ((x + y) >= lim - self.width) & ((x + y) < lim + self.width - 1):
                        if self.orient == 0:
                            self.imgOut.putpixel((x, y), self.cd)
                        else:
                            imgOut.putpixel(((self.xmax + self.xmin - x - 1), y), self.cd)
                    else:
                        continue
                except:
                    continue

def segmentation(img_path):
    size = 16         # kernel size
    BG = (50, 50, 50) # background color
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
    los = []
    ty = 0
    while ty < imy:
        tx = 0
        while tx < imx:
            width = random.uniform(0.2, 0.4)
            offset = random.uniform(0.25, 0.75)
            orient = int(random.uniform(0, 2))
            temp = Segment(tx, ty, width, offset, orient,size)
            los.append(temp)
            tx += size
        ty += size

    for segm in los:
        segm.kernel()
        segm.getColor(imgIn)
        segm.draw(imgOut)
    img_array = np.array(imgOut)

    return img_array
