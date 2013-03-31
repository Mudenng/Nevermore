import os
import cv2 as cv
import numpy
import tornado.database
from PIL import Image

img = cv.imread(os.path.join(os.path.dirname(__file__), "999.jpg"), 0)
img = img.reshape(100*100)
print img.shape
'''
s = ""
for d in img:
    s += str(d)
    s += " "
s = s[:-1]
#print s 
#print nn.shape
db = tornado.database.Connection("localhost", "nevermore", "root")
#db.execute("INSERT INTO image (id, img) VALUES ('%s', '%s')" % ("0", s))
r = db.query("SELECT img FROM image WHERE id = '0'")
nn = numpy.fromstring(r[0]['img'], dtype = numpy.uint8, sep = " ")
nn = nn.reshape(100, -1)
pic = Image.fromarray(nn)
#pic.show()
'''


