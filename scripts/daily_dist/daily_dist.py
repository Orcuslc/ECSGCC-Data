import pandas as pd
import numpy as np
import datetime as dt
from matplotlib import pyplot as plt

load_data = '../../Load-Data/load_before_2013_clean.csv'
dist_path = '../../Load-Data/dist_before_2013.txt'
avg_path = '../../Load-Data/avg_before_2013.txt'
# Load data starts from 2009-09-11

def clean_data(load_data):
	data = pd.read_csv(load_data, encoding = 'gbk', index_col = 'time1')
	index = data.index.tolist()
	#index = [i if len(i) > 10 else i + ' 00:00:00' for i in index]
	def _handle(item):
		if len(item) <= 10:
			item = item + ' 00:00:00'
	#for item in index:
		plist = item.split(' ')
		date = plist[0].split('-')
		time = plist[1].split(':')
		if len(date[2]) == 1:
			date[2] = '0'+date[2]
		if len(date[1]) == 1:
			date[1] = '0'+date[1]
		if len(time[1]) == 1:
			time[1] = '0'+time[1]
		if len(time[0]) == 1:
			time[0] = '0'+time[0]
		return date[0]+'-'+date[1]+'-'+date[2]+' '+time[0]+':'+time[1]+':'+time[2] 
	index = list(map(_handle, index))
	data.index = pd.Series(index, name = 'time1')
	data.to_csv(load_data)

def complete_data(load_data, time_list):
	data = pd.read_csv(load_data, encoding = 'gbk', index_col = 'time1')
	load_data = data.loc[time_list]['load1']
	print(load_data)

def normalize(x):
	return (np.asarray(x)/max(x)).tolist()

def is_weekend(x):
	return dt.date.isoweekday(x) not in [6, 7]
#def 

def get_time_list(start, end, drop_weekend = False):
	td = dt.datetime(2001, 1, 1, 0, 30, 0) - dt.datetime(2001, 1, 1, 0, 0, 0)
	start = dt.datetime(int(start[:4]), int(start[4:6]), int(start[6:]))
	end = dt.datetime(int(end[:4]), int(end[4:6]), int(end[6:]))
	num = int((end - start)/td)	
	if drop_weekend == True:
		return [i.strftime('%Y-%m-%d %H:%M:%S') for i in list(filter(is_weekend, [start+i*td for i in range(num+1)]))]
	else:
		return [(start+i*td).strftime('%Y-%m-%d %H:%M:%S') for i in range(num+1)]


def get_load_data(start, end, load_data, drop_weekend = False):
	data = pd.read_csv(load_data, encoding='gbk', index_col = 'time1')
	time_list = get_time_list(start, end, drop_weekend)[:-1]
	load_data = data.loc[time_list]['load1'].tolist()
	#print(load_data)
	ndays = int(len(load_data)/48)
	daily_load = []
	for i in range(ndays):
		daily_load.append(normalize(load_data[i*48:(i+1)*48]))
	#print(daily_load)
	for i in daily_load:
		plt.plot(range(48), i)
	#plt.show()
	return daily_load

def plot_load(daily_load, avg):
	for i in daily_load:
		plt.plot(range(48), i, color = 'blue')
	plt.plot(range(48), avg, linewidth = 1, color = 'red')
	return plt

def calc_dist(daily_load):
	ndays = len(daily_load)
	daily_load = np.asarray(daily_load)
	#print(np.where(np.isnan(daily_load)))
	avg = np.nanmean(daily_load, axis=0)
	err = daily_load - avg
	err_time = [np.around(err[:, i], decimals=2).tolist() for i in range(48)]
	err_time_set = [list(set(item)) for item in err_time]
	#print(err_time_set)
	err_dist = [{} for i in range(48)]
	for i in range(48):
		for err in err_time_set[i]:
			if np.isnan(err):
				continue
			count = err_time[i].count(err)
			err_dist[i][err] = count
			#print(err_dist)
	return avg, err_dist

def save_dist(err_dist):
	with open(dist_path, 'w') as f:
		for item in err_dist:
			#print(type(item))
			#count = 0
			#for key, value in item.items():
			#	if not np.isnan(value):
			#		count += 1
			count = 0
			for key, value in item.items():
				count += value
			for key, value in item.items():
				#if not np.isnan(value):
					#print(value, count)
				rate = np.around(value/count, decimals=3)
				#print(rate)
				#if rate >= 1.0:
				#	rate = 1
				f.write(str(key)+':'+str(rate)+',')
			f.write('\n')
	f.close()

def save_avg(avg):
	np.savetxt(avg_path, avg)

if __name__ == '__main__':
	#get_time_list(1)
	#clean_data(load_data)
	#a = get_time_list('20110101', '20110103')
	#print(a)
	#daily_load = get_load_data('20130911', '20160725', load_data)
	daily_load = get_load_data('20090911', '20130901', load_data)

	#print(daily_load)
	avg, err_dist, plt = calc_dist(daily_load)
	save_avg(avg)
	#print(err_dist)
	#save_dist(err_dist)
	#print(err_dist)
	#get_load_data('20091101', '20100701', load_data)

	#time_list = get_time_list('20090911', '20110915')
	#complete_data(time_list, time_list)