import pandas as pd
import numpy as np
import datetime as dt

load_data = '../../Load-Data/load_before_2013_clean.csv'

def clean_data(load_data):
	data = pd.read_csv(load_data, encoding='gbk', index_col = 'time1')
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

def normalize(x):
	return np.asarray(x)/max(x)

def get_time_list(start, end):
	td = dt.datetime(2001, 1, 1, 0, 30, 0) - dt.datetime(2001, 1, 1, 0, 0, 0)
	start = dt.datetime(int(start[:4]), int(start[4:6]), int(start[6:]))
	end = dt.datetime(int(end[:4]), int(end[4:6]), int(end[6:]))
	num = int((end - start)/td)
	return [(start+i*td).strftime('%Y-%m-%d %H:%M:%S') for i in range(num+1)]

def get_load_data(start, end, load_data):
	data = pd.read_csv(load_data, encoding='gbk', index_col = 'time1')
	time_list = get_time_list(start, end)[:-1]
	load_data = data.loc[time_list]
	print(load_data)

if __name__ == '__main__':
	#get_time_list(1)
	#clean_data(load_data)
	#a = get_time_list('20110101', '20110103')
	#print(a)
	get_load_data('20100101', '20100103', load_data)