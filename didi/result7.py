'''
Created on 28/05/2016

@author: botpi
'''
from apiDB import DB
from apididi import *
from utilsres import *
from multiprocessing import Pool


def gap_ant(district_id, date, slot, db):
    rows = db.exe("select gap from gaps where district_id=%s and date='%s' and slot=%s" % (district_id, date, slot))
    if rows:
        return rows[0]["gap"]
    else:
        return 0

def gap_ant_prom(district_id, date, slot, db):
    s = slot - 1
    if s <= 0:
        s=1

    rows = db.exe("select avg(gap) as gap from gaps where district_id=%s and date='%s' and slot>=%s order by slot limit 3"
                 % (district_id, date, s))
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

def estimate2(row, case, days_before, db):
    gap = gap_ant(row["district_id"], date_est(row["date"], days_before), row["slot"], db)
    # gap = gap_ant_prom(row["district_id"], date_est(row["date"], days_before), row["slot"], db)
    for i in xrange(1,len(case)+2):
        if i == (len(case)+1):
            gap = i
        else:
            if gap <= case[i-1]:
                gap = i
                break

    return gap

def update2(table, district, db, case):
    district_id = district["district_id"]
    rows = db.exe("select * from %s where district_id=%s" % (table, district_id))
    for row in rows:
        #d, s, gap = estimate(row, -0.5, db) # (-0.5, 0.53045)
        gap = estimate2(row, case, district["days_before"], db)
        db.exe("update %s set gap=%s where district_id=%s and date='%s' and slot=%s"
                % (table, gap, row["district_id"], row["date"], row["slot"]) )
        db.commit()

def update_table(table, db):
    rows = db.exe("select district_id, cases from districts")
    for row in rows:
        if row["cases"] == "[]":
            db.exe("update %s set gap=1 where district_id=%s" % (table, district_id))
            db.commit()
        else:
            cases = eval(row["cases"])
            update2(table, row["district_id"], db, cases)

def list_cases(district, epo, db):
    district_id = district["district_id"]
    case = read_case(district_id)
    if case:
        best_score = read_score(district_id)
        best_case = list(case)
        l = read_l(district_id)
        for iter in xrange(0, epo): #255
            update2("results_test_roma", district, db, case)
            score = testdist("results_test_roma", district_id, db)
            if score <= best_score:
                best_score = score
                save_score(district_id, best_score)
                best_case = list(case)
                save_case(district_id, best_case)
                case[len(case)-1] += 1
                l = 0
                save_l(district_id, l)
            elif l == 1:
                case[len(case)-1] += 1
            else:
                case[len(case)-1] -= 1
                case.append(case[len(case)-1]+1)
                l = 1
                save_l(district_id, l)
            # print best_case
            #print iter+1, best_score, score, "cuantos if:", len(best_case)

def clean_case(district, db):
    district_id = district["district_id"]
    case = read_case(district_id)
    if case:
        best_score = read_score(district_id)
        best_case = list(case)
        count = 0
        for iter in xrange(0,len(case)): #255
            case.remove(case[count])
            update2("results_test_roma", district, db, case)
            score = testdist("results_test_roma", district_id, db)
            if score <= best_score:
                best_score = score
                save_score(district_id, best_score)
                best_case = list(case)
                save_case(district_id, best_case)
            else:
                case = list(best_case)
                count += 1

            #print iter+1, best_score, score, "cuantos if:", len(best_case)
def train_district(district):
    district_id = district["district_id"]
    db = DB("didi")
    save_case(district_id, [1])
    save_l(district_id, 0)
    save_score(district_id, 1)
    print "train_district", district_id
    for n in xrange(0, 2):
        list_cases(district, 20, db)
        clean_case(district, db)
    print
    score = testdist("results_test_roma", district_id, db) # 0.47167 es con 1, 0.471369268265
    cases = read_case(district_id)
    db.exe("update districts set score=%s, cases='%s', complex=%s where district_id=%s" 
        % (score, cases, len(cases), district_id))
    db.commit()
    print "#### Final score ####"
    print district_id, score

if __name__ == '__main__': 
    db = DB("didi")
    district_id = 2
    # update("results_send", db)
    # case = read_case()
    # update2("results_send", db, case)
    # update2("results_test_roma", db, case)
    
    districts = db.exe("select district_id, 7 as days_before from districts order by district_id")
    # for i in xrange(0,len(districts)):
    #     districts[i]["db"] = DB("didi")
    pool = Pool(processes=12)
    print "Running..."
    # train_district(districts[0])
    pool.map(train_district, districts)
    
    
    # for district in districts:
    #     district_id = district["district_id"]
    #     save_case([1])
    #     save_l(0)
    #     save_score(1)
    #     for n in xrange(0, 5):
    #         list_cases(district, 20)
    #         clean_case(district)
    #     print
    #     score = testdist("results_test_roma", district_id, db) # 0.47167 es con 1, 0.471369268265
    #     cases = read_case()
    #     db.exe("update districts set score=%s, cases='%s', complex=%s where district_id=%s" 
    #         % (score, cases, len(cases), district_id))
    #     db.commit()
    #     print "#### Final score ####"
    #     print district_id, score

    # update_table("results_send", db)
    print test("results_test_roma", db)    
    # save_send("results7.csv", db)

    #create_test(db)
    
    db.close()
    print "end"    