import os
import cv
import numpy
from PIL import Image
import face_detect
import pic_pretreatment

if __name__ == "__main__":
    i = 0
    for image in os.listdir("raw"):
        imgpath = os.path.join("raw", image)
        equpath = os.path.join("equ", str(i) + ".jpg")
        i += 1
        # face detection
        region = face_detect.process(imgpath)
        # pretreatment
        pic_pretreatment.process(region, 
                                equfile = equpath,
                                )

