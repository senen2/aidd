'''
Created on 06/06/2016

@author: botpi
'''
from result9 import update2, read_table, save_send
from apiDB import DB
from apididi import test_table
from modresult import *
import result9

if __name__ == '__main__':
	print "start"
	db = DB("didi")
	#table_results_name = "results_send" # para enviar
	#table_results_name = "results_test_roma" # para probar envio
	table_results_name = "results_full" # para probar envio
	
	districts = db.exe("select district_id from districts order by district_id")
	for district in districts:
		district_id = district["district_id"]
		table_source = read_table("gaps", district_id, db)
		table_send = read_table(table_results_name, district_id, db)

		days_before, cases, fungap, table_test_name = best_case(district_id, db)
		fungap = getattr(result9, fungap)	

		update2(table_send, table_source, days_before, cases, fungap)
		update_table(district_id, table_results_name, table_send, db)
	
		print district_id, test_table_district(table_results_name, district_id, db)
		
	print "all", test_table(table_results_name, db)
	#save_send("results9.csv", db)
	
	db.close()
	print "end"