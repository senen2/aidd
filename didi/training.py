'''
Created on 23/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apiML import *
from randInitializeWeights import randInitializeWeights as riw
from normalization import normalization as norm
from saveScore import saveScore
import kronos

file_train = "trainset100.mat"
file_test = "testset.mat"
inputs = 187
hiddens = 50
epochs = 20

X, y = readSamples(file_train)
X = norm(X)
struc = [(hiddens,inputs),(13,hiddens + 1)]
nn_params = riw(struc)

krono = kronos.krono()
print 'learning...'
nn_params = train(X, y, struc, nn_params, epochs)
print 'seg', krono.elapsed()

print
print 'testing validation set...'
X, y = readSamples(file_test)
X = norm(X)
score = test_trainset(nn_params, X, y, struc)
seg = krono.elapsed()
saveScore(file_train,file_test,inputs,hiddens,epochs,score,seg)
print 'seg', seg