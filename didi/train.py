'''
Created on 22/05/2016

@author: botpi
'''
from apiDB import *
from apididi import *
from apiML import *
from randInitializeWeights import randInitializeWeights as riw
import kronos

X, y = readSamples("trainset.mat")
struc = [(25,185),(8,26)]
nn_params = riw(struc) #init randhom thetas

krono = kronos.krono()
print 'learning...'
nn_params = train(X, y, struc, nn_params, 50)
print 'seg', krono.elapsed()

print
print 'testing train set...'
test_trainset(nn_params, X, y, struc)
#print 'testing validation set...'
#test_trainset(nn_params, Xv, yv, struc)

print 'seg', krono.elapsed()