#coding=utf-8
import dbhandler
from datetime import datetime

checkin_type = {'onduty':0, 'offduty':1}
checkin_state = {'ontime':0, 'late':1, 'early':2}

def checkin(sid, image_path):
    now = datetime.now()
    year, month, day, hour, minute = now.year, now.month, now.day, now.hour, now.minute
    now_str = now.strftime("%Y-%m-%d %H:%M")
    db = dbhandler.DBHandler()
    today_records = db.get_checkin_records(sid, ('%d-%d-%d 00:00:00' % (year, month, day)), ('%d-%d-%d 23:59:59' % (year, month, day)))
    print today_records
    if len(today_records) == 0:
        rtype = checkin_type['onduty']   # on duty
        staff = db.get_staff(sid)
        ondutytime = staff[0]["ondutytime"]
        ondutyhour = int(ondutytime.split(":")[0])
        ondutyminute = int(ondutytime.split(":")[1])
        if (hour * 60 + minute) <= (ondutyhour * 60 + ondutyminute):
            rstate = checkin_state['ontime']  # on time
            try:
                db.add_checkin_record(sid = sid, rtype = rtype, rstate = rstate, rimage = image_path)
                return ("您已完成考勤登记. 时间：%s . 考勤类型：%s . 考勤状态：%s ." % (now_str, "上班", "正常"), 1)
            except:
                print "Error: Write checkin record to DB failed. sid = %s" % sid
                return ("好像发生了一些错误，请重试.", -1)
        else:
            rstate = checkin_state['late']  # be late
            try:
                db.add_checkin_record(sid = sid, rtype = rtype, rstate = rstate, rimage = image_path)
                return ("您已完成考勤登记. 时间：%s . 考勤类型：%s . 考勤状态：%s ." % (now_str, "上班", "有点晚"), 1)
            except:
                print "Error: Write checkin record to DB failed. sid = %s" % sid
                return ("好像发生了一些错误，请重试.", -1)
    elif len(today_records) == 1:
        rtype = checkin_type['offduty']   # off duty
        staff = db.get_staff(sid)
        offdutytime = staff[0]["offdutytime"]
        offdutyhour = int(offdutytime.split(":")[0])
        offdutyminute = int(offdutytime.split(":")[1])
        if (hour * 60 + minute) <= (offdutyhour * 60 + offdutyminute):
            rstate = checkin_state['early']  # too early
            try:
                db.add_checkin_record(sid = sid, rtype = rtype, rstate = rstate, rimage = image_path)
                return ("您已完成考勤登记. 时间：%s . 考勤类型：%s . 考勤状态：%s ." % (now_str, "下班", "有点早"), 1)
            except:
                print "Error: Write checkin record to DB failed. sid = %s" % sid
                return ("好像发生了一些错误，请重试.", -1)
        else:
            rstate = checkin_state['ontime']  # ok
            try:
                db.add_checkin_record(sid = sid, rtype = rtype, rstate = rstate, rimage = image_path)
                return ("您已完成考勤登记. 时间：%s . 考勤类型：%s . 考勤状态：%s ." % (now_str, "下班", "正常"), 1)
            except:
                print "Error: Write checkin record to DB failed. sid = %s" % sid
                return ("好像发生了一些错误，请重试.", -1)
    else:
        return ("您今天已经完成了全部登记，不需要再次登记.", 0)


if __name__ == '__main__':
    print checkin("224", "aa")
