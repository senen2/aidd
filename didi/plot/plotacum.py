'''
Created on 26/05/2016

@author: botpi
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
district_id = 1
x = formatplot("friday %s - district %s" % ("2016-01-22", district_id), ymax=30000, ndiv=31)

#d, s, g = getacum("results", district_id, "2016-01-22", db)
d, s, g = getacum("diditest.gaps", district_id, "2016-01-22", db)
plt.plot(x, d, '-', label="22", color="red")
# plt.plot(x, s, '-*', label="supply", color="red")
# plt.plot(x, g, '-+', label="22", color="red")

d, s, g = getacum("gaps", district_id, "2016-01-01", db)
plt.plot(x, d, '-', label="01-demand", color="black")
plt.plot(x, s, '-', label="01-supply", color="black")
#plt.plot(x, g, '-', label="03", color="black")


d, s, g = getacum("gaps", district_id, "2016-01-08", db)
plt.plot(x, d, '-', label="10-demand", color="orange")
plt.plot(x, s, '-', label="10-supply", color="orange")

d, s, g = getacum("gaps", district_id, "2016-01-15", db)
plt.plot(x, d, '-', label="17-demand", color="cyan")
plt.plot(x, s, '-', label="17-supply", color="cyan")

d, s, g = getdsg("gaps", district_id, "2016-01-15", db)
plt.plot(x, d, '-', label="17-demand-real", color="magenta")


plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)

plt.show()



