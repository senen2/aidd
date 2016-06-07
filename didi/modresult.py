'''
Created on 07/06/2016

@author: botpi
'''
def update_table(district_id, table, memory, db):
    for date in memory:
        slots = memory[date]
        for slot in slots:
            db.exe("update %s set gap=%s where district_id=%s and date='%s' and slot=%s"
                % (table, memory[date][slot], district_id, date, slot))
        db.commit()

def best_cases(db):
    db.exe("""
            create temporary table x1
            SELECT district_id, MIN(score) AS score 
            FROM districts_score 
            GROUP BY district_id
            """)
    cases = db.exe("""
            SELECT DISTINCT districts_score.district_id, cases
            FROM districts_score
                INNER JOIN x1 
                    ON x1.district_id = districts_score.district_id
                    AND x1.score=districts_score.score
            """)
    db.exe("drop table x1")
    return cases

def test_table_district(table, district_id, db):
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

def best_case(district_id, db):
    best = db.exe("""
        select scenes.*, cases 
        from districts_score
            inner join scenes on scenes.id=districts_score.scene_id
        where district_id=%s order by score limit 1"""
         % district_id)[0]
         
    days_before = best["days_before"]
    cases = eval(best["cases"])
    fungap = best["fungap"]
    table_test_name = best["table_test"]
    return days_before, cases, fungap, table_test_name