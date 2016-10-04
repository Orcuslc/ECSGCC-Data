import numpy as np
import pandas as pd
from conf import *

def scale_data(data):
	"""
	Scale data to [0, 5] inteval, as a requirement of SVM.
	
	Parameters
	-----------
	data : pandas.DataFrame
		Input dataframe, with a column named `max_load` and a column named `temperature`

	Returns
	--------
	data : pandas.DataFrame
		Output dataframe, with `max_load` and `temperature` column scaled

	Raises
	-------
	ZeroDivisionError
		if `LOAD_SCALE`, `TEMP_SCALE` to be `0`.

	"""
	data['max_load'] = data['max_load']/LOAD_SCALE
	data['temperature'] = data['temperature']/TEMP_SCALE
	return data

def handle_weekday(weekday, conf = WEEKDAYS):
	"""
	Quantify the weekday information and make it into a six-number string

	Parameters
	----------
	weekday : int or string
			one of `{1, 2, 3, 4, 5, 6, 7}`
	
	conf : list of strings, optional
		Configurations of weekdays, default: `WEEKDAYS` in `conf.py`

	Returns
	--------
	res : string
		The scaled weekday information, one of the conf, respectively corresponding to the `weekday` info.

	Raises
	-------
	LookupError
		if `weekday` is not in `['1', '2', '3', '4', '5', '6', '7']`.
	"""
	weekday = str(weekday)
	if weekday == '1':
		res = conf[0]
	elif weekday == '2':
		res = conf[1]
	elif weekday == '3':
		res = conf[2]
	elif weekday == '4':
		res = conf[3]
	elif weekday == '5':
		res = conf[4]
	elif weekday == '6':
		res = conf[5]
	elif weekday == '7':
		res = conf[6]
	else:
		raise LookupError('Weekday invaild!')
	return res

def handle_holiday(holiday, length = 2,  conf = HOLIDAYS):
	"""
	Quantify the holiday information and make it a string

	Parameters
	-----------
	holiday : int or string
		one of `{-1, 0, 1}`
	   -1 : long holidays
		1 : weekends
		0 : non-holidays
	
	length : int, no less than 1
		The length of holiday factor in attrbution
		default: 2

	conf : list of strings, optional
		Configuration of holidays
		default: `HOLIDAYS` in `conf.py`

	Returns
	-------
	res : string
		The quantified holiday factor, one of the conf, respectively corresponding to the holiday info.

	Raises
	------
	LookupError
		if `holiday` not in `[-1, 0, 1]`.

	ArithmeticError
		if `length` < 1.
	"""
	holiday = str(holiday)
	if holiday == '-1':
		res = conf[0]
	elif holiday == '1':
		res = conf[1]
	elif holiday == '0':
		res = conf[2]
	else:
		raise LookupError('Holiday invalid!')
	if length < 1:
		raise ArithmeticError('length must be no less than 1!')
	return (res+' ')*(length - 1)+res

def write_attr(data_path = DATA_PATH, attr_path = ATTR_PATH):
	"""
	Main function in this module;
	Write attributes from data to files.

	Parameters
	-----------
	data_path : string
		The path of data files; data should be .csv

	attr_path : string
		The path of attribute file; attr should be .txt

	Returns
	--------
	Nothing

	Raises
	-------
	Nothing
	"""
	data = pd.read_csv(data_path, index_col = 'date')
	with open(attr_path, 'w') as f:
		for index in range(DAYS_BACK, len(data)):
			weekday = handle_weekday(data['weekday'].iloc[index])
			holiday = handle_holiday(str(data['holiday'].iloc[index]))
			for j in range(0, DAYS_BACK+1):
				f.write(str(data['max_load'].iloc[index-j])+' ')
			f.write(str(data['temperature'].iloc[index])+' ')
			f.write(weekday+' '+holiday+'\n')
	f.close()