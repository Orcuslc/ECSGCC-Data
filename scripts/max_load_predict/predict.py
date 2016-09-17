from sklearn.svm import SVR
from matplotlib import pyplot as plt
import numpy as np

#############################################
#	Configurations							#
#############################################
C = 4
gamma = 2**-4
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

if __name__ == '__main__':
	test(730)