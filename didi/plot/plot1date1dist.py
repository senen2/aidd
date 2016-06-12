'''
Created on 26/05/2016

@author: botpi

plot one district and one date

'''
import sys
sys.path.insert(0, '../apiAI')
sys.path.insert(0, '../')
from apididi import *
from apiplots import *
import matplotlib.pyplot as plt
import numpy as np
from apiDB import DB

db = DB("didi")
date = "2016-01-19"
district_id = 51
x = formatplot("%s - district %s" % (date, district_id))
#d, s, g = getdsg("select slot, gap, 0 as demand, 0 as supply from results where district_id=%s and date='%s' order by slot" % (i,date), db)
# d, s, g = getdsg("select slot, gap, demand, supply from gaps where district_id=%s and date='%s' order by slot"
# 					 % (district_id, date), db)
d, s, g = getdsg("gaps", district_id, date, db)

plt.plot(x, d, '-', label="demand", color="green")
plt.plot(x, s, '-', label="supply", color="blue")
plt.plot(x, g, '-', label="gap", color="red")

d, s, g = getdsg_round("gaps", district_id, date, 200, db)

plt.plot(x, d, '-', label="demand", color="green")
plt.plot(x, s, '--', label="supply", color="blue")
plt.plot(x, g, '-', label="gap", color="red")

plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)
plt.show()



