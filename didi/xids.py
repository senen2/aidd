'''
Created on 20/05/2016

@author: botpi
'''
from apiDB import *

def orders_id(db):
    db.exe("lock tables orders write, districts read")
    db.exe("""
        update orders
            inner join districts on districts.district_hash = orders.start_district_hash
        set orders.district_id = districts.district_id
    """)

def traffic_id(db):
    db.exe("lock tables traffic write, districts read")
    db.exe("""
        update traffic
            inner join districts on districts.district_hash = traffic.district_hash
        set traffic.district_id = districts.district_id
    """)

def poi_id(db):
    db.exe("lock tables poi write, districts read")
    db.exe("""
        update poi
            inner join districts on districts.district_hash = poi.district_hash
        set poi.district_id = districts.district_id
    """)


if __name__ == '__main__': 
    db = DB("didi")
    #orders_id(db)
    #poi_id(db)
    traffic_id(db)
    db.exe("unlock tables")
    db.close()
    print "end"