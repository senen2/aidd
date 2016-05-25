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
#X = norm(X)
struc = [(hiddens,inputs + 1),(13,hiddens + 1)]
nn_params = riw(struc)

krono = kronos.krono()
print 'learning...'
nn_params = train(X, y, struc, nn_params, epochs)
print 'seg', krono.elapsed()

print
print 'testing validation set...'
X, y = readSamples(file_test)
X = (X - U)/S
#X = norm(X)
score = test_trainset(nn_params, X, y, struc)
seg = krono.elapsed()
saveScore(file_train,file_test,inputs,hiddens,epochs,score,seg)
print 'seg', seg