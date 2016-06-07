'''
Created on 03/06/2016

@author: botpi
'''
from apiDB import DB


if __name__ == '__main__':
    print "begin"
    db = DB("didi")

    db.close()
    print "end"