'''
Created on 29/05/2016

@author: botpi
'''
from apiDB import DB
from apiplots import *

db = DB("didi")
districts = db.escape_string("select district_id from districts order by district_id")
for district in districts:
    district_id = district["district_id"]
    rows = 
    d, s, g = getacum("diditest.gaps", district_id, "2016-01-22", db)
    