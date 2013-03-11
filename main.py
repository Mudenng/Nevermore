import tornado.ioloop
import tornado.web
import os
import StringIO
import numpy
import cv
from PIL import Image
import base64
import face_detect
import face_recognise
import pic_pretreatment
import dbhandler

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
            min_dis = 10000000
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

            self.write(sname)
        else:
            self.write("failed")


class AddStaffPage(tornado.web.RequestHandler):
    def get(self):
        self.render("addstaff.html")

class UploadIMGHandler(tornado.web.RequestHandler):
    def post(self):
        # get picture and sid
        pic = self.get_argument("pic")
        sid = self.get_argument("sid")

        picData = base64.b64decode(pic)
        original_tmp_path = "static/original/%s_tmp.jpg" % sid
        face_tmp_path = "static/faces/%s_tmp.jpg" % sid
        grayface_tmp_path = "static/grayfaces/%s_tmp.jpg" % sid
        pic_file = open(original_tmp_path, "w")
        pic_file.write(picData)
        pic_file.close()
        # face detection
        region = face_detect.process(infile = original_tmp_path, outfile = face_tmp_path)
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
        original_tmp_path = "static/original/%s_tmp.jpg" % sid
        face_tmp_path = "static/faces/%s_tmp.jpg" % sid
        grayface_tmp_path = "static/grayfaces/%s_tmp.jpg" % sid
        grayface_pic_path = "static/grayfaces/%s.jpg" % sid
        
        # PCA 
        mean, eigenvectors = face_recognise.computePCA("static/grayfaces")  # training
        eigenface = face_recognise.get_eigenface(mean, eigenvectors, grayface_pic_path = grayface_tmp_path) # get eigenface
        l = ["%.8f" % number for number in eigenface[0]]
        eigenface_string = " ".join(l)
        
        # write to db
        try:
            db = dbhandler.DBHandler()
            # update mean and eigenvectors
            # mean to string
            m = ["%.8f" % number for number in mean[0]]
            mean_string = " ".join(m)
            # eigenvectors to string
            eigenvectors_string = ""
            for vec in eigenvectors:
                v = ["%.8f" % number for number in vec]
                vec_string = " ".join(v)
                eigenvectors_string += vec_string
                eigenvectors_string += "|"
            eigenvectors_string = eigenvectors_string[:-1]
            # update db
            db.update_pca(mean_string, eigenvectors_string)

            # add new staff information
            db.add_staff(sid, name, age, id, grayface_pic_path, eigenface_string)

            # rename pictures
            os.rename(original_tmp_path, "static/original/%s.jpg" % sid)
            os.rename(face_tmp_path, "static/faces/%s.jpg" % sid)
            os.rename(grayface_tmp_path, grayface_pic_path)

            # update all other staffs' eigenface
            staffs = db.look_table("staff")
            for record in staffs:
                spic = record['spic']
                sid = record['sid']
                eigenface = face_recognise.get_eigenface(mean, eigenvectors, grayface_pic_path = spic)
                l = ["%.8f" % number for number in eigenface[0]]
                eigenface_string = " ".join(l)
                db.update_eigenface(sid, eigenface_string)
            self.write("success")
        except:
            # delete temp pictures
            os.remove(original_tmp_path)
            os.remove(face_tmp_path)
            os.remove(grayface_tmp_path)
            self.write("failed")


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
    (r"/addstaff", AddStaffPage),
    (r"/add_new_staff", AddStaffHandler),
    (r"/upload_image", UploadIMGHandler),
    (r"/picprocess", PicProcessHandler),
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], debug = True, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
