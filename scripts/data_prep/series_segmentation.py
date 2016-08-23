# from svmutil import *
import numpy as np
from sklearn.svm import SVR
from matplotlib import pyplot as plt
import numpy as np

# X : 2009-09-15 start
# We use data in the first 2 years to train, the others to test

def calc_err(pred, real):
	err = abs(np.asarray(pred)-np.asarray(real))/np.asarray(real)
	avgerr = np.average(err)
	maxerr = max(err)
	minerr = min(err)
	print((np.where(err>0.2)))
	print(avgerr, maxerr, minerr)
	return avgerr, maxerr, minerr

def test1(n):
	y1, x1 = y[:n], x[:n]
	y2, x2 = y[n:], x[n:]
	#clf = SVR(C = 2**12, gamma = 2**-4)
	#C_list = [2**i for i in range(1, 20)]
	C = 4
	#gamma = 2**-4
	gamma = 2**-4
	gamma_list = [2**(-i/1000) for i in range(4080, 4100)]
	clf = SVR(C = C, gamma = gamma)
	clf.fit(x1, y1)
	a = clf.predict(x2)
	calc_err(a, y2)
	#error_rate_list = []
	#for gamma in gamma_list:
	#	clf = SVR(C = C, gamma = gamma)
	#	clf.fit(x1, y1)
	#	a = clf.predict(x2)
	#	error, b, c = calc_err(a, y2)
	#	error_rate_list.append(error)
	#plt.plot([np.log2(i) for i in gamma_list], error_rate_list)
	#plt.show()

def test2():
	'''
	We assume that for each year, 10.1~3.31 belongs to winter model,
		4.1~9.30 belong to summer model'''
	winter_model_train_x = x[15:198]+x[380:542]
	winter_model_train_y = y[15:198]+y[380:542]
	summer_model_train_x = x[:15]+x[198:380]+x[542:745]
	summer_model_train_y = y[:15]+y[198:380]+y[542:745]
	winter_model = SVR()
	summer_model = SVR()
	winter_model.fit(winter_model_train_x, winter_model_train_y)
	summer_model.fit(summer_model_train_x, summer_model_train_y)
	winter_model_test_x = x[745:927]+x[1110:1292]+x[1475:1675]+x[1840:2022]
	winter_model_test_y = y[745:927]+y[1110:1292]+y[1475:1675]+y[1840:2022]
	summer_model_test_x = x[927:1110]+x[1292:1475]+x[1675:1840]+x[2022:]
	summer_model_test_y = y[927:1110]+y[1292:1475]+y[1675:1840]+y[2022:]
	winter_pred = winter_model.predict(winter_model_test_x)
	calc_err(winter_pred, winter_model_test_y)
	summer_pred = summer_model.predict(summer_model_test_x)
	calc_err(summer_pred, summer_model_test_y)
	calc_err(list(winter_pred)+list(summer_pred), list(winter_model_test_y)+list(summer_model_test_y))

def test3():
	'''
	We assume that for each year, 7.1~9.30 belongs to summer model(model-1),
		12.1~2.28 belongs to winter model(model-3),
		the others, 3.1~6.30, 10.1~11.30 belongs to spring model(model-2)'''
	model_1_train_x = x[:15]+x[285:375]+x[645:745]+x[1015:1105]+x[1375:1465]
	model_1_train_y = y[:15]+y[285:375]+y[645:745]+y[1015:1105]+y[1375:1465]
	model_2_train_x = x[15:75]+x[165:285]+x[375:435]+x[525:645]+x[745:805]+x[895:1015]+x[1105:1165]+x[1255:1375]
	model_2_train_y = y[15:75]+y[165:285]+y[375:435]+y[525:645]+y[745:805]+y[895:1015]+y[1105:1165]+y[1255:1375]
	model_3_train_x = x[75:165]+x[435:525]+x[805:895]+x[1165:1255]
	model_3_train_y = y[75:165]+y[435:525]+y[805:895]+y[1165:1255]
	model_1, model_2, model_3 = SVR(), SVR(), SVR()
	model_1.fit(model_1_train_x, model_1_train_y)
	model_2.fit(model_2_train_x, model_2_train_y)
	model_3.fit(model_3_train_x, model_3_train_y)
	model_1_test_x = x[1735:1825]
	model_1_test_y = y[1735:1825]
	model_2_test_x = x[1465:1525]+x[1615:1735]+x[1825:1885]+x[1975:]
	model_2_test_y = y[1465:1525]+y[1615:1735]+y[1825:1885]+y[1975:]
	model_3_test_x = x[1525:1615]+x[1885:1975]
	model_3_test_y = y[1525:1615]+y[1885:1975]
	model_1_pred, model_2_pred, model_3_pred = model_1.predict(model_1_test_x), model_2.predict(model_2_test_x), model_3.predict(model_3_test_x)
	calc_err(model_1_pred, model_1_test_y)
	calc_err(model_2_pred, model_2_test_y)
	calc_err(model_3_pred, model_3_test_y)
	calc_err(list(model_1_pred)+list(model_2_pred)+list(model_3_pred), model_1_test_y+model_2_test_y+model_3_test_y)

