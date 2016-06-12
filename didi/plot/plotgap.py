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
date = "2016-01-24"
district_id = 28
x = formatplot("gap %s (%s) - district %s" % (date, weekday(date), district_id), ymax=1000)
#d, s, g = getdsg("results", district_id, date, db)
d, s, g = getdsg("diditest.gaps", district_id, date, db)
plt.plot(x, g, '+', label="test", color="red")
# plt.plot(x, s, '-*', label="supply", color="orange")
# plt.plot(x, g, '-+', label="22", color="black")
d, s, g = getdsg("results_send", district_id, date, db)
plt.plot(x, g, '-+', label="results_test", color="green")

# d, s, g = getdsg("results_send", district_id, date, db)
# plt.plot(x, d, '+', label="results_send", color="red")

# date = "2016-01-05"
# d, s, g = getdsg("gaps", district_id, date, db)
# plt.plot(x, g, '-', label=date, color="black")

# date = "2016-01-12"
# d, s, g = getdsg("gaps", district_id, date, db)
# plt.plot(x, g, '-', label=date, color="orange")

date = "2016-01-17"
d, s, g = getdsg("gaps", district_id, date, db)
plt.plot(x, g, '-', label="gap-source", color="cyan")
plt.plot(x, s, '-', label="supply-source", color="black")
plt.plot(x, d, '-', label="demand-source", color="orange")

# y = getsql("SELECT slot, supply FROM gaps WHERE district_id=%s AND DATE='%s' ORDER BY supply" % (district_id, date), "supply", db)
# plt.plot(x, y, '-', label="supply-ord-source", color="black")


# plot_constant(404, 144, '-', label="supply-limit-source", color="orange")
# plot_constant(665, 144, '-', label="supply-limit-source", color="orange")
plt.plot(x, np.array([404] * 144), '-', label="supply-limit-source", color="orange")
# plt.plot(x, np.array([227] * 144), '-', label="supply-limit-source", color="orange")


plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)
plt.show()



