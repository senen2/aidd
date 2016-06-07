'''
Created on 25/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../../apiAI')
sys.path.insert(0, '../ml')
sys.path.insert(0, '../')
from apiML import *
from apiplots import *
from apididi import *
from predict import predict
from randInitializeWeights import randInitializeWeights as riw
from modinputs import *
from apiDB import *

inputs = 3
hiddens = 25
epochs = 20
dbname = "didi"
bin_digits = 13
filter = ""

# inputs
db = DB(dbname)
districts = [1]
X = []
Y = []
D = []
for district_id in districts:
    dates = db.exe("select date from gaps where district_id=%s group by date" % district_id)
    for dt in dates:
        date = dt["date"]
        slots = db.exe("select slot from gaps where district_id=%s and date='%s' %s group by slot" % (district_id, date, filter))
        for sl in slots:
            slot = sl["slot"] 
            x = [district_id, slot, weekday(date)]
            y, d = demand(district_id, date, slot, bin_digits, db)
            X.append(x)
            Y.append(y)
            D.append(d)

# train
X = np.array(X)
y = np.array(Y)
struc = [(hiddens, inputs + 1), (13, hiddens + 1)]
nn_params = riw(struc)
nn_params = train(X, y, struc, nn_params, epochs)

# predict
X = np.array([[1, slot, 5] for slot in range(1, 145)])
p = predict(nn_params, X, struc)
p = bin_to_dec(p)
plotpred(p, "prueba", "", "")
plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)
plt.show()

