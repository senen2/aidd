'''
Created on 26/05/2016

@author: botpi

plot weekday test/train 
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
date = "2016-01-26"
district_id = 51
x = formatplot("gap %s (%s) - district %s" % (date, weekday(date), district_id), ymax=1000)
#d, s, g = getdsg("results", district_id, date, db)
d, s, g = getdsg("diditest.gaps", district_id, date, db)
plt.plot(x, g, '-', label="test", color="red")
# plt.plot(x, s, '-*', label="supply", color="orange")
# plt.plot(x, g, '-+', label="22", color="black")
d, s, g = getdsg("results_full", district_id, date, db)
plt.plot(x, g, '--', label="results_test", color="green")

# d, s, g = getdsg("results_send", district_id, date, db)
# plt.plot(x, d, '+', label="results_send", color="red")

# date = "2016-01-05"
# d, s, g = getdsg("gaps", district_id, date, db)
# plt.plot(x, g, '-', label=date, color="black")

# date = "2016-01-12"
# d, s, g = getdsg("gaps", district_id, date, db)
# plt.plot(x, g, '-', label=date, color="orange")

date = "2016-01-12"
d, s, g = getdsg("gaps", district_id, date, db)
plt.plot(x, g, '-', label=date, color="cyan")

plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)
plt.show()



