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

X, y = readSamples("trainset4.mat")
X = norm(X)
struc = [(25,187),(13,26)]
nn_params = riw(struc)

krono = kronos.krono()
print 'learning...'
nn_params = train(X, y, struc, nn_params, 15)
print 'seg', krono.elapsed()

X, y = readSamples("testset.mat")
X = norm(X)
print
print 'testing train set...'
test_trainset(nn_params, X, y, struc)

print 'seg', krono.elapsed()