'''
Created on 06/06/2016

@author: botpi
'''
from result9 import *
from apiDB import DB
from apididi import test_table
from modresult import *
import result9

if __name__ == '__main__':
	print "start"
	db = DB("didi")
	#results_name = "results_send" # para enviar
	results_name = "results_test" # para probar envio
	
	districts = db.exe("select district_id from districts where district_id=37 order by district_id")
	for district in districts:
		district_id = district["district_id"]

		days_before, cases, fungap, resuls_name_x, source_name = best_case(district_id, db)
		fungap = getattr(result9, fungap)	
		source = read_table(source_name, district_id, db)
		results = read_table(results_name, district_id, db)

		sieve_district(results, source, days_before, cases, fungap)
		update_table(district_id, results_name, results, db)
	
		print district_id, test_table_district(results_name, district_id, db)
		
	print "all", test_table(results_name, db)
	#save_send("results11.csv", db)
	
	db.close()
	print "end"