'''
Created on 23/05/2016

@author: botpi
'''
from apiDB import *
from apiML import *
    
if __name__ == '__main__': 
    dbname = "diditest"
    raw_input("working for " + dbname + ", watiting...")
    print "ok"
    db = DB(dbname)
    dbmat("testset.mat", db)
    db.close()    
    print "end"