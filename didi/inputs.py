'''
Created on 21/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apiDB import *
from apididi import *
from apiML import *
import numpy as np

def weather(date, slot, db):
    rows = db.exe("select weather, temperature, pm25 from weather where date='%s' and slot=%s" % (date, slot))
    if rows:
        row = rows[0]
        return [row["weather"], row["temperature"], row["pm25"]]
    else:
        return [0, 0, 0]        

def traffic(district_id, date, slot, max_levels, db):
    rows = db.exe("""
        SELECT count 
        FROM traffic_det 
        INNER JOIN traffic ON traffic.id = traffic_det.traffic_id
        LEFT JOIN traffic_levels ON traffic_levels.level = traffic_det.level
        WHERE district_id=%s AND DATE='%s' AND slot=%s
        order by traffic_det.level
        """ % (district_id, date, slot))
#     db.exe("create temporary table x2 SELECT x1.count FROM traffic_levels LEFT JOIN x1 ON x1.level = traffic_levels.level")
#     db.exe("update x2 set count=0 where count is null")
#     rows = db.exe("select count from x2")
#     db.exe("drop table x1,x2")

    if rows and len(rows)==4:
        return [x["count"] for x in rows ]
    else:
        if len(rows)!=4:
            print "traffic levels different of 4 in district_id=%s, date=%s, slot=%s" % (district_id, date, slot)
    
        return [0 for i in xrange(max_levels)]    

def poi(district_id, max_levels, db):
    db.exe("create temporary table x1 select level, count from poi where district_id=%s" % district_id)
    db.exe("create temporary table x2 SELECT x1.count, mean, desv FROM poi_levels LEFT JOIN x1 ON x1.level = poi_levels.level")
    db.exe("update x2 set count=0 where count is null")
    #db.exe("update x2 set count=round((count-mean)/desv,0)")
    rows = db.exe("select count from x2")
    db.exe("drop table x1,x2")

    if rows:
        return [x["count"] for x in rows ]
    else:
        return [0 for i in xrange(max_levels)]        
    
def gap(district_id, date, slot, bin_digits, db):
    rows = db.exe("select demand-supply as gap from gaps where district_id=%s and date='%s' and slot=%s" % (district_id, date, slot))
    if rows:
        s = np.binary_repr(int(rows[0]["gap"]), width=bin_digits)
#         s = s[-bin_digits:]
        return [int(x) for x in s]
    else:
        return [0 for i in xrange(bin_digits)]       


if __name__ == '__main__':
    dbname = "didi"
    tbsets = "sets4"
    raw_input("working " + dbname + ", " + tbsets + " watiting...")
    print "ok"
    db = DB(dbname)
    max_traffic_levels = 4
    max_poi_levels = 176
    gap_bin_digits = 13
    db.exe("truncate table " + tbsets)
    districts = db.exe("select district_id from districts order by district_id")
    for district in districts:
        district_id = district["district_id"]
        xpoi = poi(district_id, max_poi_levels, db)
        dates = db.exe("select date from gaps where district_id=%s group by date" % district_id)
        for dt in dates:
            date = dt["date"]
            if date > '2016-01-04':
                slots = db.exe("select slot from gaps where district_id=%s and date='%s' group by slot" % (district_id, date))
                for sl in slots:
                    slot = sl["slot"] 
                    x = [district_id, slot, weekday(date)]
                    x += weather(date, slot, db)
                    x += traffic(district_id, date, slot, max_traffic_levels, db)
                    x += xpoi
                    y = gap(district_id, date, slot, gap_bin_digits, db)
                    db.exe("insert into sets4 (x, y) values ('%s', '%s')" % (x, y))
                db.commit()
                
    print "end"