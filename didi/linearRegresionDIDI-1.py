import sys
sys.path.insert(0, '../apiAI')
from apiML import *
from apididi import *
from apiplots import *
import matplotlib.pyplot as plt
import numpy as np
from randInitializeWeights import randInitializeWeights as riw
from predict import predict,predict_linear
from apiDB import DB

def acum_to_normal(pdc):
	pd = np.zeros(len(pdc))
	for i in xrange(1,len(pdc)):
		pd[i] = pdc[i] - pdc[i-1]
	return pd

# db = DB("diditest")
db = DB("didi")
expo = 4
inputs = expo
hiddens = 1
struc = [(hiddens,inputs + 1)]
md = 0
md_total = np.empty_like([])
mds = []
days = ["2016-01-22", "2016-01-24", "2016-01-26", "2016-01-28", "2016-01-30"]
for district_id in xrange(1,67):
	md_distri = np.empty_like([])
	ss = []
	# for date in days:
	for day in xrange(1,22):
		date = "2016-01-" + str(day)
		x = formatplot("friday %s - district %s" % (date, district_id), ymax=30000, ndiv=31)
		d, s, g = getacum("gaps", district_id, date, db)
		X = polynomio(x,expo)
		d_params = normalEquation(X,d)
		s_params = normalEquation(X,s)

		d, s, g = getdsg("gaps", district_id, date, db)
		pdc = predict_linear(d_params,X)
		psc = predict_linear(s_params,X)

		pd = acum_to_normal(pdc)
		ps = acum_to_normal(psc)

		nz = np.where(g > 0)
		ps = ps[nz]
		pd = pd[nz]
		g = g[nz]

		gp = pd - ps
		gp = np.ones(len(g))
		md_day = np.mean(np.abs(g-gp)/g)
		md_distri = np.hstack((md_distri,md_day))

		ss.append(np.abs(g-gp)/g)
		# print date, g
		# mean = np.mean( np.abs(g-gp)/g )
  #       md += mean
	# mds.append(np.mean(ss))
	mean = np.mean(md_distri)
	md_total = np.hstack((md_total,mean))
# print "Didi Score:", md/(21*66)
# md_total = np.mean(mean)
mean2 = np.mean(np.array(mds))
print "Didi Score:", np.mean(mean) ,mean2