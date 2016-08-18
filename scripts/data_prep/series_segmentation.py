import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
# from tools.modified_svm import *
# from sklearn.ensemble import RandomForestClassifier
from svmutil import *

# We use the libsvm provided by http://www.csie.ntu.edu.tw/~cjlin/libsvm/ and the Python interface it provided within.

# 2015: 0927 中秋未将0926计入
holiday = {
	'2016':['0101','0102','0103','0207','0208','0209','0210','0211','0212','0213','0402','0403','0404','0430','0501','0502','0609','0610','0611','0915','0916','0917','1001','1002','1003','1004','1005','1006','1007'],
	'2015':['0101','0102','0103','0218','0219','0220','0221','0222','0223','0224','0225','0404','0405','0406','0501','0502','0503','0620','0621','0622','0903','0904','0905','0927','1001','1002','1003','1004','1005','1006','1007'],
	'2014':['0101','0131','0201','0202','0203','0204','0205','0206','0405','0406','0407','0501','0502','0503','0531','0601','0602','0906','0907','0908','1001','1002','1003','1004','1005','1006','1007'],
	'2013':['0101','0102','0103','0209','0210','0211','0212','0213','0214','0215','0404','0405','0406','0429','0430','0501','0610','0611','0612','0919','0920','0921','1001','1002','1003','1004','1005','1006','1007'],
	'2012':['0101','0102','0103','0122','0123','0124','0125','0126','0127','0128','0402','0403','0404','0429','0430','0501','0622','0623','0624','0930','1001','1002','1003','1004','1005','1006','1007'],
	'2011':['0101','0102','0103','0202','0203','0204','0205','0206','0207','0208','0403','0404','0405','0430','0501','0502','0604','0605','0606','0910','0911','0912','1001','1002','1003','1004','1005','1006','1007'],
	'2010':['0101','0102','0103','0213','0214','0215','0216','0217','0218','0219','0403','0404','0405','0501','0502','0503','0614','0615','0616','0922','0923','0924','1001','1002','1003','1004','1005','1006','1007'],
	'2009':['0101','0102','0103','0125','0126','0127','0128','0129','0130','0131','0404','0405','0406','0501','0502','0503','0528','0529','0530','1001','1002','1003','1004','1005','1006','1007','1008']}
not_weekend = {
	'2009':['0104','0124','0201','0531','0927','1010'],
	'2010':['0220','0221','0612','0613','0919','0925','0926','1009'],
	'2011':['0130','0212','0402','1008','1009','1231'],
	'2012':['0121','0129','0331','0401','0428','0929'],
	'2013':['0105','0106','0216','0217','0407','0427','0428','0608','0609','0922','0929','1012'],
	'2014':['0126','0208','0504','0928','1011'],
	'2015':['0104','0215','0228','0906','0928','1010'],
	'2016':['0206','0214','0612','0918','1008','1009']
	}

def read_data(data_path):
	data = pd.read_csv(data_path, encoding='gbk')
	time_list = data['time'].tolist()
	load_list = np.asarray(data['load'].tolist(), dtype = np.float)
	load_list = np.where(np.isnan(load_list), 0, load_list) # Convert all np.nan in load_list to 0
	#return np.asarray([time_list, load_list])
	return np.asarray(list(zip(time_list, load_list)))

def scale_data(data):
	time_list = data[0]
	load_list = np.asarray(data[1], dtype = np.float)
	normalized_load_list = load_list/load_list.max()
	return normalized_load_list

def handle_holiday(rawdate, if_raw = True):
	if if_raw == True:
		year = int(rawdate[:4])
		month = int(rawdate[4:6])
		day = int(rawdate[6:])
		date = dt.date(year, month, day)
	else:
		date = rawdate
		rawdate = date.strftime('%Y%m%d')
	weekday = dt.date.isoweekday(date)
	if rawdate[4:] in holiday[rawdate[:4]]:
		is_holiday = 1
	else:
		is_holiday = 0
	if rawdate[4:] in not_weekend[rawdate[:4]]:
		weekend = 0
	else:
		if weekday in [6, 7]:
			weekend = 1
		else:
			weekend = 0
	return {'date':rawdate, 'holiday':is_holiday, 'weekend':weekend, 'weekday':weekday}

def get_calender_detail(start, end, if_raw = True):
	if if_raw == True:
		start = dt.date(int(start[:4]), int(start[4:6]), int(start[6:]))
		end = dt.date(int(end[:4]), int(end[4:6]), int(end[6:]))
	delta = (end - start).days
	date_list = [start+dt.timedelta(i) for i in range(delta+1)]
	detail = list(map(lambda x:handle_holiday(x, if_raw=False), date_list))
	date = pd.Series([item['date'] for item in detail], name = 'date')
	detail = [{'holiday':item['holiday'], 'weekend':item['weekend'], 'weekday':item['weekday']} for item in detail]
	df = pd.DataFrame(detail, index = date)
	# print(df)
	return df
 
def set_attr(data, calendar_path, attr_path):
	calendar = pd.read_csv(calendar_path, index_col = 'date')
	complete_data = []
	for index in range(7, len(data)):
		record = data.iloc[index]
		time = record['dates']
		load = record['max_load']
		cal_data = calendar.loc[int(time)]
		holiday = cal_data['holiday']
		weekend = cal_data['weekend']
		weekday = cal_data['weekday']
		ndays_back = 7
		past_load_data = []
		for i in range(1, 8):
			record = data.iloc[index - i]
			past_load_data.append(record['max_load'])
		complete_data.append((past_load_data[0], past_load_data[1], past_load_data[2], past_load_data[3], past_load_data[4], past_load_data[5], past_load_data[6], holiday, weekend, weekday))
	with open(attr_path, 'w') as f:
		for item in complete_data:
			string = ''
			for data in item:
				string = string + str(data) + '\t'
			f.write(string+'\n')
	f.close()


def handle_date_format(date):
	date = date.split('/')
	year = date[0]
	month = date[1]
	day = date[2]
	if len(month) == 1:
		month = '0' + month
	if len(day) == 1:
		day = '0' + day
	return year + month + day
		
def run(max_load_path, calendar_path, attr_path):
	data = pd.read_csv(max_load_path, encoding='gbk')
	dates = data['dates'].tolist()
	dates = list(map(handle_date_format, dates))
	data['dates'] = dates
	set_attr(data, calendar_path, attr_path)

if __name__ == '__main__':
	#date_path = '/media/Library/Chuan/Documents/GitHub/ECSGCC-data/Load-Data/calendar1.csv'
	#start = '20090101'
	#end = '20161231'
	#df = get_calender_detail(start, end)
	#df.to_csv(date_path)


	data_path = '/media/Library/Desktop/ECSGCC/data/load.csv'
	calendar_path = '/media/Library/Chuan/Documents/GitHub/ECSGCC-data/Load-Data/calendar.csv'
	max_load_path = '/media/Library/Chuan/Documents/GitHub/ECSGCC-data/Load-Data/date-max-load.csv'
	attr_path = '/media/Library/Chuan/Documents/GitHub/ECSGCC-data/Load-Data/attr.txt'
	run(max_load_path, calendar_path, attr_path)