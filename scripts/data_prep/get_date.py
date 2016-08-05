import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_date(data_path, date_index_path):
	data = pd.read_csv(data_path, encoding='gbk')
	timelist = np.asarray(data['time'].tolist())
	indexlist = []
	datelist = []
	for index in range(len(timelist)):
		if len(timelist[index]) <= 10:
			datelist.append(timelist[index])
			indexlist.append(index)
	dates = pd.DataFrame({'date':datelist, 'index':indexlist})
	dates.to_csv(date_index_path)

if __name__ == '__main__':
	data_path = 'E:\\Desktop\\data\\load.csv'
	date_index_path = 'E:\\Chuan\\Documents\\GitHub\\ECSGCC-data\\DATA for Loads\\date-index.csv'
	get_date()