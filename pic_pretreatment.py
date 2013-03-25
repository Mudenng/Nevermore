from PIL import Image
import cv
import numpy
import wavepy as wv

def equalizeHist(cvImage):
    cv.EqualizeHist(cvImage, cvImage)
    return cvImage

def powerTransform(cvImage, c, r):
    lut = cv.CreateMat(256, 1, cv.CV_8U)
    for i in range(256):
        v = cv.Round(c * pow(i / 255.0, r) * 255);
        if( v < 0 ):
            v = 0;
        if( v > 255 ):
            v = 255;
        lut[i,0] = v;
    cv.LUT(cvImage, cvImage, lut);
    return cvImage

def DWT(pilImage, j):
    x = numpy.asarray(pilImage)
    nm = 'bior3.7'
    ext = 'per'
    [dwtop,length,flag] = wv.dwt.dwt2(x, j, nm, ext)
    disp = wv.dwt.dispdwt(dwtop, length, j)
    length2 = wv.dwt.out_dim(length, j)
    l0 = length2[0]
    l1 = length2[1]
    disp[disp < 0.0] = 0.0
    disp[0:l0, 0:l1] = disp[0:l0, 0:l1] * 255.0 / disp.max()
    disp[disp > 255.0] = 255.0
    disp2 = disp[0:l0, 0:l1]
    pilImage = Image.fromarray(disp2)
    return pilImage

def process(image, grayfile = None, equfile = None, powfile = None, dwtfile = None):
    # Do DWT
    # image = DWT(image, 1)
    # Resize picture
    width = 100
    height = 100
    image = image.resize((width, height), Image.ANTIALIAS)
    if dwtfile:
        image = image.convert("L")
        image.save(dwtfile, "JPEG", quality = 100)

    # PIL to opencv
    cvImage = cv.CreateImageHeader(image.size, cv.IPL_DEPTH_8U, 1)
    cv.SetData(cvImage, image.tostring())

    # Equalize hist
    cvEquHist = equalizeHist(cvImage)
    if cvEquHist:
        if equfile:
            equ_image = Image.fromstring("L", cv.GetSize(cvEquHist), cvEquHist.tostring())
            # print equ_image
            equ_image.save(equfile, "JPEG", quality = 100)
            # data = list(equ_image.getdata())
            # print data
    else:
        print "Error: cannot do equlize hist"
        return

    # Power transform
    cvPow = powerTransform(cvEquHist, 1, 0.19)
    if cvPow:
        if powfile:
            pow_image = Image.fromstring("L", cv.GetSize(cvPow), cvPow.tostring())
            pow_image.save(powfile, "JPEG", quality = 100)
    else:
        print "Error: cannot do power transform"
        return

    return cvPow
