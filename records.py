#coding=utf-8
import dbhandler
import calendar

def staff_monthly_record(sid, year, month):
    db = dbhandler.DBHandler()
    num_days = calendar.monthrange(int(year), int(month))[1]
    time1 = "%s-%s-%d 00:00:00" % (year, month, 1)
    time2 = "%s-%s-%d 23:59:59" % (year, month, num_days)
    records = db.get_checkin_records(sid, time1, time2)
    onduty = [-1] * num_days
    offduty = [-1] * num_days
    for r in records:
        day = r['rtime'].day
        rtype = r['rtype']
        rstate = r['rstate']
        if rtype == 0:
            onduty[day - 1] = int(rstate)
        else:
            offduty[day - 1] = int(rstate)
    # Create string
    onduty_str = ""
    for n in onduty:
        onduty_str += str(n) + " "
    offduty_str = ""
    for n in offduty:
        offduty_str += str(n) + " "

    return (onduty_str[:-1], offduty_str[:-1])

if __name__ == "__main__":
    print staff_monthly_record("224", "2013", "3")
