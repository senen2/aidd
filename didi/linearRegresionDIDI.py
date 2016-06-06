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

		# probando con los test
		# mds_test = np.empty_like([])
		# for district_id_test in xrange(1,67):
		# 	ss_test = np.empty_like([])
		# 	for date_test in days_test:
		# 		x_test = formatplot("friday %s - district %s" % (date_test, district_id_test), ymax=30000, ndiv=31)
		# 		X_test = polynomial(x_test,expo)
		# 		d_test, s_test, g_test = getdsg("diditest.gaps", district_id_test, date_test, db)
		# 		pdc_test = predict_linear(d_params,X_test)
		# 		psc_test = predict_linear(s_params,X_test)

		# 		pd_test = acum_to_normal(pdc_test)
		# 		ps_test = acum_to_normal(psc_test)

		# 		nz_test = np.where(g_test > 0)
		# 		ps_test = ps_test[nz_test]
		# 		pd_test = pd_test[nz_test]
		# 		g_test = g_test[nz_test]

		# 		gp_test = pd_test - ps_test
		# 		gp_test = np.ones(len(g_test))

		# sigue con el mismo train
		# plt.plot(x, d, '-', label="demand acum")
		# plt.plot(x, s, '-', label="supply acum")
		plt.plot(g, '-', label="gap acum")

		d, s, g = getdsg("gaps", district_id, date, db)

		plt.plot(g, '-', label="gap real")

		pdc = predict_linear(d_params,X)
		psc = predict_linear(s_params,X)

		# plt.plot(x, pdc, '-', label="demand acum pronostic")
		# plt.plot(x, psc, '-', label="supply acum pronostic")

		pd = acum_to_normal(pdc)
		ps = acum_to_normal(psc)

		# plt.plot(x, d, '-', label="demand")
		# plt.plot(x, s, '-', label="supply")
		# plt.plot(x, pd, '-', label="demand pronostic")
		# plt.plot(x, ps, '-', label="supply pronostic")

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