'''
Created on 06/06/2016

@author: botpi
'''
from apiDB import DB
from apididi import *
from utilsres import *
from multiprocessing import Pool

def testdist(table_results, table_test):
    i = 0
    s = 0
    for date in table_results:
        if date in table_test:
            slots = table_results[date]
            for slot in slots:
                if slot in table_test[date]:
                    g = table_test[date][slot]
                    if g:
                        s += abs(g - table_results[date][slot]) / g 
                        i +=1
    return s / i

def read_gap(table_source, date, slot):
    gap = 0
    if date in table_source:
        if slot in table_source[date]:
            gap = table_source[date][slot]
    return gap

def read_gap_prom(table_source, date, slot):
    sum = read_gap(table_source, date, slot)
    n = 1

    s = slot - 1
    if s > 0:
        sum += read_gap(table_source, date, s)
        n += 1

    s = slot + 1
    if s <= 144:
        sum += read_gap(table_source, date, s)
        n += 1

    return s / n
# 
def date_est(date, step):
    day = int(date[-2:])
    dif = step
    if day == 30:
        dif = step + 7

    return date[:8] + ("00" + str(day - dif))[-2:]

def estimate2(table_source, date, slot, case, days_before):
    gap = read_gap(table_source, date_est(date, days_before), slot)
    #gap = read_gap_prom(table_source, date_est(date, days_before), slot)
    if gap>14:
        pass
    
    for i in xrange(1,len(case)+2):
        if i == (len(case)+1):
            gap = i
        else:
            if gap <= case[i-1]:
                gap = i
                break
    return gap

def update2(table_results, table_source, days_before, case): # cambio
    for date in table_results:
        for slot in table_results[date]:
            table_results[date][slot] = estimate2(table_source, date, slot, case, days_before)

# def update_table(table, db):
#     rows = db.exe("select district_id, cases from districts")
#     for row in rows:
#         if row["cases"] == "[]":
#             db.exe("update %s set gap=1 where district_id=%s" % (table, district_id))
#             db.commit()
#         else:
#             cases = eval(row["cases"])
#             update2(table, row["district_id"], db, cases)

def list_cases(district, table_results, table_source, table_test, epo):
    district_id = district["district_id"]
    case = read_case(district_id)
    if case:
        best_score = read_score(district_id)
        best_case = list(case)
        l = read_l(district_id)
        for itera in xrange(0, epo): #255
            update2(table_results, table_source, district["days_before"], case)
            score = testdist(table_results, table_test)
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

def clean_case(district, table_results, table_source, table_test):
    district_id = district["district_id"]
    case = read_case(district_id)
    if case:
        best_score = read_score(district_id)
        best_case = list(case)
        count = 0
        for itera in xrange(0,len(case)): #255
            case.remove(case[count])
            update2(table_results, table_source, district["days_before"], case)
            score = testdist(table_results, table_test)
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
    dates = db.exe("select date from %s where district_id=%s group by date" % (table_name, district_id)) # update2
    for dt in dates:
        date = dt["date"]
        table[date] = {}
        slots = db.exe("select slot, gap from %s where district_id=%s and date='%s' order by slot" 
            % (table_name, district_id, date))
        for slot in slots:
            table[date][slot["slot"]] = {}
            table[date][slot["slot"]] = slot["gap"]
    return table

def train_district(district):
    coment = "con 1, days 14, prom"
    district_id = district["district_id"]
    db = DB("didi")
    table_results = read_table("results_test_roma", district_id, db)
    table_test = read_table("diditest.gaps", district_id, db)
    table_source = read_table("gaps", district_id, db)
    
    save_case(district_id, [1])
    save_l(district_id, 0)
    save_score(district_id, 1)
    print "train_district", district_id
    for n in xrange(0, 20):
        list_cases(district, table_results, table_source, table_test, 50)
        clean_case(district, table_results, table_source, table_test)

    score = testdist(table_results, table_test)# 0.47167 es con 1, 0.471369268265    
    cases = read_case(district_id)
    db.exe("insert into districts_score (district_id, score, cases, coment) values (%s, %s, '%s', '%s')"
            % (district_id, score, cases, coment))
    db.commit()
    print "#### Final score ####"
    print district_id, score

if __name__ == '__main__': 
    print "Running..."
    db = DB("didi")
    districts = db.exe("select district_id, 14 as days_before from districts order by district_id")

    for district in districts:
        train_district(district)
    #train_district(districts[52])

    # for district in districts:
    #     update2("results_send", "gaps", district["days_before"], case)

    # pool = Pool(processes=3)
    # pool.map(train_district, districts)
    
    db.close()
    print "end"    