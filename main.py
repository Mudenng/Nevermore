import tornado.ioloop
import tornado.web
import os
import base64

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html", title="main")

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.get_argument("data")
        picData = base64.b64decode(data)
        pic_file = open("pic.png", "w")
        pic_file.write(picData)
        pic_file.close()

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": False,
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload", UploadHandler),
], debug=True, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
