import tornado.web

class MainPage(tornado.web.RequestHandler):
    def get(self):
        self.render("html/main.html")

class AddStaffPage(tornado.web.RequestHandler):
    def get(self):
        self.render("html/addstaff.html")
