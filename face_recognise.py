import os
import cv2 as cv
import numpy
import dbhandler

MAX_COMPONENTS = 100

def computePCA(faces_path = None):
    raw_matrix = None
    if faces_path:
        for image in os.listdir(faces_path):
            if "jpg" in image:
                imgraw = cv.imread(os.path.join(faces_path, image), 0)
                imgraw = imgraw.reshape(100 * 100)
                try:
                    raw_matrix = numpy.vstack((raw_matrix, imgraw))
                except:
                    raw_matrix = imgraw
    else:
        db = dbhandler.DBHandler()
        records = db.look_table("images")
        for record in records:
            imgraw = numpy.fromstring(record['img'], dtype = numpy.uint8, sep = " ")
            try:
                raw_matrix = numpy.vstack((raw_matrix, imgraw))
            except:
                raw_matrix = imgraw

    # print "image matrix shape:", raw_matrix.shape

    # PCA
    mean, eigenvectors = cv.PCACompute(raw_matrix, numpy.mean(raw_matrix, axis = 0).reshape(1,-1), maxComponents = MAX_COMPONENTS)
    # print "mean shape: ", mean.shape
    # print "eigenvectors shape:", eigenvectors.shape
    return (mean, eigenvectors)

def get_eigenface(mean, eigenvectors, cvData = None, grayface_pic_path = None):
    if grayface_pic_path:
        image = cv.imread(grayface_pic_path, 0)
    else:
        image = cvData
    image = image.reshape(100 * 100)
    transimg = numpy.array([image])
    if eigenvectors.shape[0] <= 1:
        eigenface = numpy.asarray([[0]])
    else:
        eigenface = cv.PCAProject(transimg, mean, eigenvectors)
    return eigenface

if __name__ == "__main__":
    mean1, eigenvectors1 = computePCA(faces_path = os.path.join(os.path.dirname(__file__), "grayfaces"))
    mean2, eigenvectors2 = computePCA()
    print numpy.array_equal(mean1, mean2)
    print numpy.array_equal(eigenvectors1, eigenvectors2)
