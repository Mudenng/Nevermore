import dbhandler
import numpy
from PIL import Image

db = dbhandler.DBHandler()
r = db.look_table("settings")
records = db.get_face("001")
nm = numpy.fromstring(records[0]['img'], dtype = numpy.uint8, sep = " ")
nm = nm.reshape(100, -1)
image = Image.fromarray(nm)
image.show()
