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
                return ("You have checked in successfully at %s. Type = %s, State = %s" % (now_str, "onduty", "ontime"), 1)
            except:
                print "Error: Write checkin record to DB failed. sid = %s" % sid
                return ("Some error, please try again", 0)
        else:
            rstate = checkin_state['late']  # be late
            try:
                db.add_checkin_record(sid = sid, rtype = rtype, rstate = rstate, rimage = image_path)
                return ("You have checked in successfully at %s. Type = %s, State = %s" % (now_str, "onduty", "late"), 1)
            except:
                print "Error: Write checkin record to DB failed. sid = %s" % sid
                return ("Some error, please try again", 0)
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
                return ("You have checked in successfully at %s. Type = %s, State = %s" % (now_str, "offduty", "too early"), 1)
            except:
                print "Error: Write checkin record to DB failed. sid = %s" % sid
                return ("Some error, please try again", 0)
        else:
            rstate = checkin_state['ontime']  # ok
            try:
                db.add_checkin_record(sid = sid, rtype = rtype, rstate = rstate, rimage = image_path)
                return ("You have checked in successfully at %s. Type = %s, State = %s" % (now_str, "offduty", "ok"), 1)
            except:
                print "Error: Write checkin record to DB failed. sid = %s" % sid
                return ("Some error, please try again", 0)
    else:
        return ("You have checked today, no more needed.", 0)


if __name__ == '__main__':
    print checkin("224", "aa")
