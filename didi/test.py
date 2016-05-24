'''
Created on 21/05/2016

@author: botpi
'''
from apididi import *

print "slot,day 1,1 ", slot_day("2016-01-05 00:05:11")
print "slot,day 1,5 ", slot_day("2016-01-16 00:00:40")
print "slot,day 144,5 ", slot_day("2016-01-09 23:55:17")

print "slot 90 ", slot("14:54:28")
print "slot 122 ", slot(" 20:17:44")
print "slot 144 ", slot("23:30:22")

print "day 1 ", weekday("2016-01-05")
print "day 5 ", weekday("2016-01-16")
print "day 5 ", weekday("2016-01-09")
