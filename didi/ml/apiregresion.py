'''
Created on 27/05/2016

@author: botpi
'''
import numpy as np

def gradesc(X, y, theta, alpha, num_iters):
    m = len(y)    
    for i in xrange(num_iters):
        theta -= alpha/m * (X.dot(theta) - y).transpose()
    return theta
                            
def computeCost(X, y, theta):
    p = (X*theta - y)
    return np.sum(p*p) / 2 / len(y)
