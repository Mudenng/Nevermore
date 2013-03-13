import tornado.ioloop
import tornado.web
import os
import StringIO
import numpy
import cv
import cv2
from PIL import Image
import base64
import time
import face_detect
import face_recognise
import pic_pretreatment
import dbhandler

TIMEFORMAT = "%Y-%m-%d %X"

class MainPage(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class RecogniseHandler(tornado.web.RequestHandler):
    def post(self):
        pic = self.get_argument("pic")
        picData = base64.b64decode(pic)
        buf = StringIO.StringIO()
        buf.write(picData)
        buf.seek(0)
        # face detection
        region = face_detect.process(imgData = buf)
        # pretreatment
        if region:
            cvEquHist = pic_pretreatment.process(region)
            cv2Data = numpy.asarray(cvEquHist[:])
            # get mean and eigenvectors from DB
            db = dbhandler.DBHandler()
            try:
               mean, eigenvectors = db.get_pca()
            except:
                print "Error: Failed to get mean and eigenvectors from DB"
            # project
            # convert mean and eigenvectors
            mean_list = [float(i) for i in mean.split(" ")]
            mean_numpy = numpy.asarray(mean_list[:]).reshape(1, -1)

            vec_strings = [s for s in eigenvectors.split("|")]
            eigenvectors_list = []
            for vec_str in vec_strings:
                vec_list = [float(i) for i in vec_str.split(" ")]
                eigenvectors_list.append(vec_list)
            eigenvectors_numpy = numpy.asarray(eigenvectors_list[:]).reshape(len(eigenvectors_list),-1)

            # get eigenface
            eigenface = face_recognise.get_eigenface(mean_numpy, eigenvectors_numpy, cvData = cv2Data)
            # compute distance with all staffs
            min_dis = 1000000000
            sid = ""
            sname = ""
            staffs = db.look_table("staff")
            for staff in staffs:
                eface_str = staff["eigenface"]
                eface = [float(i) for i in eface_str.split(" ")]
                dis = numpy.linalg.norm(eigenface[0] - eface)
                if dis < min_dis:
                    min_dis = dis
                    sid = staff["sid"]
                    sname = staff["name"]
            self.write(sid + "|" + sname)
        else:
            self.write("failed")

class CheckinHandler(tornado.web.RequestHandler):
    def post(self):
        print self.get_argument("sid"), "checked in at", time.strftime(TIMEFORMAT, time.localtime())
        self.write("success")

class AddStaffPage(tornado.web.RequestHandler):
    def get(self):
        self.render("addstaff.html")

class UploadIMGHandler(tornado.web.RequestHandler):
    def post(self):
        # get picture and sid
        pic = self.get_argument("pic")
        sid = self.get_argument("sid")

        picData = base64.b64decode(pic)
        buf = StringIO.StringIO()
        buf.write(picData)
        buf.seek(0)
        face_tmp_path = "static/faces/%s_tmp.jpg" % sid
        grayface_tmp_path = "static/grayfaces/%s_tmp.jpg" % sid

        # face detection
        region = face_detect.process(imgData = buf, outfile = face_tmp_path)
        # pretreatment
        if region:
            pic_pretreatment.process(region, 
                                    equfile = grayface_tmp_path,
                                    )
            self.write("success")
        else:
            self.write("failed")

class AddStaffHandler(tornado.web.RequestHandler):
    def post(self):
        # get info
        name = self.get_argument("name")
        age = int(self.get_argument("age"))
        id = self.get_argument("id")
        sid = self.get_argument("sid")
        grayface_tmp_path = "static/grayfaces/%s_tmp.jpg" % sid
        db = dbhandler.DBHandler()

        # write staff information to DB
        try:
            db.add_staff(sid, name, age, id, eigenface = " ")
        except:
            print "Error: Add staff information failed. sid = %s" % sid
            self.write("failed")
            return False
        # write new face to DB
        grayface = cv2.imread(grayface_tmp_path, 0)
        grayface = grayface.reshape(100 * 100)
        grayface_str = ""
        for p in grayface:
            grayface_str += str(p)
            grayface_str += " "
        grayface_str = grayface_str[:-1]
        try:
            db.store_face(sid, grayface_str)
        except:
            print "Error: Store image to DB failed. sid = %s" % sid
            self.write("failed")
            return False

        # Compute PCA - Training
        mean, eigenvectors = face_recognise.computePCA()

        # Update all staffs' eigenface
        staffs = db.look_table("staff")
        for staff in staffs:
            sid = staff["sid"]
            try:
                records = db.get_face(sid)
            except:
                print "Error: Get image from DB failed. sid = %s" % sid
                self.write("failed")
                return False
            nm = numpy.fromstring(records[0]['img'], dtype = numpy.uint8, sep = " ")
            nm = nm.reshape(100, -1)
            eigenface = face_recognise.get_eigenface(mean, eigenvectors, cvData = nm)
            l = ["%.8f" % number for number in eigenface[0]]
            eigenface_str = " ".join(l)
            try:
                db.update_eigenface(sid, eigenface_str)
            except:
                print "Error: Write eigenface to DB failed. sid = %s" % sid
                self.write("failed")
                return False

        # Write mean and eigenvectors to DB
        # mean to string
        m = ["%.8f" % number for number in mean[0]]
        mean_str = " ".join(m)
        # eigenvectors to string
        eigenvectors_str = ""
        for vec in eigenvectors:
            v = ["%.8f" % number for number in vec]
            vec_str = " ".join(v)
            eigenvectors_str += vec_str
            eigenvectors_str += "|"
        eigenvectors_str = eigenvectors_str[:-1]
        try:
            db.update_pca(mean_str, eigenvectors_str)
        except:
            print "Error: Update mean and eigenvectors to DB failed. "
            self.write("failed")
            return False

        os.remove(grayface_tmp_path)
        self.write("success")


class PicProcessHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("picprocess.html", 
                    original = "static/original.jpg", 
                    detected = "static/detected.jpg", 
                    gray = "static/gray.jpg", 
                    smooth = "static/smooth.jpg",
                    equ = "static/equ.jpg",
                    )


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": False,
}

application = tornado.web.Application([
    (r"/", MainPage),
    (r"/recognise", RecogniseHandler),
    (r"/checkin", CheckinHandler),
    (r"/addstaff", AddStaffPage),
    (r"/add_new_staff", AddStaffHandler),
    (r"/upload_image", UploadIMGHandler),
    (r"/picprocess", PicProcessHandler),
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], debug = True, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
