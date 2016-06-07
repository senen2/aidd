'''
Created on 26/05/2016

@author: botpi

plot one week one district

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
color = ["green", "red", "blue", "cyan", "black", "orange", "magenta"]
dates = ["2016-01-11", "2016-01-12", "2016-01-13", "2016-01-14", "2016-01-15", "2016-01-16", "2016-01-17"]
days = ["mon", "tue",  "wed",  "thu",  "fri",  "sat",  "sun"]
x = formatplot("week %s / %s - district %s" % (dates[0], dates[6], district_id), ymax=400)
for i in range(7):
    date = dates[i]
    d, s, g = getdsg("gaps", district_id, date, db)

    plt.plot(x, g, '-', label=days[i], color=color[i])
    #plotdsg(d, s, g, "%s - %s - district %s" % (dates[0], dates[6], district_id), color[i], days[i])
    
# mng = plt.get_current_fig_manager()
# mng.resize( * mng.window.maxsize())
plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)
plt.show()



