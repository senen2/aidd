'''
Created on 07/06/2016

@author: botpi

'''
from apiDB import DB
from apididi import create_test_full

print "begin"
db = DB("didi")
create_test_full(db)
db.close()
print "end"