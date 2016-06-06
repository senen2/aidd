'''
Created on 21/05/2016

@author: botpi
'''
from datetime import datetime
import numpy as np

def slot_day(time):
    dt = time.split()
    date = datetime.strptime(dt[0], "%Y-%m-%d")
    h = dt[1].split(":")
    return int( float(h[0])*6 + float(h[1])/10 + 1), date.weekday() #, dt[0] # 0 = monday

def slot(time):
    h = time.split(":")
    return int( float(h[0])*6 + float(h[1])/10 + 1)

def weekday(date):
    return datetime.strptime(date, "%Y-%m-%d").weekday() # 0 = monday

def test(table, db):
    db.exe("""
        CREATE temporary TABLE x2
        SELECT gaps.district_id, AVG(ABS(results.gap - gaps.gap) / gaps.gap) AS n, SUM(gaps.gap) AS gap, SUM(results.gap) AS s
        FROM %s as results
        INNER JOIN diditest.gaps AS gaps 
            ON gaps.district_id=results.district_id
            AND gaps.date=results.date
            AND gaps.slot=results.slot
        WHERE gaps.gap>0
        GROUP BY gaps.district_id
        """ % table)
    rows = db.exe("SELECT AVG(n) as a FROM x2")
    db.exe("drop table x2")
    return rows[0]["a"]

def testdist(table, district_id, db):
    rows = db.exe("""
        SELECT AVG(ABS(results.gap - gaps.gap) / gaps.gap) AS a
        FROM %s as results
        INNER JOIN diditest.gaps AS gaps 
            ON gaps.district_id=results.district_id
            AND gaps.date=results.date
            AND gaps.slot=results.slot
        WHERE gaps.gap>0 and results.district_id=%s
        """ % (table, district_id))
    return rows[0]["a"]

def before(district_id, date, slot, db):
    rows= db.exe("""
            select demand, supply, slot 
            from diditest.gaps 
            where district_id=%s and date='%s' and slot<%s 
            order by slot desc limit 1"""
            % (district_id, date, slot))
    if rows:
        return rows[0]
    else:
        None
        
def create_test(db):
    rows = db.exe("select * from results_send")
    db.exe("truncate table results_test")
    for row in rows:
        yes = before(row["district_id"], row["date"], row["slot"])
        if yes:
            db.exe("""
                insert into results_test (district_id, date, slot)
                values ('%s', '%s', '%s') 
            """ % (row["district_id"], row["date"], yes["slot"]))
            db.commit()

def save_send(filename, db):
    rows = db.exe("select * from results_send")
    f = open(filename, "w")
    for row in rows:
        f.write("%s,%s-%s,%s\n" % (row["district_id"], row["date"], row["slot"], row["gap"]))
    f.close()

# ---------------------------

    
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
            k = t.index(j)
            dz.append(d[k])
            sz.append(s[k])
            gz.append(g[k])
        else:
#             if j==1:
#                 dz.append(d[1])
#                 sz.append(s[1])
#                 gz.append(g[1])
#             elif j>len(d)-1:
#                 dz.append(d[-1])
#             elif j>len(s)-1:
#                 sz.append(s[-1])
#             elif j>len(g)-1:
#                 gz.append(g[-1])
#             else:
#                 dz.append(dz[-1])
#                 sz.append(sz[-1])
#                 gz.append(gz[-1])

            dz.append(0)
            sz.append(0)
            gz.append(0)
        
    ds = 0
    ss = 0
    gs = 0
    for i in range(len(dz)-1):
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
