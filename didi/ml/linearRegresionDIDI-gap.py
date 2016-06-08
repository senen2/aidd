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
		pd[i-1] = pdc[i] - pdc[i-1]
	return pd

db = DB("didi")
expo = 4
inputs = expo
hiddens = 1
struc = [(hiddens,inputs + 1)]
mds = np.empty_like([])
days_test = ["2016-01-22", "2016-01-24", "2016-01-26", "2016-01-28", "2016-01-30"]
print "start"
for district_id in xrange(51,67):
	ss = np.empty_like([])
	for day in xrange(1,22):
		if day < 10:
			date = "2016-01-0" + str(day)
		else:
			date = "2016-01-" + str(day)
		x = formatplot("friday %s - district %s" % (date, district_id), ymax=30000, ndiv=31)
		d, s, g = getacum("gaps", district_id, date, db)
		X = polynomial(x,expo)
		d_params = normalEquation(X,d)
		s_params = normalEquation(X,s)
		g_params = normalEquation(X,g)

		# plt.plot(x, d, '-', label="demand acum")
		# plt.plot(x, s, '-', label="supply acum")
		plt.plot(x, g, '-', label="gap acum")

		d, s, g = getdsg("gaps", district_id, date, db)

		# plt.plot(d, '-', label="demand real")
		# plt.plot(s, '-', label="supply real")
		plt.plot(x, g, '-', label="gap real")

		pdc = predict_linear(d_params,X)
		psc = predict_linear(s_params,X)
		pgc = predict_linear(g_params,X)

		# plt.plot(x, pdc, '-', label="demand acum pronostic")
		# plt.plot(x, psc, '-', label="supply acum pronostic")
		plt.plot(x, pgc, '-', label="gap acum pronostic")

		pd = acum_to_normal(pdc)
		ps = acum_to_normal(psc)
		pg = acum_to_normal(pgc)
		
		# plt.plot(x, pd, '-', label="demand pronostic")
		# plt.plot(x, ps, '-', label="supply pronostic")
		plt.plot(x, pg, '-', label="gap pronostic")

		#trying
		gp = pd - ps
		plt.plot(x, pg, '--', label="gap (pd-ps) pronostic")

		plt.legend(loc='upper left', shadow=True, fontsize='large', numpoints=1)
		plt.show()

		nz = np.where(g > 0)
		ps = ps[nz]
		pd = pd[nz]
		g = g[nz]

		gp = pd - ps
		gp = np.around(gp)
		gp = np.abs(gp)
		# gp = np.ones(len(g))

		ss = np.hstack((ss.T.ravel(),(np.abs(g-gp)/g).T.ravel()))
	mds = np.hstack((mds.T.ravel(),(np.mean(ss)).T.ravel()))
mean2 = np.mean(np.array(mds))
print "Didi Score:", mean2