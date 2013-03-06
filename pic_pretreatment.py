from PIL import Image
import cv
import numpy

def convert_gray(image):
    # PIL to opencv
    bgrImage = numpy.array(image)
    cvBgrImage = cv.fromarray(bgrImage)
    # Reverse BGR
    cvRgbImage = cv.CreateImage(cv.GetSize(cvBgrImage),8,3)
    cv.CvtColor(cvBgrImage, cvRgbImage, cv.CV_BGR2RGB)

    # opencv to PIL gray picture
    grayscale = cv.CreateImage((cvRgbImage.width, cvRgbImage.height), 8, 1)
    cv.CvtColor(cvRgbImage, grayscale, cv.CV_BGR2GRAY)

    return Image.fromstring("L", cv.GetSize(grayscale), grayscale.tostring())

def process(image, outfile):
    gray_image = convert_gray(image)
    if gray_image:
        gray_image.save(outfile, "JPEG", quality = 80)
    else:
        print "Error: cannot convert to gray image"
