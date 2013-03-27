import tornado.ioloop
import tornado.web
import os
import handler
import page_render

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": False,
}

application = tornado.web.Application([
    (r"/", page_render.MainPage),
    (r"/manage", page_render.ManagePage),
    (r"/staff_info", page_render.StaffInfoPage),
    (r"/staff_record", page_render.StaffRecordPage),
    (r"/addstaff", page_render.AddStaffPage),

    (r"/login", handler.LoginHandler),
    (r"/logout", handler.LogoutHandler),
    (r"/recognise", handler.RecogniseHandler),
    (r"/add_new_staff", handler.AddStaffHandler),
    (r"/upload_image", handler.UploadIMGHandler),
    (r"/record_info", handler.RecordInfoHandler),
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], debug = True, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
