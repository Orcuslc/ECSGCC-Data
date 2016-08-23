import pandas as pd
import numpy as np
import datetime as dt

def normalize(x):
	return np.asarray(x)/max(x)

def get_time_list(start):
	td = dt.datetime(2001, 1, 1, 0, 0, 30) - dt.datetime(2001, 1, 1, 0, 0, 0)

if __name__ == '__main__':
	get_time_list(1)