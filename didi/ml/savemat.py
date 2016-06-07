'''
Created on 23/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apiDB import *
from apiML import *
    
if __name__ == '__main__': 
    dbname = "diditest"
    # raw_input("savemat working " + dbname + ", press enter...")
    print "ok"
    db = DB(dbname)
    dbmat("gap.mat", db)
    db.close()    
    print "end"