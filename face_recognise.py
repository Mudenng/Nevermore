import os
import cv2 as cv
import numpy


def computePCA(faces_path):
    raw_matrix = None
    # faces_path = os.path.join(os.path.dirname(__file__), "equ")
    for image in os.listdir(faces_path):
        if "jpg" in image:
            imgraw = cv.imread(os.path.join(faces_path, image), 0)
            imgraw = imgraw.reshape(100 * 100)
            try:
                raw_matrix = numpy.vstack((raw_matrix, imgraw))
            except:
                raw_matrix = imgraw
    print "image matrix shape:", raw_matrix.shape
    # PCA
    mean, eigenvectors = cv.PCACompute(raw_matrix, numpy.mean(raw_matrix, axis=0).reshape(1,-1), maxComponents = 0)
    print "mean shape: ",mean.shape
    print "eigenvectors shape:", eigenvectors.shape
    return (mean, eigenvectors)

def get_eigenface(mean, eigenvectors, cvData = None, grayface_pic_path = None):
    if grayface_pic_path:
        image = cv.imread(grayface_pic_path, 0)
    else:
        image = cvData
    image = image.reshape(100 * 100)
    transimg = numpy.array([image])
    eigenface = cv.PCAProject(transimg, mean, eigenvectors)
    return eigenface

if __name__ == "__main__":
    mean, eigenvectors = computePCA(os.path.join(os.path.dirname(__file__), "equ"))
    eigenface = get_eigenface(os.path.join(os.path.dirname(__file__), "s.jpg"), mean, eigenvectors)
    print eigenface
    l = ["%.8f" % number for number in eigenface[0]]
    print " ".join(l)
