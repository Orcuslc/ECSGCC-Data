import pandas as pd
import numpy as np

path = '../../modified-data/simp_daily_data.csv'
attr_path = '../../modified-data/attr.txt'
data = pd.read_csv(path, index_col = 'date')

############################################
#	Configurations:						   #
#	MAX-LOAD = 40000					   #
#	MAX-TEMP = 45						   #
############################################
MAX_LOAD = 10000
MIN_LOAD = 10000
MAX_TEMP = 29
DAYS_BACK = 6

def scale_load(data):
	#print(min(data['max_load']))
	data['max_load'] = data['max_load'] / MAX_LOAD
	#data['max_load'] = (data['max_load']-MIN_LOAD)/(MAX_LOAD-MIN_LOAD)
	#data['temperature'] = data['temperature'] / MAX_TEMP
	data['temperature'] = abs(data['temperature'] - 20)/MAX_TEMP
	return data

def handle_weekday(weekday):
	weekday = str(weekday)
	if weekday == '1':
		res = '0 0 0 0 0 1'
	elif weekday == '2':
		res = '0 0 0 0 1 0'
	elif weekday == '3':
		res = '0 0 0 1 0 0'
	elif weekday == '4':
		res = '0 0 1 0 0 0'
	elif weekday == '5':
		res = '0 1 0 0 0 0'
	elif weekday == '6':
		res = '1 0 0 0 0 0'
	else:
		res = '0 0 0 0 0 0'
	return res


# def handle_weekday(weekday):
# 	weekday = str(weekday)
# 	return weekday
	# if weekday == '1':
	# 	return '0 0 0 0 0 0 1'
	# elif weekday == '2':
	# 	return '0 0 0 0 0 1 0'
	# elif weekday == '3':
	# 	return '0 0 0 0 1 0 0'
	# elif weekday == '4':
	# 	return '0 0 0 1 0 0 0'
	# elif weekday == '5':
	# 	return '0 0 1 0 0 0 0'
	# elif weekday == '6':
	# 	return '0 1 0 0 0 0 0'
	# else:
	# 	return '1 0 0 0 0 0 0'

# def handle_weekday(weekday):
# 	weekday = str(weekday)
# 	if weekday == '1':
# 		return '0'
# 	elif weekday == '2':
# 		return '0.1'
# 	elif weekday == '3':
# 		return '0.2'
# 	elif weekday == '4':
# 		return '0.3'
# 	elif weekday == '5':
# 		return '0.4'
# 	elif weekday == '6':
# 		return '0.8'
# 	else:
# 		return '1.0'

def handle_holiday(holiday):
	holiday = str(holiday)
	if holiday == '-1':
		holiday = '1'
	elif holiday == '1':
		holiday = '0.21'
	else:
		holiday = '0'
	return (holiday+' ')*1+holiday
	#return holiday

#def handle_weekday(weekday):
#	weekday = str(weekday)
#	if weekday in ['1', '2', '3', '4', '5']:
#		return '0'
#	#elif weekday == '6':
#	#	return '-1'
#	#else:
#	#	return '1'
#	else:
#		return '1'

# def handle_temp(temperature, index):
# 	return 

def write(data):
	with open(attr_path, 'w') as f:
		for index in range(DAYS_BACK, len(data)):
			weekday = handle_weekday(data['weekday'].iloc[index])
			holiday = str(data['holiday'].iloc[index])
			holiday = handle_holiday(holiday)
			for j in range(0, DAYS_BACK+1):
				f.write(str(data['max_load'].iloc[index-j])+ ' ')
			for j in range(0, 1):
				f.write(str(data['temperature'].iloc[index-j]) + ' ')
			# f.write(str(data['temperature'].iloc[index])+weekday+' '+holiday+'\n')
			f.write(weekday+' '+holiday+'\n')
	f.close()
			#f.write(+' '+str(index['max_load'])+' '+str(['temperature']+' '))



if __name__ == '__main__':
	data = scale_load(data)	
	write(data)