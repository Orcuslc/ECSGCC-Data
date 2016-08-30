import pandas as pd
import datetime as dt

def get_time_list(start, end, step = 30):
	'''
	step: time step of the list, with its unit of 1 min
	'''
	time1 = dt.datetime(2000, 1, 1, 0, 0, 0)
	try:
		nhours = step//60
		if nhours <= 23:
			time2 = dt.datetime(2000, 1, 1, int(nhours), int(step%60), 0)
		else:
			raise BaseException('The step should be within one day.')
		
