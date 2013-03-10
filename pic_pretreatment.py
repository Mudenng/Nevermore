from PIL import Image
import cv
import numpy

def convert_gray(cvRgbImage):
    # opencv to gray picture
    grayscale = cv.CreateImage((cvRgbImage.width, cvRgbImage.height), 8, 1)
    cv.CvtColor(cvRgbImage, grayscale, cv.CV_BGR2GRAY)
    return grayscale

def smooth(cvImage):
    cv.Smooth(cvImage, cvImage, cv.CV_GAUSSIAN, param1 = 3, param2 = 0, param3 = 0, param4 = 0)
    return cvImage

def equalizeHist(cvGrayImage):
    cv.EqualizeHist(cvGrayImage, cvGrayImage)
    return cvGrayImage


def process(image, grayfile = None, smoothfile = None, equfile = None):
    # Resize picture
    width = 100
    height = 100
    image = image.resize((width, height), Image.ANTIALIAS)
    # PIL to opencv
    bgrImage = numpy.array(image)
    cvBgrImage = cv.fromarray(bgrImage)
    # Reverse BGR
    cvRgbImage = cv.CreateImage(cv.GetSize(cvBgrImage),8,3)
    cv.CvtColor(cvBgrImage, cvRgbImage, cv.CV_BGR2RGB)

    # To gray
    cvGrayScale = convert_gray(cvRgbImage)
    if cvGrayScale:
        if grayfile:
            gray_image = Image.fromstring("L", cv.GetSize(cvGrayScale), cvGrayScale.tostring())
            gray_image.save(grayfile, "JPEG", quality = 80)
    else:
        print "Error: cannot convert to gray image"
        return
    # Gaussian smooth
    cvSmooth = smooth(cvGrayScale)
    if cvSmooth:
        if smoothfile:
            smooth_image = Image.fromstring("L", cv.GetSize(cvSmooth), cvSmooth.tostring())
            smooth_image.save(smoothfile, "JPEG", quality = 80)
    else:
        print "Error: cannot do gaussion smooth"
        return
    # Equalize hist
    cvEquHist = equalizeHist(cvSmooth)
    if cvEquHist:
        if equfile:
            equ_image = Image.fromstring("L", cv.GetSize(cvEquHist), cvEquHist.tostring())
            print equ_image
            equ_image.save(equfile, "JPEG", quality = 80)
            # data = list(equ_image.getdata())
            # print data
    else:
        print "Error: cannot do equlize hist"
        return
    return cvEquHist

