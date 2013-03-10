from PIL import Image
import cv 
  
def detect_object(image):
    grayscale = cv.CreateImage((image.width, image.height), 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
  
    cascade = cv.Load("static/haarcascade_frontalface_default.xml")
    rect = cv.HaarDetectObjects(grayscale, cascade, cv.CreateMemStorage(), 1.1, 2,
        cv.CV_HAAR_DO_CANNY_PRUNING, (20,20))

    result = []
    for r in rect:
        result.append((r[0][0], r[0][1], r[0][0]+r[0][2], r[0][1]+r[0][3]))
    return result
  
def process(infile, outfile = None):
    # detect face
    image = cv.LoadImage(infile);
    if image:
        faces = detect_object(image) 

    # get face region picture
    if faces:
        im = Image.open(infile)
        box = faces[0]
        # save face region
        im = im.crop(box)
        if outfile:
            im.save(outfile, "JPEG", quality = 80)
    else:
        print "Error: cannot detect faces on %s" % infile
    return im
