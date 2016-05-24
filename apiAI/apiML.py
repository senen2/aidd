'''
Created on 14/04/2016
@author: Botpi
machine learning related functions
'''
import numpy as np
import scipy.io
from predict import predict
from predictOne import predict as predictOne
from nnCostFunction import nnCostFunction
#from scipy.optimize import minimize
import fmincg
from apiDB import DB

def readSamples(filename):
    data = scipy.io.loadmat(filename) 
    X = data['X']
    y = data['y']
    return (X, y)

def saveSamples(filename, X, y):
    data = {}
    data["X"] = X
    data["y"] = y
    scipy.io.savemat(filename, data)

def dbmat(filename, db):
    X = []
    Y = []
    rows = db.exe("select * from sets4")
    for row in rows:
        x = eval(row['x'])
        y = eval(row['y'])
        X.append(x)
        Y.append(y)        
    saveSamples(filename, np.array(X), np.array(Y))

def prepareLabels(y2):
    try:
        my2, ny2 = y2.shape
    except:
        ny2 = 1
    
    if ny2 < 2:
        y = np.zeros((len(y2), y2.max() + 1))
        for i in range(0, len(y2)):
            for ii in range(0, len(y[i])):
                if y2[i] == ii:
                    y[i][ii] = 1
    else:
        y = y2
    return y
        
def train(X, y, struc, nn_params, niters=50):
    f = lambda p: nnCostFunction(p, X, y, struc, lambd=1.0)
    t, j, i = fmincg.minimize(f, nn_params, maxIter=niters, verbose=False)
    nn_params = t
    return nn_params
# 
# def test_trainset_2(nn_params, X, y, struc):    
#     p = predict(nn_params, X, struc)
#     accuracy = np.mean(np.double(p == y)) * 100
#     print 'test 2 Accuracy: %f'% accuracy, "%\n"
# 
# def test_trainset_3(nn_params, X, y, struc):    
#     p = predict(nn_params, X, struc)
#     s = bin_to_dec(p)
#     g = bin_to_dec(y)
#     b = np.mean(np.double(p == y)) * 100
#     accuracy = np.mean(np.double(s == g)) * 100
#     print 'test 3 Accuracy: %f'% accuracy, "%\n"

def test_trainset(nn_params, X, y, struc):    
    p = predict(nn_params, X, struc)
    s = bin_to_dec(p)
    g = bin_to_dec(y)
    g = g * 1.0
    a = np.where(g == 0)
    g[a] = 0.1e300
    r = np.mean(np.abs(g-s)/g)
    print 'Didi Score: %f\n'% r

def test_one(nn_params, X, y, struc):    
    p = predictOne(nn_params, X, struc)
    accuracy = np.mean(np.double(p == y.argmax())) * 100
    print 'Training Set Accuracy: %f\n'% accuracy

def bin_to_dec(a):
    return a.dot(1 << np.arange(a.shape[-1] - 1, -1, -1))

def saveweights(nn_params, struc, IDnet):    
    w = ''.join(['%.10f,' % num for num in nn_params])[:-1] #Get rid of the last comma
    db = DB(name="nn")
    db.Exe("insert into weights (IDnet, struct, weights) values (%s,'%s','%s')" % (IDnet, str(struc) , w))
    db.close()

def readweights(IDnet):
    db = DB(name="nn")
    rows = db.Exe("select * from weights where IDnet=%s" % IDnet)
    if rows:
        ws = rows[0]['weights'].split(",")
        n = np.array(map(float, ws))
        struc = eval(rows[0]["struct"])
        return n, struc

def randInitializeWeights(struc):
    epsilon_init = 0.12
    W = np.empty_like([])
    for i in struc:
        m2 = i[0]
        n2 = i[1]
        w = np.random.random((m2,n2)) * 2 * epsilon_init - epsilon_init
        W =  np.hstack((W.T.ravel(), w.T.ravel()))
    return W