'''
Created on 23/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apiML import *
from randInitializeWeights import randInitializeWeights as riw
from normalization import normalization as norm
import kronos

file_train = "trainset100.mat"
file_test = "testset.mat"
inputs = 186
hiddens = 25
epochs = 20

X, y = readSamples(file_train)
U = np.mean(X, axis=0)
S = np.std(X, axis=0)
X = (X - U)/S
struc = [(hiddens,inputs + 1),(13,hiddens + 1)]
nn_params = riw(struc)

krono = kronos.krono()
print 'learning...'
nn_params = train(X, y, struc, nn_params, epochs)
print 'seg', krono.elapsed()

print
print 'testing validation set...'
X, y = readSamples(file_test)
districts = X[:,0]
X = (X - U)/S
score1 = test_trainset(nn_params, X, y, struc)
score = test_trainset2(nn_params, X, y, struc,districts,66)
seg = krono.elapsed()
saveScore(file_train,file_test,inputs,hiddens,epochs,score,seg,struc,nn_params)
print 'seg', seg
print "Didi Score(old):", score1
print "Didi Score(fix):", score