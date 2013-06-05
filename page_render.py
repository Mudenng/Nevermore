import tornado.web
from datetime import datetime
import dbhandler
import handler
import records

class MainPage(tornado.web.RequestHandler):
    def get(self):
        self.render("static/html/main.html")

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

class AdminHomePage(handler.AuthAdminBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login_admin")
            return False;
        name = tornado.escape.xhtml_escape(self.current_user)
        db = dbhandler.DBHandler()
        atype = self.get_secure_cookie("atype")
        self.render("static/html/admin_home.html", name = name, atype = atype)

class AddStaffPage(handler.AuthAdminBaseHandler):
    def get(self):
        if not self.current_user or int(self.get_secure_cookie("atype")) == 2:
            self.redirect("/login_admin")
            return False;
        name = tornado.escape.xhtml_escape(self.current_user)
        self.render("static/html/add_staff.html", name = name)

class StaffsPage(handler.AuthAdminBaseHandler):
    def get(self):
        if not self.current_user or int(self.get_secure_cookie("atype")) == 2:
            self.redirect("/login_admin")
            return False;
        name = tornado.escape.xhtml_escape(self.current_user)
        self.render("static/html/staffs.html", name = name)

class AdminsPage(handler.AuthAdminBaseHandler):
    def get(self):
        if not self.current_user or int(self.get_secure_cookie("atype")) != 0:
            self.redirect("/login_admin")
            return False;
        name = tornado.escape.xhtml_escape(self.current_user)
        self.render("static/html/admins.html", name = name)

class ModifyStaffPage(handler.AuthAdminBaseHandler):
    def get(self):
        if not self.current_user or int(self.get_secure_cookie("atype")) == 2:
            self.redirect("/login_admin")
            return False;
        name = tornado.escape.xhtml_escape(self.current_user)
        sid = self.get_argument("sid")
        db = dbhandler.DBHandler()
        staff = db.get_staff(sid)[0]
        self.render("static/html/modify_staff.html", name = name, sid = staff['sid'], departid = staff['department'], sname = staff['name'], age = staff['age'], idnumber = staff['idnumber'], pwd = staff['pwd'], ondutytime = staff['ondutytime'], offdutytime = staff['offdutytime'])

class ModifyAdminPage(handler.AuthAdminBaseHandler):
    def get(self):
        if not self.current_user or int(self.get_secure_cookie("atype")) != 0:
            self.redirect("/login_admin")
            return False;
        name = tornado.escape.xhtml_escape(self.current_user)
        aid = int(self.get_argument("aid"))
        db = dbhandler.DBHandler()
        admin = db.get_admin(aid)[0]
        self.render("static/html/modify_admin.html", name = name, aid = admin['aid'], aname = admin['name'], pwd = admin['pwd'], power = admin['atype'])

class ConfigPage(handler.AuthAdminBaseHandler):
    def get(self):
        if not self.current_user or int(self.get_secure_cookie("atype")) == 1:
            self.redirect("/login_admin")
            return False;
        name = tornado.escape.xhtml_escape(self.current_user)
        db = dbhandler.DBHandler()
        sensitivity = int(db.get_setting("sensitivity"))
        ip_start = db.get_setting("ip_start")
        ip_end = db.get_setting("ip_end")
        self.render("static/html/config.html", name = name, sliderval = sensitivity, ipstart = ip_start, ipend = ip_end)

class CheckRecordsPage(handler.AuthAdminBaseHandler):
    def get(self):
        if not self.current_user or int(self.get_secure_cookie("atype")) == 2:
            self.redirect("/login_admin")
            return False;
        aname = tornado.escape.xhtml_escape(self.current_user)
        try:
            sid = self.get_argument("sid")
        except:
            sid = ""
        try:
            year = self.get_argument("year")
            month = self.get_argument("month")
        except:
            year = datetime.now().year
            month = datetime.now().month
        db = dbhandler.DBHandler()
        staff = db.get_staff(sid)
        if not sid or len(sid) == 0 or len(staff) == 0:
            self.render("static/html/check_records.html", aname = aname, sid = "", onduty = "none", offduty = "none", year = year, month = month)
        else:
            r = records.staff_monthly_record(sid, str(year), str(month))
            self.render("static/html/check_records.html", 
                        aname = aname,
                        sid = sid,
                        onduty = r[0],
                        offduty = r[1],
                        year = year,
                        month = month,
                       )

class RecordSumPage(handler.AuthAdminBaseHandler): 
    def get(self):
        if not self.current_user or int(self.get_secure_cookie("atype")) == 2:
            self.redirect("/login_admin")
            return False;
        db = dbhandler.DBHandler()
        name = tornado.escape.xhtml_escape(self.current_user)
        data = [20.123,13.4,2.0,4.2,4.52,21.1,8.3]
        try:
            year = self.get_argument("year")
            month = self.get_argument("month")
        except:
            year = datetime.now().year
            month = datetime.now().month
        departmentID = db.get_allDepartment()
        dataOnduty = [0]*len(departmentID)
        dataOffduty = [0]*len(departmentID)
        # countOnPie = [20.1,20.5,29.5,10.6,19.3]
        # countOffPie = [19.3,29.5,20.5,20.1,10.6]
        # countOnBar = [1.1,2.3,6.7,9.2,1.2]
        # countOffBar = [3.1,1.3,8.7,5.2,4.2]
        #Please uncomment
        countOnPie = [0]*len(departmentID)
        countOffPie = [0]*len(departmentID)
        countOnBar = [0]*len(departmentID)
        countOffBar = [0]*len(departmentID)
        sids = db.get_allStaff()
        for sid in sids:
            r = records.staff_monthly_record(sid["sid"], str(year), str(month))
            countOnBar[sid["department"]] = countOnBar[sid["department"]] + (r[0].count('1')+r[0].count('0'))
            countOffBar[sid["department"]] = countOffBar[sid["department"]] + (r[1].count('1')+r[1].count('2')+r[1].count('0'))
            dataOnduty[sid["department"]] = dataOnduty[sid["department"]] + (r[0].count('1')-r[0].count('-1'))
            dataOffduty[sid["department"]] = dataOffduty[sid["department"]] + r[1].count('2')
        tempOnPie = sum(dataOnduty)
        tempOffPie = sum(dataOffduty)
        for x in xrange(0,len(departmentID)):
            countOnBar[x] = dataOnduty[x] / float(countOnBar[x])
            countOffBar[x] = dataOffduty[x] / float(countOffBar[x])
            if tempOnPie != 0:
                countOnPie[x] = dataOnduty[x] / float(tempOnPie)
            if tempOffPie != 0:
                countOffPie[x] = dataOffduty[x] / float(tempOffPie)
        # self.render("static/html/record_sum.html", name = name,dataOnduty = dataOnduty,dataOffduty = dataOffduty,year = year,month = month)
        self.render("static/html/record_sum.html", name = name,countOnBar = countOnBar,
            countOffBar = countOffBar,countOnPie = countOnPie,countOffPie = countOffPie,
            year = year,month = month)
