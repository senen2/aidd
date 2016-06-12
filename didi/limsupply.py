'''
Created on 08/06/2016

@author: botpi
'''
from apiDB import DB
from apididi import *
from result9 import *

def score_supply(table, limit):
    sum = 0
    i = 0
    for slot in table:
        demand = table[slot]["demand"]
        gap = table[slot]["gap"]
        if gap > 0:
            if demand > limit:
                s = demand - limit
            else:
                s = 1
            sum += abs(gap - s) / gap
            i += 1
    return sum / i

def train_date(list, score, limit, step):
    best_limit = limit
    best_score = score
    dir = 1
    while True:
        score = score_supply(list, limit)
        if score < best_score:
            best_score = score
            best_limit = limit
            dir = 1
        elif dir > 0:
            dir = -dir
        elif dir < 0:
            return best_limit, best_score
        limit += dir

def max_supply(table):
    mx = 0
    for slot in table:
        if mx < table[slot]["supply"]:
            mx = table[slot]["supply"]
    return mx

def train_district_supply(district_id, db):
    table_source = read_table_dsg("diditest.gaps", district_id, db)
    s=0
    i=0
    for date in table_source:
        mx = max_supply(table_source[date])
        limit, score = train_date(table_source[date], 100, mx*.7, 10)
        print district_id, date, weekday(date), limit, score
        s += score
        i += 1
    print "all", s/i

if __name__ == '__main__':
    print "start"
    db = DB("didi")
    districts = db.exe("select district_id from districts where district_id=51 order by district_id")
    for district in districts:
        train_district_supply(district["district_id"], db) 

    
    db.close()
    print "end"