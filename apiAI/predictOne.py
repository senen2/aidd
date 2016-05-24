#andres botello
import numpy as np
from sigmoid import sigmoid

def predict(thetas, X, struc):
    layers = []
    t1 = 0
    t2 = 0
    local = {'h1': X,'t': 0.0}
    c = 1
    for i in range(0, len(struc)):
        m2 = struc[i][0]
        n2 = struc[i][1]
        t2 += m2 * n2
        layers.append({'layer': i,'theta': thetas[t1:t2].reshape(n2,m2).transpose()})
        t1 = t2
    
    for layer in layers:
        theta = layer['theta']
        local['h'+ str(c+1)] = sigmoid((np.hstack((1, local['h'+ str(c)]))).dot(theta.conj().transpose()))
        c += 1
        
    p = local['h'+ str(c)].argmax()
    return p
