'''
Created on 21/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apiDB import *
from apididi import *
from modinputs import *

dbname = "didi"
filter = "" # "and gap<=100"
raw_input("inputsres working " + dbname + " " + filter + ", press enter...")
print "ok"
db = DB(dbname)
max_traffic_levels = 4
max_poi_levels = 176
gap_bin_digits = 13
y = ("0 " * gap_bin_digits).split()
db.exe("truncate table sets")
districts = db.exe("select district_id from districts order by district_id")
for district in districts:
    district_id = district["district_id"]
    xpoi = poi(district_id, max_poi_levels, db)
    dates = db.exe("select date from results0 group by date")
    for dt in dates:
        date = dt["date"]
        slots = db.exe("select slot from results0 where date='%s'" % date)
        for sl in slots:
            slot = sl["slot"] 
            x = [district_id, slot, weekday(date)]
            x += weather_near(date, slot, db)
            x += traffic_near(district_id, date, slot, max_traffic_levels, db)
            x += xpoi
            y = gap(district_id, date, slot, gap_bin_digits, db)
            db.exe("insert into sets (x, y) values ('%s', '%s')" % (x, y))
        db.commit()
            
print "end"