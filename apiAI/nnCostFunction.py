#andres botello
import numpy as np
import sigmoid as s
import sigmoidGradient as sigg

def nnCostFunction(thetas, X, y, struc, lambd=1.0, bias=1):
    j = 0.0
    grad = {}
    grad_final = np.empty_like([]) 
    m,n = X.shape
    hidden = []
    t1 = 0
    t2 = 0
    
#     try:
#         my2, ny2 = y2.shape
#     except:
#         ny2 = 1
#     
#     if ny2 < 2:
#         y = np.zeros((len(y2),y2.max()+1))
#         for i in range(0,len(y2)):
#             for ii in range(0,len(y[i])):
#                 if y2[i] == ii:
#                     y[i][ii] = 1
#     else:
#         y = y2
        
    for i in range(0,len(struc)):
        m2 = struc[i][0]
        n2 = struc[i][1]
        t2 += m2 * n2
        hidden.append({'layer': i,'theta': thetas[t1:t2].reshape(n2,m2).transpose()})
        t1 = t2
    local = {'a1': X,'t': 0.0}
    c = 1
    last = ''
    if bias == 1:
        for layer in hidden:
            theta = layer['theta']
            local['Theta' + str(c)] = theta 
            local['theta' + str(c)] = theta.copy()
            local['theta' + str(c)][:,0] = 0.0
            local['t'] += (local['theta' + str(c)][:]**2).sum()
            local['a'+ str(c)] = np.hstack((np.ones((m,1)),local['a'+ str(c)]))
            c += 1
            local['z'+ str(c)] = local['a'+ str(c - 1)].dot(theta.conj().transpose())
            local['a'+ str(c)] = s.sigmoid(local['z'+ str(c)])
            last = 'a' + str(c)
            
        cost = y * np.log(local[last]) + (1 - y) * np.log(1 - local[last])
        r = (lambd / (2.0 * m)) * local['t']
        j = -(1.0 / m) * cost.sum() + r
        

        local['s' + str(c)] = local['a'+ str(c)] - y
        for i in range(1,(c-1)):
            local['s' + str(c-1)] = ((local['s' + str(c)]).dot(local['Theta' + str(c-1)][:,1:])) * sigg.sigmoidGradient(local['z'+ str(c-1)])
        for i in range(0,c-1):
            delta = (local['s' + str(c-i)].conj().transpose()).dot(local['a'+ str(c-(i+1))])
            r = (lambd / m) * local['theta' + str(c-(i+1))]
            grad['Theta' + str(c-(i+1))] = (1.0 / m) * delta + r
        for i in range(1,c):
            grad_final =  np.hstack((grad_final.T.ravel(), grad['Theta' + str(i)].T.ravel()))
    return (j, grad_final)