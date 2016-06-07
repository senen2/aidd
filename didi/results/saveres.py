'''
Created on 25/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apiML import *
from apiDB import *
from predict import predict

X, y = readSamples("trainset.mat")
u = np.mean(X, axis=0)
s = np.std(X, axis=0)

nn_params, struc, score0 = readweights_didi(49)
X, y = readSamples("testset.mat")
districts = X[:,0]
X = (X - u)/s
p = predict(nn_params, X, struc)
S = bin_to_dec(p)
G = bin_to_dec(y)

X, y = readSamples("testset.mat")
db = DB("didi")
db.exe("truncate table results")
for i in range(len(X)):
    rows = db.exe("select date from results0 where weekday(date)=%s limit 1" % int(X[i][2]))
    db.exe("INSERT INTO results (district_id, date, slot, gap, s, dif) VALUES ('%s', '%s', '%s', '%s', %s, %s)"
     % (int(X[i][0]), rows[0]["date"], int(X[i][1]), G[i], S[i], G[i]-S[i] ))
db.close()
print "end"


# score = test_trainset(nn_params, X, y, struc)
# score1 = test_trainset1(nn_params, X, y, struc)
# score2 = test_trainset2(nn_params, X, y, struc, districts, 66)
# print score0, score, score1, score2
# 106, 0.987581338286