'''
Created on 14/04/2016
@author: Botpi
machine learning related functions
'''
import numpy as np
import scipy.io
import scipy.linalg as linalg
from predict import predict, predict_linear
from predictOne import predict as predictOne
from nnCostFunction import nnCostFunction
from linearCostFunction import linearCostFunction
#from scipy.optimize import minimize
import fmincg
import matplotlib.pyplot as plt
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
    rows = db.exe("select * from sets")
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

def test_trainset_3(nn_params, X, y, struc):    
    p = predict(nn_params, X, struc)
    s = bin_to_dec(p)
    g = bin_to_dec(y)
    accuracy = np.mean(np.around(np.double(s == g),2)) * 100
    print 'test 3 Accuracy: %f'% accuracy, "%\n"

def test_trainset(nn_params, X, y, struc):    
    p = predict(nn_params, X, struc)
    s = bin_to_dec(p)
    g = bin_to_dec(y)
    g = np.ma.array(g, mask=False)
    s = np.ma.array(s, mask=False)
    g = g * 1.0
    a = np.where(g == 0)
    # g[a] = 0.1e300
    g.mask[a] = True
    g = g.compressed()
    s.mask[a] = True
    s = s.compressed()
    r = np.mean(np.abs(g-s)/g)
    return r

def test_trainset1(nn_params, X, y, struc):    
    p = predict(nn_params, X, struc)
    s = bin_to_dec(p)
    g = bin_to_dec(y)
    nz = np.where(g>0)
    g = g[nz]
    s = s[nz]
    r = np.mean(np.abs(g-s)/g)
    return r

def test_trainset2(nn_params, X, y, struc, ig, ng):    
    P = predict(nn_params, X, struc)
    S = bin_to_dec(P)
    G = bin_to_dec(y)
    nz = np.where(G > 0)
    S = S[nz]
    G = G[nz]
    group = X[:, ig][nz]

    md = 0
    for i in range(1, ng + 1):
        d = np.where(group==i)
        g = G[d]
        s = S[d]
        mean = np.mean( np.abs(g-s)/g )
        md += mean
    return md/ng

def predict_results(nn_params, X, struc):
    p = predict(nn_params, X, struc)
    return bin_to_dec(p)

def test_one(nn_params, X, y, struc):    
    p = predictOne(nn_params, X, struc)
    accuracy = np.mean(np.double(p == y.argmax())) * 100
    print 'Training Set Accuracy: %f\n'% accuracy

def bin_to_dec(a):
    return a.dot(1 << np.arange(a.shape[-1] - 1, -1, -1))

def saveweights(nn_params, struc, IDnet):    
    w = ''.join(['%.10f,' % num for num in nn_params])[:-1] #Get rid of the last comma
    db = DB(name="nn")
    db.exe("insert into weights (IDnet, struct, weights) values (%s,'%s','%s')" % (IDnet, str(struc) , w))
    db.close()

def readweights(IDnet):
    db = DB(name="nn")
    rows = db.exe("select * from weights where IDnet=%s" % IDnet)
    if rows:
        ws = rows[0]['weights'].split(",")
        n = np.array(map(float, ws))
        struc = eval(rows[0]["struct"])
        return n, struc

def readweights_didi(IDnet):
    db = DB(name="didi")
    rows = db.exe("select struct, weights, score from score where id=%s" % IDnet)
    if rows:
        ws = rows[0]['weights'].split(",")
        n = np.array(map(float, ws))
        struc = eval(rows[0]["struct"])
        return n, struc, rows[0]["score"]

def saveScore(file_train, file_test, inputs, hiddens, epochs, score, seg, struc, weights):
    w = ''.join(['%.10f,' % num for num in weights])[:-1] #Get rid of the last comma
    db = DB("didi")
    db.exe("""INSERT INTO score (file_train, file_test, inputs, hiddens, epochs, score, seg, DATETIME, struct, weights) 
            VALUE ('%s', '%s', '%s', '%s', '%s', '%s', '%s', SYSDATE(), '%s', '%s')""" % 
            (file_train, file_test, inputs, hiddens, epochs, score, seg, struc, w))
    db.close()

def saveres(nn_params, X, struc, file_train):
    p = predict(nn_params, X, struc)
    S =  bin_to_dec(p)
    X, y = readSamples(file_train)
    db = DB("didi")
    for i in range(len(X)):
        rows = db.exe("select date from results0 where weekday(date)=%s limit 1" % X[i,1])
        db.exe("INSERT INTO results (district_id, date, slot, gap) VALUES ('%s', '%s', '%s', '%s')"
         % (X[i, 0], rows[0]["date"], X[i, 2], S[i] ))
    db.close()


def randInitializeWeights(struc):
    epsilon_init = 0.12
    W = np.empty_like([])
    for i in struc:
        m2 = i[0]
        n2 = i[1]
        w = np.random.random((m2,n2)) * 2 * epsilon_init - epsilon_init
        W =  np.hstack((W.T.ravel(), w.T.ravel()))
    return W
def normalEquation(X, y):
    try:
        m,n = X.shape
        X = np.hstack((np.ones((m,1)),X))
    except:
        m = len(X)
        X = np.hstack((np.ones((m,1)), X.reshape(-1,1)))

    # X = np.hstack((np.ones((m,1)),X))
    xt = X.conj().transpose()
    pi = linalg.pinv(xt.dot(X))
    l = pi.dot(X.conj().transpose())
    w = l.dot(y)
    w = np.hstack(w.T.ravel())
    return w

def train_linear(X, y, nn_params, niters=50):
    f = lambda p: linearCostFunction(X, y, p)
    t, j, i = fmincg.minimize(f, nn_params, maxIter=niters, verbose=False)
    nn_params = t
    return nn_params

def polynomial(X, expo):
    try:
        m,n = X.shape
    except:
        X = X.reshape(-1,1)
    for i in xrange(1,expo + 1):
        if i == 1:
            x = X
        else:
            x = np.hstack((x, (X ** i)))
            # x = np.hstack((x, (X ** i), 2 * X))
            # x = np.hstack((x, (X ** i), 2 * X,X * X))
    return x    
