import sys
sys.path.insert(0, '../apiAI')
from apiRL import *
#from apiML import *
from randInitializeWeights import randInitializeWeights as riw
from normalization import normalization as norm
import matplotlib.pyplot as plt
import kronos

file_train = "mat/" + "trainset100.mat"
file_test = "mat/" + "testset.mat"
inputs = 186
hiddens = 1
epochs = 1
expo = 1
dist = 66

# X = np.array([[1,2,3,4],[1,2,3,4]])
# y = np.array([1,2,3,4,5])
X, y = readSamples(file_train)
districts = X[:,0]
# X = np.hstack((X[:,0:2],X[:,4:6]))
X = X[:,0:2]
# nz = np.where(districts == dist)
# X = X[nz]
X = polynomio(X,expo)
U = np.mean(X, axis=0)
S = np.std(X, axis=0)
X = (X - U)/S
y = bin_to_dec(y)
# y = y[nz]
struc = [(hiddens,inputs + 1)]

krono = kronos.krono()
print 'learning...'
nn_params = normalEquation(X,y)
print 'seg', krono.elapsed()

print
print 'testing validation set...'
X, y = readSamples(file_test)
districts = X[:,0]
# X = np.hstack((X[:,0:2],X[:,4:6]))
X = X[:,0:2]
# nz = np.where(districts == dist)
# X = X[nz]
X = polynomio(X,expo)
X = (X - U)/S
y = bin_to_dec(y)
# y = y[nz]
score = test_trainset3(nn_params, X, y, struc,districts,dist)
seg = krono.elapsed()
saveScore(file_train,file_test,inputs,hiddens,epochs,score,seg,struc,nn_params)
print 'seg', seg
print "Didi Score(fix):", score