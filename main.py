import tornado.ioloop
import tornado.web
import os
import sys
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
    (r"/staffs", page_render.StaffsPage),
    (r"/admins", page_render.AdminsPage),

    (r"/admin_home", page_render.AdminHomePage),
    (r"/add_staff", page_render.AddStaffPage),
    (r"/modify_staff", page_render.ModifyStaffPage),
    (r"/check_records", page_render.CheckRecordsPage),
    (r"/record_sum",page_render.RecordSumPage),
    (r"/modify_admin", page_render.ModifyAdminPage),
    (r"/config", page_render.ConfigPage),

    (r"/login", handler.LoginHandler),
    (r"/login_admin", handler.LoginAdminHandler),
    (r"/logout", handler.LogoutHandler),
    (r"/logout_admin", handler.LogoutAdminHandler),

    (r"/recognise", handler.RecogniseHandler),

    (r"/add_new_staff", handler.AddStaffHandler),
    (r"/upload_image", handler.UploadIMGHandler),
    (r"/checksid", handler.CheckSIDHandler),
    (r"/staff_list", handler.StaffListHandler),
    (r"/admins_list", handler.AdminsListHandler),
    (r"/update_staff", handler.UpdateStaffHandler),
    (r"/delete_staff", handler.DeleteStaffHandler),
    (r"/record_detail", handler.CheckRecordHandler),
    (r"/record_chg", handler.RecordChangeHandler),
    (r"/record_add", handler.RecordAddHandler),
    (r"/add_admin", handler.AddAdminHandler),
    (r"/delete_admin", handler.DeleteAdminHandler),
    (r"/update_admin", handler.UpdateAdminHandler),
    (r"/change_settings", handler.ChangeSettingsHandler),

    (r"/record_info", handler.RecordInfoHandler),

    (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], debug = True, **settings)

if __name__ == "__main__":
    port = int(sys.argv[1])
    application.listen(port)
    print "Server runing at port %d" % port
    tornado.ioloop.IOLoop.instance().start()
