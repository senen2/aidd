'''
Created on 28/05/2016

@author: botpi
'''
from apiDB import DB

db = DB("didi")
rows = db.exe("select * from results_send")
for row in rows:
    if row["date"]=="2016-01-30":
        date = "2016-01-16"
    else:
        dt = row["date"].split("-")
        m = "00%s" % (int(dt[2]) - 7)
        date = "%s-%s-%s" % (dt[0], dt[1], m[-2:])  
    
    g = db.exe("select gap from gaps where district_id=%s and date='%s' and slot=%s"
               % (row["district_id"], date, row["slot"]) )


#     if row["date"]=="2016-01-30":
#         pass
#     print row
    
    gap = 1
    if g:
        if g[0]["gap"] > gap:
            gap = g[0]["gap"]
    
    db.exe("update results_send set gap=%s where district_id=%s and date='%s' and slot=%s"
            % (gap, row["district_id"], row["date"], row["slot"]) )
    db.commit()
    
print "end"    