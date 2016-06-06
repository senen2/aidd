'''
Created on 26/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apididi import *
from apiplots import *
import matplotlib.pyplot as plt
import numpy as np
from apiDB import DB

db = DB("didi")
date = "2016-01-22"
district_id = 1
x = formatplot("friday %s - district %s" % (date, district_id))
#d, s, g = getdsg("select slot, gap, 0 as demand, 0 as supply from results where district_id=%s and date='%s' order by slot" % (i,date), db)
d, s, g = getdsg("select slot, gap, demand, supply from diditest.gaps where district_id=%s and date='%s' order by slot"
                  % (district_id, date), db)

plt.plot(x, d, '-', label="demand", color="red")
plt.plot(x, s, '-*', label="supply", color="red")
plt.plot(x, g, '-+', label="22", color="red")

date = "2016-01-01"
d, s, g = getdsg("select slot, gap, demand, supply from gaps where district_id=%s and date='%s' order by slot"
                  % (district_id, date), db)

# plt.plot(x, d, '-', label="demand", color="black")
# plt.plot(x, s, '-', label="supply", color="black")
plt.plot(x, g, '-', label="03", color="black")


date = "2016-01-08"
d, s, g = getdsg("select slot, gap, demand, supply from gaps where district_id=%s and date='%s' order by slot"
                  % (district_id, date), db)
plt.plot(x, g, '-', label="10", color="orange")


date = "2016-01-15"
d, s, g = getdsg("select slot, gap, demand, supply from gaps where district_id=%s and date='%s' order by slot"
                  % (district_id, date), db)
plt.plot(x, g, '-', label="17", color="cyan")

plt.legend(loc='upper right', shadow=True, fontsize='large', numpoints=1)

plt.show()



