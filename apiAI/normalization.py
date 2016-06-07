import numpy as np

def normalization(X):
#     m,n = X.shape
#     U = np.ones((m,n))
#     S = np.ones((m,n))
    u = np.mean(X, axis=0)
#     U = U * u
    s = np.std(X, axis=0)
#     a = np.where( s == 0 )
#     s[a] = 0.1e300
#     S = S * s
    X = (X - u)/s
    return X
#     return np.nan_to_num(X)