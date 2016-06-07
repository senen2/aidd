'''
Created on 29/05/2016

@author: botpi
'''
import numpy as np
import scipy.linalg as linalg
from apiML import *

def randInitializeWeights(struc):
    epsilon_init = 0.12
    W = np.empty_like([])
    for i in struc:
        m2 = i[0]
        n2 = i[1]
        w = np.random.random((m2,n2)) * 2 * epsilon_init - epsilon_init
        W =  np.hstack((W.T.ravel(), w.T.ravel()))
    return W
    
def normalEquation(X,y):
    try:
        m,n = X.shape
    except:
        m = len(X)
    X = np.hstack((np.ones((m,1)),X))
    xt = X.conj().transpose()
    pi = linalg.pinv(xt.dot(X))
    l = pi.dot(X.conj().transpose())
    w = l.dot(y)
    w = np.hstack(w.T.ravel())
    return w

def polynomio(X,expo):
    for i in xrange(1,expo + 1):
        if i == 1:
            x = X
        else:
            # x = np.hstack((x, (X ** i)))
            x = np.hstack((x, (X ** i), 2 * X))
    return x

def predict_linear(thetas,X):
    m,n = X.shape
    X = np.hstack((np.ones((m,1)),X))
    return thetas * X

def test_trainset3(nn_params, X, y, struc, group, ng):   
    P = predict_linear(nn_params, X)
    S = bin_to_dec(P)
    G = y
#     plt.plot(S, '-', label="Pronosticated", color="red")
#     plt.plot(G, '-', label="real", color="blue")
#     plt.legend(loc='upper right', shadow=True, fontsize='large', numpoints=1)
#     plt.show()
    nz = np.where(G > 0)
    S = S[nz]
    G = G[nz]
    group = group[nz]

    md = 0
    for i in range(1, ng + 1):
        d = np.where(group==i)
        g = G[d]
        s = S[d]
        mean = np.mean( np.abs(g-s)/g )
        md += mean
    return md/ng

