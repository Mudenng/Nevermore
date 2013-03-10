import tornado.ioloop
import tornado.web
import os
import base64
import face_detect
import face_recognise
import pic_pretreatment
import dbhandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        pass
        # self.render("main.html")

class AddstaffPage(tornado.web.RequestHandler):
    def get(self):
        self.render("addstaff.html")

class UploadIMGHandler(tornado.web.RequestHandler):
    def post(self):
        # get picture and sid
        pic = self.get_argument("pic")
        sid = self.get_argument("sid")

        picData = base64.b64decode(pic)
        original_pic_path = "static/original/%s_tmp.jpg" % sid
        face_pic_path = "static/faces/%s_tmp.jpg" % sid
        grayface_pic_path = "static/grayfaces/%s_tmp.jpg" % sid
        pic_file = open(original_pic_path, "w")
        pic_file.write(picData)
        pic_file.close()
        # face detection
        region = face_detect.process(original_pic_path, face_pic_path)
        # pretreatment
        if region:
            pic_pretreatment.process(region, 
                                    equfile = grayface_pic_path,
                                    )
            self.write("success")
        else:
            self.write("failed")

class AddstaffHandler(tornado.web.RequestHandler):
    def post(self):
        # get info
        name = self.get_argument("name")
        age = int(self.get_argument("age"))
        id = self.get_argument("id")
        sid = self.get_argument("sid")
        original_pic_path = "static/original/%s_tmp.jpg" % sid
        face_pic_path = "static/faces/%s_tmp.jpg" % sid
        grayface_pic_path = "static/grayfaces/%s_tmp.jpg" % sid
        
        # PCA 
        mean, eigenvectors = face_recognise.computePCA("static/grayfaces")                  # training
        eigenface = face_recognise.get_eigenface(grayface_pic_path, mean, eigenvectors)     # get eigenface
        l = ["%.8f" % number for number in eigenface[0]]
        eigenface_string = " ".join(l)
        
        # write to db
        try:
            db = dbhandler.DBHandler()
            db.add_staff(sid, name, age, id, grayface_pic_path, eigenface_string)
            # rename pictures
            os.rename(original_pic_path, "static/original/%s.jpg" % sid)
            os.rename(face_pic_path, "static/faces/%s.jpg" % sid)
            os.rename(grayface_pic_path, "static/grayfaces/%s.jpg" % sid)
            self.write("success")
        except:
            # delete temp pictures
            os.remove(original_pic_path)
            os.remove(face_pic_path)
            os.remove(grayface_pic_path)
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
    (r"/", MainHandler),
    (r"/addstaff", AddstaffPage),
    (r"/add_new_staff", AddstaffHandler),
    (r"/upload_image", UploadIMGHandler),
    (r"/picprocess", PicProcessHandler),
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], debug = True, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
