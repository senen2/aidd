'''
Created on 27/05/2016

@author: botpi
'''
import matplotlib.pyplot as plt
import numpy as np

def formatplot(tit, ymax=2000, ndiv=21):
    plt.xticks( np.linspace(0, 144, 37) )
    plt.yticks( np.linspace(0, ymax, ndiv) )
    plt.ylim((0, ymax))
    plt.xlabel('slot (time)')
    plt.ylabel('orders')
    plt.title(tit)    
    #plt.legend(loc=loc, shadow=True, fontsize='large', numpoints=1)
    return np.array(range(1,145)) # x

def plotdsg(d, p, g, tit, color, dlabel):
    x = formatplot(tit)
    
    if color=="":
        colord = "green"
        colors = "blue"
        colorg = "red"
    else:
        colord = color
        colors = color
        colorg = color        
    
    plt.plot(x, d, '-', label=dlabel, color=colord)
    #plt.plot(x, p, color=colors) #, '-', label='supply')
    #plt.plot(x, g, color=colorg) #, '-', label='gap')

def plotpred(p, tit, color, dlabel):
    x = np.array([x for x in range(1,145)])
    plt.xticks( np.linspace(0, 144, 37) )
    plt.yticks( np.linspace(0, 2000, 21) )
    plt.ylim((0,2000))
    
    if color=="":
        colorp = "red"
    else:
        colorp = color
    
    plt.plot(x, p, color=colorp) #, '-', label='supply')
    
    plt.xlabel('slot (time)')
    plt.ylabel('orders')
    plt.title(tit)    
    plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)

def plot_constant(constant, rep, symbol, label="constant", color="blak"):
    x = np.array(range(1, rep + 1))
    plt.plot(x, np.array([constant] * rep), '-', label=label, color=color)
