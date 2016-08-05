import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_date():
	data = pd.read_csv('E:\\Desktop\\data\\load.csv', encoding='gbk')
	timelist = np.asarray(data['time'].tolist())
	indexlist = []
	datelist = []
	for index in range(len(timelist)):
		if len(timelist[index]) <= 10:
			datelist.append(timelist[index])
			indexlist.append(index)
	dates = pd.DataFrame({'date':datelist, 'index':indexlist})
	dates.to_csv('E:\\Chuan\\Documents\\GitHub\\ECSGCC-data\\DATA for Loads\\date-index.csv')

if __name__ == '__main__':
	get_date()