'''
Created on 23/05/2016

@author: botpi
'''
import sys
sys.path.insert(0, '../apiAI')
from apiML import *
from randInitializeWeights import randInitializeWeights as riw
import kronos

dist = ""
dir = "mat/"
file_train = dir + "gap" + dist + ".mat"
file_test = dir + "gaptest" + dist + ".mat"
inputs = 217
hiddens = 15 # 1.621108
epochs = 60 # 1.490794

X, y = readSamples(file_train)
# u = np.mean(X, axis=0)
# s = np.std(X, axis=0)
# X = (X - u)/s

struc = [(hiddens, inputs + 1), (13, hiddens + 1)]
nn_params = riw(struc)

krono = kronos.krono()
print 'learning...'
nn_params = train(X, y, struc, nn_params, epochs)
print 'seg', krono.elapsed()

# saveweights(nn_params, struc, 8)

print
print 'testing validation set...'
X, y = readSamples(file_test)
# districts = X[:,0]
# X = (X - u)/s
#score = test_trainset(nn_params, X, y, struc)
score = test_trainset1(nn_params, X, y, struc)
# score2 = test_trainset2(nn_params, X, y, struc, 0, 66)

print 'Didi Score: %f\n' % score
seg = krono.elapsed()
# saveScore(file_train, file_test, inputs, hiddens, epochs, score, seg, struc, nn_params)
print 'seg', seg
