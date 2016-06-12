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
date = "2016-01-11"
district_id = 2
x = formatplot("jam %s (%s) - district %s" % (date, weekday(date), district_id), ymax=1000)
colors = ["red", "blue", "magenta", "orange"]
for i in range(1,5):
    j = getjam(district_id, date, i, db)
    plt.plot(x, j, '-', label="level %s" % i, color=colors[i-1])

d, s, g = getdsg("diditest.gaps", district_id, date, db)
plt.plot(x, g, '+', label="test", color="black")

d, s, g = getdsg("results_full", district_id, date, db)
plt.plot(x, g, '--', label="results_test", color="green")

d, s, g = getdsg("gaps", district_id, date, db)
plt.plot(x, g, '-', label=date, color="cyan")

plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)
plt.show()



