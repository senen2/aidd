'''
Created on 31/05/2016
@author: Botpi

regression for all weekdays and ditricts
'''
import sys
sys.path.insert(0, '../apiAI')

from apiDB import DB
from apididi import *
from apiML import *

def regress(table, db):
	y = np.array(range(1,145))
	db.exe("truncate table %s" % table)
	districts = db.exe("select district_id from districts order by district_id")
	for dist in districts:
		district_id = dist["district_id"]
		#wdays = db.exe("select weekday(date) from gas group by weekday(date)")
		for wday in range(7):
			d, s, g = getdsgsql("""
					select slot, avg(demand) as demand, avg(supply) as supply, 0 as gap
					from gaps 
					where district_id=%s and weekday(date)=%s
					group by slot
					""" % (district_id, wday), db)

			dp = polynomial(d, 4)
			sp = polynomial(d, 4)

			dw = normalEquation(dp, y)
			sw = normalEquation(sp, y)
			
			dw = ''.join(['%.10f,' % num for num in dw])[:-1]
			sw = ''.join(['%.10f,' % num for num in sw])[:-1]
			db.exe("insert into %s (district_id, wday, dweights, sweights) values (%s, %s, '%s', '%s')"
							% (table, district_id, wday, dw, sw))


if __name__ == '__main__': 
    print "begin"
    db = DB("didi")
    regress("regreweek", db)
    db.close()
    print "end"