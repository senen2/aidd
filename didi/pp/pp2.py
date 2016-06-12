'''
Created on 07/06/2016

@author: botpi

'''
import sys
sys.path.insert(0, '../apiAI')
sys.path.insert(0, '../')
from apiDB import DB
from apididi import create_test_full
from result9 import *

print "begin"
db = DB("didi")
#create_test_full(db)

districts = db.exe("select district_id from results_test group by district_id")
for district in districts:
	district_id = district["district_id"]
	real = read_table("diditest.gaps", district_id, db)
	source = read_table("results_test", district_id, db)

	rows = db.exe("select * from results_test where district_id=%s" % district_id)
	for row in rows:
		gap = read_gap_ant(real, row["date"], row["slot"])
		db.exe("update results_test set gap=%s where district_id=%s and date='%s' and slot='%s'"
						% (gap, district_id, row["date"], row["slot"]) )

print "all", test_table("results_test", db)

db.close()
print "end"