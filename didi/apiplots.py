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
    return np.array([x for x in range(1,145)]) # x

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
    
def getdsg(table, district_id, date, db):
    return getdsgsql("select slot, gap, demand, supply from %s where district_id=%s and date='%s' order by slot"
                    % (table, district_id, date), db)
    
def getacum(table, district_id, date, db):
    return getacumsql("select slot, gap, demand, supply from %s where district_id=%s and date='%s' order by slot"
                        % (table, district_id, date), db)
    
def getdsgsql(sql, db):    
    rows = db.exe(sql)
    t = [r["slot"] for r in rows]
    g = [r["gap"] for r in rows]
    d = [r["demand"] for r in rows]
    s = [r["supply"] for r in rows]
    
    gz=[]
    dz=[]
    sz=[]
    for j in range(1,145):
        if j in t:
            gz.append(g[t.index(j)])
            dz.append(d[t.index(j)])
            sz.append(s[t.index(j)])
        else:
            gz.append(0)
            dz.append(0)
            sz.append(0)
    
    g = np.array(gz)
    d = np.array(dz)
    s = np.array(sz)
    
    return d, s, g
    
def getacumsql(sql, db):    
    rows = db.exe(sql)
    t = [r["slot"] for r in rows]
    d = [r["demand"] for r in rows]
    s = [r["supply"] for r in rows]
    g = [r["gap"] for r in rows]
    
    dz=[]
    sz=[]
    gz=[]
    for j in range(1,145):
        if j in t:
            dz.append(d[t.index(j)])
            sz.append(s[t.index(j)])
            gz.append(g[t.index(j)])
        else:
            dz.append(0)
            sz.append(0)
            gz.append(0)
        
    ds = 0
    ss = 0
    gs = 0
    for i in range(len(dz)):
        ds += dz[i]
        ss += sz[i]
        gs += gz[i]         

        dz[i] = ds
        sz[i] = ss
        gz[i] = gs         

    d = np.array(dz)
    s = np.array(sz)
    g = np.array(gz)
    
    return d, s, g


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
