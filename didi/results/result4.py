'''
Created on 28/05/2016

@author: botpi
'''
from apiDB import DB
from apididi import *

def estimgap(d, dant, s, sant, gant):
    return gant

def estimate(row, pendmax, db):
    #print row["district_id"], row["date"], row["slot"]
    
    d = 0
    s = 0
    gap = 1
    yes = before(row["district_id"], row["date"], row["slot"], db)
    if yes:
        befyes = before(row["district_id"], row["date"], yes["slot"], db)
        d = yes["demand"]
        s = yes["supply"]
        gap = d - s
        gap = 1

        # if row["district_id"]==3 and row["date"]=="2016-01-30" and row["slot"]==45:
        #     pass
    
        if befyes:
            deltad = yes["demand"] - befyes["demand"]
            deltas = yes["supply"] - befyes["supply"]
            deltat = yes["slot"] - befyes["slot"]

            # if abs(deltad) > pendmax:
            #     deltad = pendmax * (1 if deltad > 0 else -1)
            # if abs(deltas) > pendmax:
            #     deltas = pendmax * (1 if deltas > 0 else -1)

            gapant = gap_ant(row["district_id"], date_est(row["date"]), row["slot"], db)

            if deltad >= 0 and deltas > 0 and deltad > deltas and gapant > 1:
                gap = 2 # deltad - deltas  #0.481637623397 para 2, #0.485373181143
            # elif deltad >= 0 and deltas < 0:
            #     gap = 2
            # elif deltad < 0:
            #     gap -= 1

            d = yes["demand"] + deltad/deltat
            s = yes["supply"] + deltas/deltat
            if s > d:
                s = d
    
    if gap <= 0:
        gap = 1
    
    return d, s, gap

def gap_ant(district_id, date, slot, db):
    rows = db.exe("select gap from gaps where district_id=%s and date='%s' and slot=%s" % (district_id, date, slot))
    if rows:
        return rows[0]["gap"]
    else:
        return 0

def date_est(date, step):
    day = int(date[-2:])
    dif = step
    if day == 30:
        dif = step + 7

    return date[:8] + ("00" + str(day - dif))[-2:]

def estimate1(row, db):
    gap = gap_ant(row["district_id"], date_est(row["date"], 7), row["slot"], db)
    if gap <= 4: # 0.457844459473 0.437450047806
        gap = 1
    elif gap <= 6: # 0.451467968091 0.4364174979
        gap = 2
    elif gap <= 8: # 0.44986992536 0.436415965746
        gap = 3
    elif gap <= 16: # 0.448481298235
        gap = 4
    elif gap <= 18: # 0.446967214012
        gap = 5
    elif gap <= 19: # 0.445931287763
        gap = 6
    elif gap <= 24: # 0.445230234779
        gap = 7
    elif gap <= 30: # 0.444519444561
        gap = 8
    elif gap <= 38: # 0.443807846376
        gap = 9
    elif gap <= 42: # 0.443181674059 
        gap = 10
    else:
        gap = 11 
    return gap

def update(table, db):
    rows = db.exe("select * from %s" % table)
    for row in rows:
        #d, s, gap = estimate(row, -0.5, db) # (-0.5, 0.53045)
        gap = estimate1(row, db)
        db.exe("update %s set gap=%s where district_id=%s and date='%s' and slot=%s"
                % (table, gap, row["district_id"], row["date"], row["slot"]) )


if __name__ == '__main__': 
    db = DB("didi")
    # row = db.exe("select * from gaps where district_id=%s and date='%s' and slot=%s" % (51, "2016-01-19", 47))[0]
    # print estimate(row, -0.5, db)
    update("results_test", db)
    print test("results_test", db) # 0.47167 es con 1, 0.471369268265 
    #save_send("results5.csv", db)
    #create_test(db)
    db.close()
    # print date_est("2016-01-24", 7)
    print "end" 
