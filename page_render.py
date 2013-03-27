import tornado.web
from datetime import datetime
import dbhandler
import handler
import records

class MainPage(tornado.web.RequestHandler):
    def get(self):
        self.render("static/html/main.html")

class AddStaffPage(tornado.web.RequestHandler):
    def get(self):
        self.render("static/html/addstaff.html")

class ManagePage(handler.AuthBaseHandler):
    @tornado.web.authenticated
    def get(self):
        sid = tornado.escape.xhtml_escape(self.current_user)
        db = dbhandler.DBHandler()
        staff = db.get_staff(sid)[0]
        sname = staff['name']
        self.render("static/html/manage.html", sname = sname)

class StaffInfoPage(handler.AuthBaseHandler):
    @tornado.web.authenticated
    def get(self):
        sid = tornado.escape.xhtml_escape(self.current_user)
        db = dbhandler.DBHandler()
        staff = db.get_staff(sid)[0]
        self.render("static/html/staff_info.html", 
                    sid = sid, 
                    sname = staff['name'], 
                    age = staff['age'], 
                    idnumber = staff['idnumber'], 
                    department = staff['department'],
                    ondutytime = staff['ondutytime'],
                    offdutytime = staff['offdutytime'],
                   )

class StaffRecordPage(handler.AuthBaseHandler):
    @tornado.web.authenticated
    def get(self):
        sid = tornado.escape.xhtml_escape(self.current_user)
        db = dbhandler.DBHandler()
        staff = db.get_staff(sid)[0]
        sname = staff['name']
        try:
            year = self.get_argument("year")
            month = self.get_argument("month")
        except:
            year = datetime.now().year
            month = datetime.now().month
        r = records.staff_monthly_record(sid, str(year), str(month))
        self.render("static/html/staff_record.html", 
                    sname = sname,
                    onduty = r[0],
                    offduty = r[1],
                    year = year,
                    month = month,
                   )

