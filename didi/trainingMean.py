import sys
sys.path.insert(0, '../apiAI')
from apiML import *
from randInitializeWeights import randInitializeWeights as riw
from normalization import normalization as norm
import matplotlib.pyplot as plt
import kronos

file_train = "trainset100.mat"
file_test = "testset.mat"
inputs = 186
hiddens = 1
epochs = 1
expo = 1
dist = 66
totalDist = 1

X, y = readSamples(file_train)
# districts = X[:,0]
# X = np.hstack((X[:,0:2],X[:,4:6]))
X = X[:,0:2]
# nz = np.where(districts == dist)
# X = X[nz]
# U = np.mean(X, axis=0)
# S = np.std(X, axis=0)
# X = (X - U)/S
y2 = bin_to_dec(y)
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
# X = X[:,0:2]
nz = np.where(districts == dist)
# X = X[nz]
# X = polynomio(X,expo)
# X = (X - U)/S
y = bin_to_dec(y)
y = y[nz]
# score = test_trainset4(y, y, struc,districts,totalDist)
plt.plot(y2, '-', label="train", color="red")
plt.plot(y, '-*', label="test", color="blue")
plt.legend(loc='upper right', shadow=True, fontsize='large', numpoints=1)
plt.show()
seg = krono.elapsed()
saveScore(file_train,file_test,inputs,hiddens,epochs,score,seg,struc,nn_params)
print 'seg', seg
print "Didi Score(fix):", score