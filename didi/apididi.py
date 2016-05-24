'''
Created on 21/05/2016

@author: botpi
'''
from datetime import datetime

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