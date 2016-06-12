'''
Created on 20/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
sys.path.insert(0, '../')
from apiDB import *
from apididi import *
import os

def districts(dr, db):
    db.exe("truncate table districts")
    rows = open(dr + "cluster_map/" + "cluster_map", "r").readlines()
    for row in rows:
        v = row.split("\t")
        db.exe("insert into districts (district_hash, district_id) values ('%s', '%s')" % (v[0], v[1]))

def orders(dr, db):
#     db.exe("lock tables orders write")
    db.exe("truncate table orders")
    names = [x for x in os.listdir(dr + "order_data/") if x[0]!="."]
#     names = [names[0], names[1]]
    for name in names:
        rows = open(dr + "order_data/" + name, "r").readlines()
#         rows = [rows[0], rows[1]]
        for row in rows:
            v = row.split("\t")
            dt = v[6].split()
            answer = 0 if v[1] == "NULL" else 1
            sl = slot(dt[1])
            district_id = db.exe("select district_id from districts where district_hash='%s'" % v[3])[0]["district_id"]
            db.exe("""
                insert into orders 
                (district_id, date, slot, answer) 
                values ('%s', '%s', '%s', '%s') 
                """ % (district_id, dt[0], sl, answer))
        db.commit()

def orders_full(dr, db):
    #db.exe("lock tables orders_fullxx write")
    db.exe("truncate table orders_fully")
    names = [x for x in os.listdir(dr + "order_data/") if x[0]!="."]
    # names = [names[0], names[1]]
    for name in names:
        # db.exe("truncate table orders_fully")
        rows = open(dr + "order_data/" + name, "r").readlines()
        # rows = [rows[0], rows[1]]
        for row in rows:
            v = row.split("\t")
            dt = v[6].split()
            answer = 0 if v[1] == "NULL" else 1
            sl = slot(dt[1])
            #district_id = db.exe("select district_id from districts where district_hash='%s'" % v[3])[0]["district_id"]
            db.exe("""
                insert into orders_fully
                (order_id, driver_id, passenger_id, start_district_hash, dest_district_hash, price, datetime, date, slot, answer) 
                values ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s','%s','%s') 
                """ % (v[0], v[1], v[2], v[3], v[4], v[5], v[6], dt[0], sl, answer))
        db.commit()
        db.exe("""
            INSERT INTO orders (order_id, district_id, dest_id, passenger_id, driver_id, DATETIME, DATE, slot, answer)
            SELECT orders_unique.id, districts.district_id,  destinations.id, passengers.id, drivers.id, orders_full.datetime, orders_full.date, orders_full.slot, orders_full.answer
            FROM orders_fully as orders_full
                INNER JOIN orders_unique ON orders_unique.hash=orders_full.order_id
                INNER JOIN passengers ON passengers.hash=orders_full.passenger_id
                INNER JOIN destinations ON destinations.hash=orders_full.dest_district_hash
                INNER JOIN districts ON districts.district_hash=orders_full.start_district_hash
                LEFT JOIN drivers ON drivers.hash=orders_full.driver_id
            """)
        print name
        
def gaps(db):
    db.exe("""
        insert into gaps (district_id, date, slot, demand, supply)
        select district_id, date, slot, sum(1) as demand, sum(answer) as supply
        from orders
        group by district_id, date, slot
        """)

def weather(dr, db):
    db.exe("lock tables weather write")
    db.exe("truncate table weather")
    names = [x for x in os.listdir(dr + "weather_data/") if x[0]!="."]
#     names = [names[0], names[1]]
    for name in names:
        rows = open(dr + "weather_data/" + name, "r").readlines()
#         rows = [rows[0], rows[1]]
        for row in rows:
            v = row.split("\t")
            slot, day = slot_day(v[0])
            db.exe("""
                insert into weather 
                (date, date_time, weather, temperature, pm25, slot, day) 
                values ('%s', '%s', '%s', '%s', '%s', %s, %s) 
                """ % (v[0], v[0], v[1], v[2], v[3], slot, day))
        db.commit()

def poilevels(db):
    db.exe("truncate table poi_levels")
    db.exe("insert into poi_levels (level) select level from poi group by level")    
    
def traffic(dr, db):
    db.exe("lock tables traffic write, traffic_det write, districts read")
    db.exe("truncate table traffic")
    db.exe("truncate table traffic_det")
    names = [x for x in os.listdir(dr + "traffic_data/") if x[0]!="."]
    names = [names[0], names[1]]
    for name in names:
        rows = open(dr + "traffic_data/" + name, "r").readlines()
        rows = [rows[0], rows[1]]
        for row in rows:
            v = row.split("\t")
            district_hash = v[0]
            time = v[len(v)-1]
            slot, day = slot_day(time)
            dt = time.split()
            district_id = db.exe("select district_id from districts where district_hash='%s'" % v[0])[0]["district_id"]
            db.exe("""
                insert into traffic 
                (district_id, date, slot, day) 
                values ('%s', '%s', '%s', '%s') 
                """ % (district_id, dt[0], slot, day))
            traffic_id = db.last_insert_id()
            v.remove(district_hash)
            v.remove(time)
            for w in v:
                z = w.split(":")                
                db.exe("""
                    insert into traffic_det
                    (traffic_id, level, count) 
                    values ('%s', '%s', '%s') 
                    """ % (traffic_id, z[0], z[1]))
        db.commit()
    

if __name__ == '__main__': 
    print "begin"
#     db = DB("didi")
    db = DB("diditest2")
    #dr = "C:/prog/didi/citydata/season_1/training_data/"
    dr = "C:/prog/didi/citydata2/season_2/test_set_2/"
    #districts(dr,db)
    #weather(dr,db)
    #traffic(dr,db)    
    #orders(dr, db)
    orders_full(dr, db)
    #gaps(db)
    #poilevels(db)
    db.exe("unlock tables")
    db.close()
    print "end"