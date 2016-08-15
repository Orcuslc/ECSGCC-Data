import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from tools.modified_svm import *
from sklearn.ensemble import RandomForestClassifier
# from 'E:\\Chuan\\Documents\\libsvm-3.21\\python' import *

# We use the libsvm provided by http://www.csie.ntu.edu.tw/~cjlin/libsvm/ and the Python interface it provided within.

def read_data(data_path):
	data = pd.read_csv(data_path, encoding='gbk')
	time_list = data['time'].tolist()
	load_list = np.asarray(data['load'].tolist(), dtype = np.float)
	load_list = np.where(np.isnan(load_list), 0, load_list) # Convert all np.nan in load_list to 0
	return np.asarray([time_list, load_list])

def scale_data(data):
	time_list = data[0]
	load_list = np.asarray(data[1], dtype = np.float)
	normalized_load_list = load_list/load_list.max()
	return normalized_load_list

def handle_holiday(time_list):
	holiday = {'2015':['0101','0102','0103','0218','0219','0220','0221','0222','0223','0224','0225','0404','0501','0620','0903','0904','0905','0927','1001','1002','1003','1004','1005','1006','1007'],
		'2014':['0101','0131','0201','0202','0203','0204','0205','0206','0405','0501','0502','0503','0602','0908','1001','1002','1003','1004','1005','1006','1007'],
		'2013':['0101','0102','0103','0209','0210','0211','0212','0213','0214','0215','0404','0405','0429','0430','0501','0610','0611','0612','0919','0920','0921','1001','1002','1003','1004','1005','1006','1007'],
		'2012':['0101','0102','0103','0122','0123','0124','0125','0126','0127','0128','0402','0403','0404',],
		'2011':[],
		'2010':[],
		'2009':['0101','0102','0103','0125','0126','0127','0128','0129','0130','0131','0404','0405','0406','0501','0502','0503','0528','0529','0530','1001','1002','1003','1004','1005','1006','1007','1008']}
	not_weekend = {'2009':['0104','0124','0201','0531','0927','1010']
		'2010':[]}





def set_attr(data):



if __name__ == '__main__':
	data_path = 'E:\\Desktop\\ECSGCC\\data\\load.csv'
	data = read_data(data_path)
