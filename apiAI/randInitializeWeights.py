import numpy as np

def randInitializeWeights(struc):
    epsilon_init = 0.12
    W = np.empty_like([])
    for i in struc:
        m2 = i[0]
        n2 = i[1]
        w = np.random.random((m2,n2)) * 2 * epsilon_init - epsilon_init
        W =  np.hstack((W.T.ravel(), w.T.ravel()))
    return W