def test4():
	'''
	We assume that for each year, 7.1~9.30 belongs to summer model(model-1),
		12.1~2.28 belongs to winter model(model-3),
		the others, 3.1~6.30, 10.1~11.30 belongs to spring model(model-2)'''
	model_1_train_x = x[:15]+x[285:375]+x[645:745]+x[1015:1105]+x[1375:1465]
	model_1_train_y = y[:15]+y[285:375]+y[645:745]+y[1015:1105]+y[1375:1465]
	model_2_train_x = x[15:75]+x[375:435]+x[745:805]+x[1105:1165]
	model_2_train_y = y[15:75]+y[375:435]+y[745:805]+y[1105:1165]
	model_3_train_x = x[75:165]+x[435:525]+x[805:895]+x[1165:1255]
	model_3_train_y = y[75:165]+y[435:525]+y[805:895]+y[1165:1255]
	model_4_train_x = x[165:285]+x[525:645]+x[895:1015]+x[1255:1375]
	model_4_train_y = y[165:285]+y[525:645]+y[895:1015]+y[1255:1375]
	model_1, model_2, model_3, model_4 = SVR(), SVR(), SVR(), SVR()
	model_1.fit(model_1_train_x, model_1_train_y)
	model_2.fit(model_2_train_x, model_2_train_y)
	model_3.fit(model_3_train_x, model_3_train_y)
	model_4.fit(model_4_train_x, model_4_train_y)
	model_1_test_x = x[1735:1825]
	model_1_test_y = y[1735:1825]
	model_2_test_x = x[1465:1525]+x[1825:1885]
	model_2_test_y = y[1465:1525]+y[1825:1885]
	model_3_test_x = x[1525:1615]+x[1885:1975]
	model_3_test_y = y[1525:1615]+y[1885:1975]
	model_4_test_x = x[1615:1735]+x[1975:]
	model_4_test_y = y[1615:1735]+y[1975:]
	model_1_pred, model_2_pred, model_3_pred, model_4_pred = model_1.predict(model_1_test_x), model_2.predict(model_2_test_x), model_3.predict(model_3_test_x), model_4.predict(model_4_test_x)
	calc_err(model_1_pred, model_1_test_y)
	calc_err(model_2_pred, model_2_test_y)
	calc_err(model_3_pred, model_3_test_y)
	calc_err(model_4_pred, model_4_test_y)
	calc_err(list(model_1_pred)+list(model_2_pred)+list(model_3_pred)+list(model_4_pred), model_1_test_y+model_2_test_y+model_3_test_y+model_4_test_y)


if __name__ == '__main__':


	attr_path = '/media/Library/Chuan/Documents/GitHub/ECSGCC-data/Load-Data/attr-1.txt'
	model_path = '/media/Library/Chuan/Documents/GitHub/ECSGCC-data/Load-Data/segment_model.txt'
	with open(attr_path) as f:
		data = f.read().split('\n')
	for index in range(len(data)):
		data[index] = data[index].split(' ')[:-1]
	data = data[:-1]

	global x, y
	y = [float(record[0]) for record in data]
	str2float = lambda alist: [float(i) for i in alist]
	x = [str2float(record[1:]) for record in data]

	n = 730
	#test1(n)
	test2()
	#test1(n)
	#test3()
	#test4()


	#prob = svm_problem(y, x, isKernel=True)
	#param = svm_parameter('-s 4 -b 1')
	#m = svm_train(prob, param)
	#svm_save_model(model_path, m)
	#p_labels, p_acc, p_vals = svm_predict(y, x, m)