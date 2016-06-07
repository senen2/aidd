'''
Created on 26/05/2016

@author: botpi

plot dsg on a date by several districts
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
date = "2016-01-08"
x = formatplot("date %s" % date)
district_id = 51
for i in range(51, 52):
    #d, s, g = getdsg("results", i,date, db)
    d, s, g = getdsg("gaps", i,date, db)

    plt.plot(x, d, '-', label="demand-%s" % i, color="green")
    plt.plot(x, s, '-', label="supply-%s" % i, color="blue")
    plt.plot(x, g, '-', label="gap-%s" % i, color="red")

plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)
plt.show()



