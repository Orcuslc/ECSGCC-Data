from sklearn.svm import SVR
from matplotlib import pyplot as plt
from matplotlib import dates as mdt
import numpy as np
import datetime as dt

#############################################
#	Configurations							#
#############################################
C = 4
gamma = 2**-4
DAYS_BACK = 6
attr_path = '../../modified-data/attr.txt'
model_path = '../../modified-data/model.txt'
with open(attr_path) as f:
	data = f.read().split('\n')
for index in range(len(data)):
	data[index] = data[index].split(' ')[:-1]
data = data[:-1]

global x, y
y = [float(record[0]) for record in data]
str2float = lambda alist: [float(i) for i in alist]
x = [str2float(record[1:]) for record in data]

def calc_err(pred, real):
	err = abs(np.asarray(pred)-np.asarray(real))/np.asarray(real)
	avgerr = np.average(err)
	maxerr = max(err)
	minerr = min(err)
	print(len(list((np.where(err>0.2)))[0]))	
	print(len(list((np.where(err>0.1)))[0]))
	print(avgerr, maxerr, minerr)
	return avgerr, maxerr, minerr

def test(n):
	y1, x1 = y[:n], x[:n]
	y2, x2 = y[n:], x[n:]
	# y2, x2 = y1, x1
	print(len(y2))
	clf = SVR(C = C, gamma = gamma)
	#weight = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4] + [1, 1, 2]
	#weight = np.asarray(weight*n).reshape(n, 10)
	#weight = np.asarray([[(1/n)*(n-i)**2] for i in range(n)])
	#weight.shape = n, 
	#print(weight.shape)
	#clf.fit(x1, y1, sample_weight = weight)
	clf.fit(x1, y1)
	a = clf.predict(x2)
	calc_err(a, y2)

	org = dt.date(2011, 1, 1)
	td = dt.date(2011, 1, 2) - org
	begin = org + td*(n)
	date_list = [org+td*i for i in range(n+DAYS_BACK, 2032)]
	print(len(date_list))

	p1 = plt.subplot(211)
	line1, = p1.plot(date_list, y2, label = 'actual', color = 'r')
	line2, = p1.plot(date_list, a, label = 'simulation', color = 'b')
	p1.legend(handles = [line1, line2])

	p2 = plt.subplot(212)
	line3, = p2.plot(date_list, abs(y2-a)/y2, label = 'error', color = 'g')
	p2.legend(handles = [line3])
	p1.grid(True)
	p2.grid(True)
	plt.show()

def multi_step_predict(n, m = 2):
	x1, y1 = x[:n], y[:n]
	clf1 = SVR(C = C, gamma = gamma)
	clf1.fit(x1, y1)

	x2, y2 = x[n:n*m], y[n:n*m]
	y2_p = clf1.predict(x2)
	y[n:n*m] = y2_p

	for i in range(DAYS_BACK):
		# print(x[n:n*m])
		x[n:n*m][i] = y[n-i-1:(n*m)-i-1]

	x1, y1 = x[:n*m], y[:n*m]

	clf = SVR(C = C, gamma = gamma)
	clf.fit(x1, y1)

	x2, y2 = x[n*m:], y[n*m:]
	a = clf.predict(x2)
	calc_err(a, y2)

	org = dt.date(2011, 1, 1)
	td = dt.date(2011, 1, 2) - org
	begin = org + td*(n)
	date_list = [org+td*i for i in range(n+DAYS_BACK, 2032)]
	print(len(date_list))

	p1 = plt.subplot(211)
	line1, = p1.plot(date_list, y2, label = 'actual', color = 'r')
	line2, = p1.plot(date_list, a, label = 'simulation', color = 'b')
	p1.legend(handles = [line1, line2])

	p2 = plt.subplot(212)
	line3, = p2.plot(date_list, (y2-a)/y2, label = 'error', color = 'g')
	p2.legend(handles = [line3])
	p1.grid(True)
	p2.grid(True)
	plt.show()


if __name__ == '__main__':
	test(730)
	# multi_step_predict(365)