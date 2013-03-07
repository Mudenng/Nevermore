import tornado.ioloop
import tornado.web
import os
import base64
import face_detect
import pic_pretreatment

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class UpLoadHandler(tornado.web.RequestHandler):
    def post(self):
        # get and save original picture
        data = self.get_argument("data")
        picData = base64.b64decode(data)
        pic_file = open("static/original.jpg", "w")
        pic_file.write(picData)
        pic_file.close()
        # face detection
        region = face_detect.process("static/original.jpg", "static/detected.jpg")
        # pretreatment
        pic_pretreatment.process(region, 
                                grayfile = "static/gray.jpg", 
                                smoothfile = "static/smooth.jpg",
                                equfile = "static/equ.jpg",
                                )
        self.write("uploadok")


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
    (r"/upload", UpLoadHandler),
    (r"/picprocess", PicProcessHandler),
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], debug = True, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
