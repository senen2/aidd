'''
Created on 21/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apiDB import *
from apididi import *
from modinputs import *
from apiML import *

test = "test"
dist = 4
dir = "mat/"
dbname = "didi" + test
file_mat = dir + "gap" + test + str(dist) + ".mat"
filter = "" # "and gap<=100"
# raw_input("inputs working " + dbname + " " + filter + ", press enter...")
print "ok"
db = DB(dbname)
max_traffic_levels = 4
max_poi_levels = 176
gap_bin_digits = 13
X = []
y = []
db.exe("truncate table sets")
# districts = db.exe("select district_id from districts order by district_id")
districts = [dist]
for district in districts:
    # district_id = district["district_id"]
    district_id = district
    # xpoi = poi(district_id, max_poi_levels, db)
    dates = db.exe("select date from gaps where district_id=%s group by date" % district_id)
    for dt in dates:
        date = dt["date"]
        slots = db.exe("select slot from gaps where district_id=%s and date='%s' %s group by slot" % (district_id, date, filter))
        for sl in slots:
            slot = sl["slot"] 
            x = [0] * 66
            x[district_id-1] = 1
            x1 = [0] * 144
            x1[slot-1] = 1
            x += x1
            x1 = [0] * 7
            x1[weekday(date)] = 1
            x += x1
            # x = [district_id, slot, weekday(date)]
#             x += weather(date, slot, db)
#             x += traffic(district_id, date, slot, max_traffic_levels, db)
#             x += xpoi
#             y = gap(district_id, date, slot, gap_bin_digits, db)
            X.append(x)
            y.append(gap(district_id, date, slot, gap_bin_digits, db))
            #db.exe("insert into sets (x, y) values ('%s', '%s')" % (x, y))
        #db.commit()

saveSamples(file_mat, np.array(X), np.array(y))

print "end"