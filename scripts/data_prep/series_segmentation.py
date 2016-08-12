import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

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

def segment(data):
	
	
if __name__ == '__main__':
	data_path = 'E:\\Desktop\\ECSGCC\\data\\load.csv'
	data = read_data(data_path)
