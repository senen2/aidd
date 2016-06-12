'''
Created on 09/06/2016

@author: botpi

plot nexl slot 
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
date = "2016-01-12"
district_id = 27
d, s, g = getdsg("gaps", district_id, date, db)
x = np.copy(g)
x = np.delete(x, -1)
g = np.delete(g, 0)
plt.plot(x, g, '+', label="test", color="red")
#plt.plot(g, x, '+', label="test", color="blue")

plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)
plt.show()



