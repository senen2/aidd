'''
Created on 23/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apiDB import *
from apiML import *
    
if __name__ == '__main__': 
    dbname = "didi"
    raw_input("working " + dbname + ", watiting...")
    print "ok"
    db = DB(dbname)
    dbmat("trainset4.mat", db)
    db.close()    
    print "end"