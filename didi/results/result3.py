'''
Created on 28/05/2016

@author: botpi
'''
from apiDB import DB
from apididi import *

def estimate(row, pendmax):
    #print row["district_id"], row["date"], row["slot"]
    
    d = 0
    s = 0
    yes = before(row["district_id"], row["date"], row["slot"])
    if yes:
        befyes = before(row["district_id"], row["date"], yes["slot"])
        
        # if row["district_id"]==3 and row["date"]=="2016-01-30" and row["slot"]==45:
        #     pass
        
        if befyes:
            deltad = yes["demand"] - befyes["demand"]
            deltas = yes["supply"] - befyes["supply"]
            deltat = yes["slot"] - befyes["slot"]

            if abs(deltad) > pendmax:
                deltad = pendmax * (1 if deltad > 0 else -1)
            if abs(deltas) > pendmax:
                deltas = pendmax * (1 if deltas > 0 else -1)

            d = yes["demand"] + deltad/deltat
            s = yes["supply"] + deltas/deltat
            if s > d:
                s = d
        else:
            d = yes["demand"]
            s = yes["supply"]
    
    gap = d - s
    if gap <= 0:
        gap = 1
    
    return d, s, gap

def update(table, db):
    rows = db.exe("select * from %s" % table)
    for row in rows:
        d, s, gap = estimate(row, -0.5) # (-0.5, 0.53045)
        db.exe("update %s set demand=%s, supply=%s, gap=%s where district_id=%s and date='%s' and slot=%s"
                % (table, d, s, gap, row["district_id"], row["date"], row["slot"]) )


if __name__ == '__main__': 
    db = DB("didi")
    #update("results_send", db)
    ###update("diditest.gaps", "s", db)
    #update("results_send", db)
    #print test("results_test", db)
    #save_send("results3.csv", db)
    #create_test(db)
    db.close()
    print "end"    