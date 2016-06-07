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

def date_est(date):
    if date=="2016-01-22":
        return "2016-01-15"
    elif date=="2016-01-24":
        return "2016-01-17"
    elif date=="2016-01-26":
        return "2016-01-19"
    elif date=="2016-01-28":
        return "2016-01-21"
    elif date=="2016-01-30":
        return "2016-01-16"

def estimate1(row, db):
    gap = gap_ant(row["district_id"], date_est(row["date"]), row["slot"], db)
    if gap <= 6: # 0.457844459473
        gap = 1
    elif gap <= 8: # 0.451467968091
        gap = 2
    elif gap <= 12: # 0.44986992536
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
    elif gap <= 46: # 0.443243113357
        gap = 10
    else:
        gap = 11 
    return gap

def estimate2(row, db, case):
    gap = gap_ant(row["district_id"], date_est(row["date"]), row["slot"], db)
    for i in xrange(1,len(case)+2):
        if i == (len(case)+1):
            gap = i
        else:
            if gap <= case[i-1]:
                gap = i
                break

    return gap

def update(table, db):
    rows = db.exe("select * from %s" % table)
    for row in rows:
        #d, s, gap = estimate(row, -0.5, db) # (-0.5, 0.53045)
        gap = estimate1(row, db)
        db.exe("update %s set gap=%s where district_id=%s and date='%s' and slot=%s"
                % (table, gap, row["district_id"], row["date"], row["slot"]) )

def update2(table, district_id, db, case):
    rows = db.exe("select * from %s where district_id=%s" % (table, district_id))
    for row in rows:
        #d, s, gap = estimate(row, -0.5, db) # (-0.5, 0.53045)
        gap = estimate2(row, db, case)
        db.exe("update %s set gap=%s where district_id=%s and date='%s' and slot=%s"
                % (table, gap, row["district_id"], row["date"], row["slot"]) )

def update_table(table, db):
    rows = db.exe("select district_id, cases from districts")
    for row in rows:
        if row["cases"] == "[]":
            db.exe("update %s set gap=1 where district_id=%s" % (table, district_id))
        else:
            cases = eval(row["cases"])
            update2(table, row["district_id"], db, cases)

def save_case(data):
    with open("case.txt", "w") as f:
        c = 0
        for d in data:
            if c == len(data)-1:
                f.write(str(d))
            else:
                f.write(str(d)+",")
                c += 1
    f.close()

def read_case():
    f = open("case.txt", "rb")
    data = f.read().split(",")
    f.close()
    if data == ['']:
        return []
    else:
        return [int(x) for x in data]
    # data = f.read()
    # case = []
    # for d in data.split(","):
    #     case.append(int(d))
    # return  case

def save_score(score):
    f = open("score.txt", "w")
    score += 0.000000000001
    f.write(str(score))
    f.close()

def read_score():
    f = open("score.txt", "rb")
    data = f.read()
    f.close()
    return float(data)

def save_l(score):
    f = open("l.txt", "w")
    f.write(str(score))
    f.close()

def read_l():
    f = open("l.txt", "rb")
    data = f.read()
    f.close()
    return int(data)

def save_case2(data):
    with open("case2.txt", "w") as f:
        c = 0
        for d in data:
            if c == len(data)-1:
                f.write(str(d))
            else:
                f.write(str(d)+",")
                c += 1
    f.close()

def read_case2():
    f = open("case2.txt", "rb")
    data = f.read()
    case = []
    for d in data.split(","):
        case.append(int(d))
    f.close()
    return  case

def save_score2(score):
    f = open("score2.txt", "w")
    score += 0.000000000001
    f.write(str(score))
    f.close()

def read_score2():
    f = open("score2.txt", "rb")
    data = f.read()
    f.close()
    return float(data)

def list_cases(district_id, epo):
    case = read_case()
    if case:
        # best_score = 100
        best_score = read_score()
        # best_case = []
        best_case = list(case)
        # l = 0
        l = read_l()
        for iter in xrange(0, epo): #255
            update2("results_test_roma", district_id, db, case)
            score = testdist("results_test_roma", district_id, db)
            if score <= best_score:
                best_score = score
                save_score(best_score)
                best_case = list(case)
                save_case(best_case)
                case[len(case)-1] += 1
                l = 0
                save_l(l)
            elif l == 1:
                case[len(case)-1] += 1
            else:
                case[len(case)-1] -= 1
                case.append(case[len(case)-1]+1)
                l = 1
                save_l(l)
            # print best_case
            print iter+1, best_score, score, "cuantos if:", len(best_case)

def clean_case(district_id):
    case = read_case()
    if case:
        best_score = read_score()
        best_case = list(case)
        count = 0
        for iter in xrange(0,len(case)): #255
            case.remove(case[count])
            update2("results_test_roma", district_id, db, case)
            score = testdist("results_test_roma", district_id, db)
            if score <= best_score:
                best_score = score
                save_score(best_score)
                best_case = list(case)
                save_case(best_case)
            else:
                case = list(best_case)
                count += 1

            print iter+1, best_score, score, "cuantos if:", len(best_case)

if __name__ == '__main__': 
    db = DB("didi")
    district_id = 2
    # row = db.exe("select * from gaps where district_id=%s and date='%s' and slot=%s" % (51, "2016-01-19", 47))[0]
    # print estimate(row, -0.5, db)
    # update("results_send", db)
    # case = read_case()
    # update2("results_send", db, case)
    # update2("results_test_roma", db, case)
    
    districts = db.exe("select district_id from districts order by district_id")
    for dist in districts:
        save_case([1])
        save_l(0)
        save_score(1)
        district_id = dist["district_id"]
        for n in xrange(0, 20):
            list_cases(district_id, 50)
            clean_case(district_id)
        print
        score = testdist("results_test_roma", district_id, db) # 0.47167 es con 1, 0.471369268265
        cases = read_case()
        db.exe("update districts set score=%s, cases='%s', complex=%s where district_id=%s" 
            % (score, cases, len(cases), district_id))
        db.commit()
        print "#### Final score ####"
        print district_id, score

    # update_table("results_send", db)
    # print test("results_test_roma", db)    
    # save_send("results6.csv", db)

    #create_test(db)
    
    db.close()
    print "end"    