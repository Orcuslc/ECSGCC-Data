import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdt
import datetime as dt

def get_max_load(data_path, date_index_path, max_load_path):
	max_load_list = []
	data = pd.read_csv(data_path, encoding='gbk')
	date_index = pd.read_csv(date_index_path)
	for i in range(len(date_index) - 1):
		date = date_index.iloc[i]['date']
		index1 = date_index.iloc[i]['index']
		index2 = date_index.iloc[i+1]['index']
		max_load = max(data.iloc[index1:index2]['load'])
		max_load_list.append(max_load)
	pdt = [dt.datetime.strptime(d, '%Y/%m/%d').date() for d in date_index['date'][:-1]]
	locator = mdt.DayLocator(bymonthday=[0, 30])
	locator.MAXTICKS = 1500
	plt.gca().xaxis.set_major_formatter(mdt.DateFormatter('%Y/%m/%d'))
	plt.gca().xaxis.set_major_locator(locator)
	plt.plot(pdt, max_load_list)
	plt.gcf().autofmt_xdate()
	plt.gca().xaxis.grid(True)
	plt.gca().yaxis.grid(True)
	date_load = pd.DataFrame({'date':date_index['date'][:-1], 'max_load':max_load_list})
	date_load.to_csv(max_load_path)
	plt.show()

if __name__ == '__main__':
	data_path = 'E:\\Desktop\\data\\load.csv'
	date_index_path = 'E:\\Chuan\\Documents\\GitHub\\ECSGCC-data\\DATA for Loads\\date-index.csv'
	max_load_path = 'E:\\Chuan\\Documents\\GitHub\\ECSGCC-data\\DATA for Loads\\date-load.csv'
	get_max_load(data_path, date_index_path, max_load_path)