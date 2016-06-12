'''
Created on 07/06/2016

@author: botpi
'''
from result9 import *
from apiDB import DB
from modresult import *
import result9

if __name__ == '__main__':
    print "Running..."
    db = DB("didi")

    district_id = 39
#     days_before = 7
#     fungap = read_gap_prom
#     cases = [14, 18, 34, 38, 42, 46]
    #case = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 39, 74, 75, 81, 82, 100, 105, 108, 127, 128, 137, 164, 214, 219, 230, 235, 238, 254, 264, 294, 328, 333, 340, 342, 343, 408, 454, 516, 522, 527, 557, 564, 598, 612, 642, 653, 656, 669, 698, 702, 753, 757, 764, 831, 855, 876]    
    
    days_before, cases, fungap, results_name, source_name = best_case(district_id, db)
    fungap = getattr(result9, fungap)       

    results = read_table(results_name, district_id, db)
    source = read_table(source_name, district_id, db)
    real = read_table("diditest2.gaps", district_id, db)

    # memory test
    sieve_district(results, source, days_before, cases, fungap)
    score = test_district(results, real)
    print score

    # table test
    update_table(district_id, results_name, results, db)
    scoret = test_table_district(results_name, district_id, db)
    print scoret
    
    db.close()
    print "end"     