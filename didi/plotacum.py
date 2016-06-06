'''
Created on 26/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apiML import *
from apididi import *
from apiplots import *
import matplotlib.pyplot as plt
import numpy as np
from randInitializeWeights import randInitializeWeights as riw
from apiDB import DB

db = DB("didi")
date = "2016-01-22"
district_id = 1
x = formatplot("friday %s - district %s" % (date, district_id), ymax=30000, ndiv=31)

#d, s, g = getacum("results", district_id, "2016-01-01", db)
#d, s, g = getacum("diditest.gaps", district_id, "2016-01-01", db)
#plt.plot(x, d, '-', label="demand", color="red")

# plt.plot(x, s, '-*', label="supply", color="red")
# plt.plot(x, g, '-+', label="22", color="red")

d, s, g = getacum("diditest.gaps", district_id, "2016-01-22", db)
# plt.plot(x, d, '-', label="demand", color="black")
# plt.plot(x, s, '-', label="supply", color="black")
plt.plot(x, d, '-', label="03", color="black")

# X = np.asarray(x)
expo = 4
inputs = expo
hiddens = 1
struc = [(hiddens,inputs + 1)]
districts = 1
totalDist = 1
X = polynomio(x,expo)
# U = np.mean(X, axis=0)
# S = np.std(X, axis=0)
# X = (X - U)/S
nn_params = riw(struc)
nn_params = normalEquation(X,d)
# nn_params = train_linear(X, d, nn_params, 5000)
print nn_params
# nn_params[0] = 0
score = test_trainset4(nn_params, X, d, struc,districts,totalDist)
print "Didi Score(fix):", score

d, s, g = getacum("gaps", district_id, "2016-01-08", db)
plt.plot(x, d, '-', label="10", color="orange")

print nn_params
# nn_params[0] = 0
score = test_trainset4(nn_params, X, d, struc,districts,totalDist)
print "Didi Score(fix):", score

d, s, g = getacum("gaps", district_id, "2016-01-15", db)
plt.plot(x, d, '-', label="17", color="cyan")

plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)

plt.show()



