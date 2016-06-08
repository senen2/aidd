#andres botello
import numpy as np

def linearCostFunction(X,y,thetas):
    try:
        m,n = X.shape
        X = np.hstack((np.ones((m,1)),X))
    except:
        m = len(X)
        X = np.hstack((np.ones((m,1)), X.reshape(-1,1)))

    a = X.dot(thetas.conj().transpose())
    c = (a - y) ** 2
    j = (1.0 / (2.0 * m)) * c.sum()
    
    c = (a - y).dot(X)
    g = (1.0 / m) * c
    return (j, g)