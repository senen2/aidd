'''
Created on 06/06/2016

@author: botpi
'''
from apiDB import DB
from apididi import *
from utilsres import *
from multiprocessing import Pool

def test_district(results, real):
    i = 0
    s = 0
    for date in results:
        if date in real:
            slots = results[date]
            for slot in slots:
                if slot in real[date]:
                    g = real[date][slot]
                    if g:
                        s += abs(g - results[date][slot]) / g 
                        i +=1
    return s / i

def read_gap(source, date, slot):
    gap = 0
    if date in source:
        if slot in source[date]:
            gap = source[date][slot]
    return gap

def read_gap_prom(source, date, slot):
    sum = read_gap(source, date, slot)
    n = 1

    s = slot - 1
    if s > 0:
        sum += read_gap(source, date, s)
        n += 1

    s = slot + 1
    if s <= 144:
        sum += read_gap(source, date, s)
        n += 1

    return s / n

def read_gap_ant(table, date, slot):
    gap = 0
    if date in table:
        if slot in table[date]:
            if slot-1 in table[date]:
                gap = table[date][slot-1]
            else:
                gap = 1
    return gap
 
def date_est(date, step):
    day = int(date[-2:])
    dif = step
    if day >= 30:
        dif = step + 7

    return date[:8] + ("00" + str(day - dif))[-2:]

def sieve_slot(source, date, slot, case, days_before, fungap):
    gap = fungap(source, date_est(date, days_before), slot)
    for i in xrange(1,len(case)+2):
        if i == (len(case)+1):
            gap = i
        else:
            if gap <= case[i-1]:
                gap = i
                break
    return gap

def sieve_district(results, source, days_before, sieves, fungap): # cambio
    for date in results:
        for slot in results[date]:
            results[date][slot] = sieve_slot(source, date, slot, sieves, days_before, fungap)

def list_cases(district_id, results, source, real, days_before, fungap, epo):
    case = read_case(district_id)
    if case:
        best_score = read_score(district_id)
        best_case = list(case)
        l = read_l(district_id)
        for itera in xrange(0, epo): #255
            sieve_district(results, source, days_before, case, fungap)
            score = test_district(results, real)
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
            # print itera+1, best_score, score, "cuantos if:", len(best_case)

def clean_case(district_id, results, source, real, days_before, fungap):
    case = read_case(district_id)
    if case:
        best_score = read_score(district_id)
        best_case = list(case)
        count = 0
        for itera in xrange(0,len(case)): #255
            case.remove(case[count])
            sieve_district(results, source, days_before, case, fungap)
            score = test_district(results, real)
            if score <= best_score:
                best_score = score
                save_score(district_id, best_score)
                best_case = list(case)
                save_case(district_id, best_case)
            else:
                case = list(best_case)
                count += 1

            # print itera+1, best_score, score, "cuantos if:", len(best_case)
    
def read_table(table_name, district_id, db): # nuevo cambio
    table = {}
    dates = db.exe("select date from %s where district_id=%s group by date" % (table_name, district_id)) # sieve_district
    for dt in dates:
        date = dt["date"]
        table[date] = {}
        slots = db.exe("select slot, gap from %s where district_id=%s and date='%s' order by slot" 
            % (table_name, district_id, date))
        for slot in slots:
            table[date][slot["slot"]] = slot["gap"]
    return table
    
def read_table_dsg(table_name, district_id, db): # nuevo cambio
    table = {}
    dates = db.exe("select date from %s where district_id=%s group by date" % (table_name, district_id)) # sieve_district
    for dt in dates:
        date = dt["date"]
        table[date] = {}
        slots = db.exe("select slot, demand, supply, gap from %s where district_id=%s and date='%s' order by slot" 
            % (table_name, district_id, date))
        for slot in slots:
            table[date][slot["slot"]] = {}
            table[date][slot["slot"]]["demand"] = slot["demand"]
            table[date][slot["slot"]]["supply"] = slot["supply"]
            table[date][slot["slot"]]["gap"] = slot["gap"]
    return table

def train_district(district_id, days_before, fungap, table_test_name, scene_id):
    db = DB("didi")
    results = read_table(table_test_name, district_id, db) # gaps to calculate
    real = read_table("diditest2.gaps", district_id, db) # real gaps
    source = read_table("diditest2.gaps", district_id, db) # gaps to sieve

    # algorithm
    # results -> look in source -> sieve with cases -> results
    #                                     ^
    #                                     !
    # test results with real -> modify cases
    
    save_case(district_id, [1])
    save_l(district_id, 0)
    save_score(district_id, 1)
    print "train_district", district_id
    for n in xrange(1, 21):
        list_cases(district_id, results, source, real, days_before, fungap, 50*n)
        clean_case(district_id, results, source, real, days_before, fungap)

    score = test_district(results, real)# 0.47167 es con 1, 0.471369268265    
    cases = read_case(district_id)
    db.exe("insert into districts_score (district_id, scene_id, score, cases) values (%s, %s, %s, '%s')"
            % (district_id, scene_id, score, cases))
    db.close()
    print "#### Scene final score ####"
    print district_id, scene_id, score

if __name__ == '__main__': 
    print "Running..."
    db = DB("didi")
    districts = db.exe("select district_id from districts order by district_id")
    scenes = db.exe("select * from scenes where active=1")

    for district in districts:
        for scene in scenes:
            train_district(district["district_id"], scene["days_before"], globals()[scene["fungap"]], scene["table_test"], scene["id"])
#             train_district(district["district_id"], 7, globals()['read_gap'], "results_test_roma_3", "prueba5")
    #train_district(districts[52])

    # for district in districts:
    #     sieve_district("results_send", "gaps", district["days_before"], case)

    # pool = Pool(processes=3)
    # pool.map(train_district, districts)
    
    db.close()
    print "end"    