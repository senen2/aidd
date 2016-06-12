'''
Created on 12/06/2016

@author: botpi

'''
import sys
sys.path.insert(0, '../apiAI')
sys.path.insert(0, '../')
from apiDB import DB
from apididi import create_test

print "begin"
db = DB("didi")
create_test(db)
db.close()
print "end"