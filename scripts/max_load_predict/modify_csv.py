import numpy as np
import pandas as pd
import datetime as dt

path = '../../modified-data/dailyDATA_clean.csv'
save_path = '../../modified-data/simp_daily_data_2.csv'
data = pd.read_csv(path, encoding='gbk')



def dump_data(data):
	new_data = pd.DataFrame()
	new_data['date'] = data['date']
	new_data['max_load'] = data['max_load']
	new_data['temperature'] = data['average_c']
	weekday_list = [1, 2, 3, 4, 5, 6, 7]
	weekdays = []
	for i in range(len(data['weekday'])):
		day = (i+6)%7
		if day == 0:
			day = 7
		weekdays.append(day)
	weekdays = pd.Series(weekdays, name = 'weekday')
	new_data['weekday'] = weekdays
	####################################################################
	##	We Choose 0 for weekday, 1 for weekend, -1 for long holidays  ##
	####################################################################
	holiday_list = [0, -1, 1]
	hol = data['hol']
	holidays = []
	for i in hol:
		if i == '小长假':
			holidays.append(-1)
		elif i == '周末':
			holidays.append(1)
		else:
			holidays.append(0)
	holidays = pd.Series(holidays, name = 'holiday')
	new_data['holiday'] = holidays
	new_data.to_csv(save_path, index = False)


if __name__ == '__main__':
	dump_data(data)