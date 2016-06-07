'''
Created on 21/05/2016

@author: botpi
'''
import numpy as np
    
def weather(date, slot, db):
    rows = db.exe("select weather, temperature, pm25 from weather where date='%s' and slot=%s" % (date, slot))
    if rows:
        row = rows[0]
        return [row["weather"], row["temperature"], row["pm25"]]
    else:
        return [0, 0, 0]        

def weather_near(date, slot, db):
    slot = slot_near(date, slot, db)
    return weather(date, slot, db)

def traffic(district_id, date, slot, max_levels, db):
    rows = db.exe("""
        SELECT count 
        FROM traffic_det 
        INNER JOIN traffic ON traffic.id = traffic_det.traffic_id
        LEFT JOIN traffic_levels ON traffic_levels.level = traffic_det.level
        WHERE district_id=%s AND DATE='%s' AND slot=%s
        order by traffic_det.level
        """ % (district_id, date, slot))

    if rows and len(rows)==4:
        return [x["count"] for x in rows ]
    else:
        return [0 for i in xrange(max_levels)]    

def traffic_near(district_id, date, slot, max_levels, db):
    slot = slot_near(date, slot, db)
    return traffic(district_id, date, slot, max_levels, db)

def slot_near(date, slot, db):
    rows = db.exe("select slot from results0 where date='%s' and slot=%s" % (date, slot))
    if not rows:
        rows = db.exe("select slot from results0 where date='%s' and slot<%s order by slot desc limit 1" % (date, slot))
        if rows:
            slot = rows[0]["slot"]
        else:
            rows = db.exe("select slot from results0 where date='%s' and slot>%s order by slot limit 1" % (date, slot))
            if rows:
                slot = rows[0]["slot"]
    return slot

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
        return [int(x) for x in s]
    else:
        return [0 for i in xrange(bin_digits)]       
   
def demand(district_id, date, slot, bin_digits, db):
    rows = db.exe("select demand from gaps where district_id=%s and date='%s' and slot=%s" % (district_id, date, slot))
    if rows:
        s = np.binary_repr(int(rows[0]["demand"]), width=bin_digits)
        return [int(x) for x in s], rows[0]["demand"]
    else:
        return [0 for i in xrange(bin_digits)], 0       
