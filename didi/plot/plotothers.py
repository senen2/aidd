'''
Created on 01/06/2016

@author: botpi

plot weather,

'''
import sys
sys.path.insert(0, '../apiAI')
sys.path.insert(0, '../')
from apiDB import DB
from apiplots import *
import matplotlib.pyplot as plt
import numpy as np

def frequency(field, db):
	rows = db.exe("SELECT %s, COUNT(1) AS n FROM weather GROUP BY %s" % (field, field))
	x = np.array([r[field] for r in rows])
	y = np.array([r["n"] for r in rows])

	fig, ax = plt.subplots(1)
	ax.set_title("%s frequency" % field)
	ax.plot(x, y)
	plt.show()

if __name__ == '__main__': 
	db = DB("didi")
	frequency("weather", db)
	frequency("temperature", db)
	frequency("pm25", db)

	db.close()