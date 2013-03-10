import os
import cv2 as cv
import numpy


def process():
    raw_matrix = None
    faces_path = os.path.join(os.path.dirname(__file__), "equ")
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

    # test it!
    sample_img = cv.imread(os.path.join(os.path.dirname(__file__), "s.jpg"), 0)
    sample_img = sample_img.reshape(100 * 100)
    transimg = numpy.array([sample_img])
    sample_result = cv.PCAProject(transimg, mean, eigenvectors)
    min_dis = 1000000
    id = "xx"
    for image in os.listdir(faces_path):
        if "jpg" in image:
            imgraw = cv.imread(os.path.join(faces_path, image), 0)
            imgraw = imgraw.reshape(100 * 100)
            timg = numpy.array([imgraw])
            r = cv.PCAProject(timg, mean, eigenvectors)
            dis = numpy.linalg.norm(r - sample_result)
            if dis < min_dis:
                min_dis = dis
                id = image
    print id


if __name__ == "__main__":
    process()
