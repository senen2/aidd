#andres botello
import numpy as np
from sigmoid import sigmoid

def predict(thetas, X, struc):
    layers = []
    t1 = 0
    t2 = 0
    for i in range(0, len(struc)):
        m2 = struc[i][0]
        n2 = struc[i][1]
        t2 += m2 * n2
        layers.append({'layer': i, 'theta': thetas[t1:t2].reshape(n2, m2).transpose()})
        t1 = t2
    
    local = {'h1': X, 't': 0.0}
    m, n = X.shape
    c = 1
    for layer in layers:
        theta = layer['theta']
        local['h'+ str(c+1)] = sigmoid((np.hstack((np.ones((m,1)), local['h'+ str(c)]))).dot(theta.conj().transpose()))
        c += 1
        
    return local['h'+ str(c)]

def predict_linear(thetas,X):
    try:
        m,n = X.shape
        X = np.hstack((np.ones((m,1)),X))
    except:
        m = len(X)
        X = np.hstack((np.ones((m,1)), X.reshape(-1,1)))
    return X.dot(thetas.conj().transpose())
