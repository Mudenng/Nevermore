import numpy
import dbhandler
import face_recognise

ratio = [2, 1.8, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.2]

# Manhattan Distance
def L1(v1,v2):
    return sum([abs(v1[i]-v2[i]) for i in range(len(v1))])

def update(sensitivity):
    db = dbhandler.DBHandler()
    staffs = db.look_table("staff")
    efaces = {}
    for staff in staffs:
        sid = staff["sid"]
        eface_str = staff["eigenface"]
        eigenface = [float(i) for i in eface_str.split(" ")]
        efaces[sid] = eigenface

    # Update all staffs' distance
    for sid in efaces:
        theface = efaces[sid]
        min = 10000000.0
        for other in efaces:
            if other != sid:
                dis = L1(theface, efaces[other])
                if dis < min:
                    min = dis
        try:
            db.update_distance(sid, min / ratio[sensitivity])
        except:
            print "Error: Write distance to DB failed. sid = %s" % sid
            return -1
    print "Updated staffs' distances."
    return 0
